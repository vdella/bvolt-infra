from bvolt_infra.core_client import CoreApiClient


def test_client_default_url() -> None:
    client = CoreApiClient()
    assert client is not None
