import json

from tests.mocks.fetchers.alerts_fetcher_mock import MockAlertsFetcher


def test_get_test_alerts():
    fetcher = MockAlertsFetcher()
    test_alerts = fetcher.get_test_alerts(days_back=1)
    assert_new_alerts(test_alerts)


def test_get_model_alerts():
    fetcher = MockAlertsFetcher()
    model_alerts = fetcher.get_model_alerts(days_back=1)
    assert_new_alerts(model_alerts)


def test_get_source_freshness_alerts():
    fetcher = MockAlertsFetcher()
    source_freshness_alerts = fetcher.get_source_freshness_alerts(days_back=1)
    assert_new_alerts(source_freshness_alerts)


def test_get_new_alerts():
    fetcher = MockAlertsFetcher()
    alerts = fetcher.get_new_alerts(days_back=1)
    test_alerts = alerts.tests
    model_alerts = alerts.models
    source_freshness_alerts = alerts.source_freshnesses
    assert_new_alerts(test_alerts)
    assert_new_alerts(model_alerts)
    assert_new_alerts(source_freshness_alerts)


def assert_new_alerts(new_alerts):
    alerts_to_send = new_alerts.alerts
    alerts_to_skip = new_alerts.alerts_to_skip

    # Test the following tests are not suppresed:
    #   - Alert after suppression interval
    #   - Alert without suppression interval
    #   - First occurrence alert with suppression interval
    assert json.dumps(
        [alert.id for alert in alerts_to_send], sort_keys=True
    ) == json.dumps(["alert_id_2", "alert_id_3", "alert_id_4"], sort_keys=True)

    # Test the following tests are suppresed:
    #   - alert_id_1 (Alert whithin suppression interval)
    # Test the following tests are skipped due to dedup:
    #   - alert_id_5 (Duplication of alert_id_4 with earlier detected time)
    assert json.dumps(
        [alert.id for alert in alerts_to_skip], sort_keys=True
    ) == json.dumps(["alert_id_1", "alert_id_5"], sort_keys=True)