const metrics = [
  ["grid_voltage_l1", "Grid Voltage L1", "V"],
  ["grid_voltage_l2", "Grid Voltage L2", "V"],
  ["grid_voltage_l3", "Grid Voltage L3", "V"],
  ["total_load_power", "Total Load Power", "W"],
  ["pv_power", "PV Power", "W"],
  ["total_grid_power", "Total Grid Power", "W"],
  ["battery_soc", "Battery SOC", "%"],
  ["battery_voltage", "Battery Voltage", "V"],
  ["battery_current", "Battery Current", "A"],
  ["battery_power", "Battery Power", "W"],
  ["battery_temperature", "Battery Temperature", "C"]
];
const telemetryPanelStateKey = "bvolt-infra.telemetry-panel.open";

function getMetricFamily(key) {
  if (key.startsWith("battery_")) {
    return "battery";
  }
  if (key.startsWith("grid_") || key.includes("grid")) {
    return "grid";
  }
  if (key.startsWith("pv_") || key.includes("pv")) {
    return "pv";
  }
  if (key.includes("load")) {
    return "load";
  }
  return "default";
}

function initializeTelemetryPanelState() {
  const panel = document.getElementById("telemetry-panel");
  if (!panel) {
    return;
  }

  try {
    const savedState = window.localStorage.getItem(telemetryPanelStateKey);
    if (savedState === "true") {
      panel.open = true;
    } else if (savedState === "false") {
      panel.open = false;
    }

    panel.addEventListener("toggle", () => {
      window.localStorage.setItem(telemetryPanelStateKey, String(panel.open));
    });
  } catch {
    // Ignore storage access errors and fall back to default details behavior.
  }
}

function formatValue(value, unit) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "-";
  }
  return `${Number(value).toFixed(2)} ${unit}`;
}

function renderCard(label, state) {
  if (!state) {
    return `
      <article class="card">
        <h2>${label}</h2>
        <p>No telemetry available.</p>
      </article>
    `;
  }

  const rows = metrics.map(([key, title, unit]) => `
    <div class="metric-row metric-row--${getMetricFamily(key)}">
      <dt>${title}</dt>
      <dd>${formatValue(state[key], unit)}</dd>
    </div>
  `).join("");

  return `
    <article class="card">
      <h2>${label}</h2>
      <dl>${rows}</dl>
    </article>
  `;
}

async function refresh() {
  const status = document.getElementById("status");
  const cards = document.getElementById("cards");

  try {
    const response = await fetch("/api/inverters/latest");
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const payload = await response.json();
    cards.innerHTML = Object.entries(payload)
      .map(([label, state]) => renderCard(label, state))
      .join("");
    status.textContent = `Last refresh: ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    status.textContent = "Refresh failed. Check bvolt-core connectivity.";
  }
}

refresh();
initializeTelemetryPanelState();
setInterval(refresh, (window.BVOLT_INFRA?.refreshSeconds || 5) * 1000);
