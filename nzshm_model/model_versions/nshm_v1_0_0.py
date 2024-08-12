#! nshm_v1_0_0.py
from typing import Dict, Any

from nzshm_model.psha_adapter.openquake.hazard_config import OpenquakeConfig
from nzshm_model.psha_adapter.openquake.hazard_config_compat import DEFAULT_HAZARD_CONFIG

model_args: Dict[str, Any] = dict(
    version='NSHM_v1.0.0',
    title="Initial version",
    slt_json="nshm_v1.0.0.json",
    gmm_json="gmcm_nshm_v1.0.0.json",
    gmm_xml="NZ_NSHM_GMM_LT_final_EE_new_names.xml",
    hazard_config=OpenquakeConfig(DEFAULT_HAZARD_CONFIG),
)
