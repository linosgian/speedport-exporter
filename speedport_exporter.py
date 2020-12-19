import os
from flask import Flask, Response

from prometheus_client import Gauge, generate_latest

from speedport_metrics import SpeedportMetrics

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

app = Flask(__name__)

upstream_snr = Gauge('upstream_snr', 'Upstream Signal to Noise ratio (dB)')
downstream_snr = Gauge('downstream_snr', 'Downstream Signal to Noise ratio (dB)')

dsl_crc_errors = Gauge('upstream_crc_errors', 'DSL CRC errors')
dsl_fec_errors = Gauge('upstream_fec_errors', 'DSL FEC errors')

upstream_attenuation = Gauge('upstream_attenuation', 'Upstream attenuation (dB)')
downstream_attenuation = Gauge('downstream_attenuation', 'Downstream attenuation (dB)')

upstream_current_rate = Gauge('upstream_current_rate', 'Upstream rate (Mbps)')
downstream_current_rate = Gauge('downstream_current_rate', 'Downstream rate (Mbps)')

status = Gauge('status', 'Connection status, 0 for down, 1 for up')

router_hostname = os.environ.get('ROUTER_HOSTNAME', '192.168.1.1')
speedport_metrics = SpeedportMetrics(router_hostname)

@app.route('/metrics', methods=['GET'])
def metrics():
    cur_metrics = speedport_metrics.metrics()

    upstream_snr.set(cur_metrics['upstream_snr'])
    upstream_current_rate.set(cur_metrics['upstream_current_rate'])
    downstream_snr.set(cur_metrics['downstream_snr'])
    downstream_current_rate.set(cur_metrics['downstream_current_rate'])
    dsl_crc_errors.set(cur_metrics['dsl_crc_errors'])
    dsl_fec_errors.set(cur_metrics['dsl_fec_errors'])
    status.set(cur_metrics['dsl_fec_errors'])
    upstream_attenuation.set(cur_metrics['upstream_attenuation'])
    downstream_attenuation.set(cur_metrics['downstream_attenuation'])
    status.set(cur_metrics['dsl_status'])
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
