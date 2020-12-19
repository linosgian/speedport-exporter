import time
import logging
import json
import requests

logging.basicConfig(format='%(asctime)s: %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_MAX_METRICS_AGE = 2 # in seconds

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
        headers = {"Accept-Language": "en-US,en;q=0.5"}
        r = requests.get("http://{}/data/Status.json".format(self.router_hostname), headers=headers)
        metrics_json = json.loads(r.text)
        metrics = {item['varid']:item['varvalue'] for item in metrics_json}
        return {
                    'upstream_snr': float(metrics['dsl_snr'].split('/')[1].strip()),
                    'upstream_current_rate': int(metrics['dsl_upstream'])/1000,
                    'downstream_snr': float(metrics['dsl_snr'].split('/')[0].strip()),
                    'downstream_current_rate': int(metrics['dsl_downstream'])/1000,
                    'dsl_crc_errors': int(metrics['dsl_crc_errors']),
                    'dsl_fec_errors': int(metrics['dsl_fec_errors']),
                    'dsl_status': 1 if metrics['dsl_status'] == 'online' else 0,
                    'downstream_attenuation': float(metrics['vdsl_atnd']),
                    'upstream_attenuation': float(metrics['vdsl_atnu']),
               }
