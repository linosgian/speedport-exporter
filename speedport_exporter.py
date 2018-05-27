import io
import sys
import time

from prometheus_client import Gauge, start_http_server

from speedport_metrics import SpeedportMetrics

def register_prometheus_gauges(m_func):
    upstream_snr = Gauge('upstream_snr', 'Upstream Signal to Noise ratio (dB)')
    upstream_snr.set_function(lambda: m_func()['upstream_snr'])
    
    upstream_current_rate = Gauge('upstream_current_rate', 'Upstream rate (kbps)')
    upstream_current_rate.set_function(lambda: m_func()['upstream_current_rate'])

    upstream_crc_errors = Gauge('upstream_crc_errors', 'Upstream CRC errors')
    upstream_crc_errors.set_function(lambda: m_func()['upstream_crc_errors'])

    upstream_fec_errors = Gauge('upstream_fec_errors', 'Upstream FEC errors')
    upstream_fec_errors.set_function(lambda: m_func()['upstream_fec_errors'])

    upstream_attenuation = Gauge('upstream_attenuation', 'Upstream attenuation (dB)')
    upstream_attenuation.set_function(lambda: m_func()['upstream_attenuation'])

    downstream_snr = Gauge('downstream_snr', 'Downstream Signal to Noise ratio (dB)')
    downstream_snr.set_function(lambda: m_func()['downstream_snr'])

    downstream_current_rate = Gauge('downstream_current_rate', 'Downstream rate (kbps)')
    downstream_current_rate.set_function(lambda: m_func()['downstream_current_rate'])

    downstream_attenuation = Gauge('downstream_attenuation', 'Downstream attenuation (dB)')
    downstream_attenuation.set_function(lambda: m_func()['downstream_attenuation'])

    downstream_crc_errors = Gauge('downstream_crc_errors', 'Downstream CRC errors')
    downstream_crc_errors.set_function(lambda: m_func()['downstream_crc_errors'])

    downstream_fec_errors = Gauge('downstream_fec_errors', 'Downstream FEC errors')
    downstream_fec_errors.set_function(lambda: m_func()['downstream_fec_errors'])

    status = Gauge('status', 'Connection status, 0 for down, 1 for up')
    status.set_function(lambda: m_func()['status'])

    connection_type = Gauge('connection_type', 'Connection type, 0 for ADSL, 1 for VDSL')
    connection_type.set_function(lambda: m_func()['connection_type'])

def main():
    if len(sys.argv) < 2:
        print('Router hostname required')
        quit(1)
    router_hostname = sys.argv[1]
    speedport_metrics = SpeedportMetrics(router_hostname)
    register_prometheus_gauges(speedport_metrics.metrics)
    start_http_server(8000)
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
