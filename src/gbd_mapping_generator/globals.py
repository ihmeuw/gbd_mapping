from typing import List, NamedTuple, Tuple


class __IdTypes(NamedTuple):
    ME_ID: str = "me_id"
    REI_ID: str = "rei_id"
    C_ID: str = "c_id"
    S_ID: str = "s_id"
    COV_ID: str = "cov_id"
    HS_ID: str = "hs_id"


ID_TYPES = __IdTypes()


# Type aliases
CovariateData = Tuple[str, float, bool, bool, bool]
CovariateDataSeq = List[CovariateData]
