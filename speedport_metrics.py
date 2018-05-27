import xml.etree.ElementTree as ET
import time
import io
import logging

import pycurl

logging.basicConfig(format='%(asctime)s: %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_MAX_METRICS_AGE = 10 # in seconds

class SpeedportMetrics(object):
    def __init__(self, router_hostname, max_metrics_age=DEFAULT_MAX_METRICS_AGE):
        self.router_hostname = router_hostname
        self.max_metrics_age = max_metrics_age
        self._refresh_metrics_dict()
        
    def metrics(self):
        if self._stale_metrics():
            self._refresh_metrics_dict()
        return self.metrics_dict

    def _stale_metrics(self):
        return time.time() - self.metrics_timestamp > self.max_metrics_age

    def _refresh_metrics_dict(self):
        logger.warning('Refreshing metrics')
        self.metrics_dict = self._get_current_metrics()
        self.metrics_timestamp = time.time()

    def _get_current_metrics(self):
        metrics_bytes = self._get_metrics_bytes()
        metrics_string = metrics_bytes.decode('utf8')
        return self._parse_router_metrics(metrics_string)

    def _get_metrics_bytes(self):
        metrics_buffer = io.BytesIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, "http://{}/common_page/status_info_lua.lua".format(self.router_hostname))
        curl.setopt(curl.WRITEDATA, metrics_buffer)
        curl.perform()
        curl.close()
        return metrics_buffer.getvalue()

    @staticmethod
    def _parse_router_metrics(metrics_string):
        xml_root = ET.fromstring(metrics_string)
        dsl_metrics = [element.text for element in xml_root.findall('./OBJ_DSLINTERFACE_ID/Instance/ParaValue')]
        return {
                    'upstream_snr': int(dsl_metrics[1]) / 10,
                    'upstream_current_rate': int(dsl_metrics[2]),
                    'downstream_snr': int(dsl_metrics[3]) / 10,
                    'downstream_current_rate': int(dsl_metrics[4]),
                    'upstream_crc_errors': int(dsl_metrics[5]),
                    'downstream_attenuation': int(dsl_metrics[6]) / 10,
                    'upstream_fec_errors': int(dsl_metrics[7]),
                    'status': 1 if dsl_metrics[8] == 'Up' else 0,
                    'downstream_crc_errors': int(dsl_metrics[9]),
                    'downstream_fec_errors': int(dsl_metrics[10]),
                    'upstream_attenuation': int(dsl_metrics[11]),
                    'connection_type': 1 if dsl_metrics[12] == 'VDSL2' else 0
                }