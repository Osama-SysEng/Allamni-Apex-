from shared.operational import HttpMetrics

def test_http_metrics_capture_status_and_latency():
    metrics=HttpMetrics(); metrics.started(); metrics.record('/students/me',200,.02); metrics.record('/students/me',500,.04); metrics.completed()
    snapshot=metrics.snapshot()
    assert snapshot['in_flight']==0
    assert snapshot['routes']['/students/me']['requests']==2
    assert snapshot['routes']['/students/me']['server_errors']==1
