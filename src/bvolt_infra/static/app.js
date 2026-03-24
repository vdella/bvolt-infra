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
    <dt>${title}</dt>
    <dd>${formatValue(state[key], unit)}</dd>
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
setInterval(refresh, (window.BVOLT_INFRA?.refreshSeconds || 5) * 1000);
