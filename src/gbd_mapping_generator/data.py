from typing import List

import numpy as np
import pandas as pd

# The purpose of this import block is to mask the dependency on internal
# IHME data and allow CI and automated testing to work.
try:
    from vivarium_gbd_access import gbd
except ModuleNotFoundError:

    class GbdDummy:
        """Mock class to wrap internal dependency."""

        def __getattr__(self, item):
            raise ModuleNotFoundError("Required package vivarium_gbd_access not found.")

    gbd = GbdDummy()

from .globals import CovariateData, CovariateDataSeq
from .util import clean_entity_list

CAUSE_SET_ID = 3
RISK_SET_ID = 2
ETIOLOGY_SET_ID = 3

SURVEY_LOCATION_ID = 180
###############################################
# Canonical mappings between entities and ids #
###############################################


def get_sequelae():
    sequelae = gbd.get_sequela_id_mapping()
    sequelae = pd.DataFrame(
        {
            "sequela_name": clean_entity_list(sequelae.sequela_name),
            "sequela_id": sequelae.sequela_id,
        }
    )
    return sequelae.sort_values("sequela_id")


def get_etiologies():
    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies["most_detailed"] == 1]
    etiologies = pd.DataFrame(
        {"rei_name": clean_entity_list(etiologies.rei_name), "rei_id": etiologies.rei_id}
    )
    return etiologies.sort_values("rei_id")


def get_causes(level=None):
    causes = gbd.get_cause_metadata(cause_set_id=CAUSE_SET_ID)
    if level is not None:
        causes = causes[causes.level == level]
    causes = pd.DataFrame(
        {"cause_name": clean_entity_list(causes.cause_name), "cause_id": causes.cause_id}
    )
    return causes.sort_values("cause_id")


def get_risks():
    risks = gbd.get_rei_metadata(rei_set_id=RISK_SET_ID)
    risks = pd.DataFrame(
        {"rei_name": clean_entity_list(risks.rei_name), "rei_id": risks.rei_id}
    )
    return risks.sort_values("rei_id")


def get_covariates():
    covariates = get_covariate_data()
    covariates = {c[0]: c[1] for c in covariates}
    covariates = pd.DataFrame.from_dict(covariates, orient="index").reset_index()
    return covariates.rename(
        columns={"index": "covariate_name", 0: "covariate_id"}
    ).sort_values("covariate_id")


#####################################
# Lists of entity names in id order #
#####################################


def get_sequela_list():
    return get_sequelae().sequela_name.tolist()


def get_etiology_list():
    return get_etiologies().rei_name.tolist()


def get_cause_list():
    return get_causes().cause_name.tolist()


def get_risk_list():
    return get_risks().rei_name.tolist()


def get_covariate_list(with_survey=False):
    return get_covariates().covariate_name.tolist()


#####################################################
# Functions to organize data for mapping production #
#####################################################


def get_sequela_data() -> List:
    sequelae = gbd.get_sequela_id_mapping()

    return list(
        zip(
            clean_entity_list(sequelae.sequela_name),
            sequelae.sequela_id,
            sequelae.modelable_entity_id,
            clean_entity_list(sequelae.healthstate_name),
            sequelae.healthstate_id,
        )
    )


def get_etiology_data() -> List:
    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies["most_detailed"] == 1]

    return list(zip(clean_entity_list(etiologies.rei_name), etiologies.rei_id))


def get_cause_data():
    sequelae = gbd.get_sequela_id_mapping().sort_values("sequela_id")

    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies["most_detailed"] == 1].sort_values("rei_id")

    cause_etiology_map = gbd.get_cause_etiology_mapping()
    cause_me_map = gbd.get_cause_me_id_mapping()
    cause_me_map["cause_name"] = clean_entity_list(cause_me_map["modelable_entity_name"])
    cause_me_map = cause_me_map[["modelable_entity_id", "cause_name"]].set_index("cause_name")

    causes = gbd.get_cause_metadata(cause_set_id=CAUSE_SET_ID)

    causes = pd.DataFrame(
        {
            "cause_name": clean_entity_list(causes.cause_name),
            "cause_id": causes.cause_id,
            "parent_id": causes.parent_id,
            "most_detailed": causes.most_detailed,
            "level": causes.level,
            "male": causes.male.replace({np.NaN: False, 1: True}),
            "female": causes.female.replace({np.NaN: False, 1: True}),
            "yll_only": causes.yll_only.replace({np.NaN: False, 1: True}),
            "yld_only": causes.yld_only.replace({np.NaN: False, 1: True}),
            "yll_age_start": causes.yll_age_start.replace({np.NaN: 0}),
            "yll_age_end": causes.yll_age_end.replace({np.NaN: 95}),
            "yld_age_start": causes.yld_age_start.replace({np.NaN: 0}),
            "yld_age_end": causes.yld_age_end.replace({np.NaN: 95}),
        }
    )

    causes = (
        causes.set_index("cause_name")
        .join(cause_me_map)
        .sort_values("cause_id")
        .reset_index()
    )

    cause_data = []
    for _, cause in causes.iterrows():
        name = cause["cause_name"]
        cid = cause["cause_id"]
        parent = causes.set_index("cause_id").at[cause["parent_id"], "cause_name"]
        dismod_id = cause["modelable_entity_id"]
        most_detailed = cause["most_detailed"]
        level = cause["level"]
        restrictions = make_cause_restrictions(cause)
        eti_ids = cause_etiology_map[cause_etiology_map.cause_id == cid].rei_id.tolist()
        associated_etiologies = clean_entity_list(
            etiologies[etiologies.rei_id.isin(eti_ids)].rei_name
        )
        associated_sequelae = clean_entity_list(
            sequelae[sequelae.cause_id == cid].sequela_name
        )
        sub_causes = causes[causes.parent_id == cid].cause_name.tolist()

        cause_data.append(
            (
                name,
                cid,
                dismod_id,
                most_detailed,
                level,
                parent,
                restrictions,
                associated_sequelae,
                associated_etiologies,
                sub_causes,
            )
        )

    return cause_data


def get_age_restriction_edge(age_restriction, end=False):
    id_map = {
        0.0: [2, None],
        0.01: [3, 2],
        0.10: [4, 3],
        1.0: [5, 4],
        5.0: [6, 5],
        10.0: [7, 6],
        15.0: [8, 7],
        20.0: [9, 8],
        30.0: [11, 10],
        40.0: [13, 12],
        45.0: [14, 13],
        50.0: [15, 14],
        55.0: [16, 15],
        60.0: [17, 16],
        65.0: [18, 17],
        95.0: [235, 32],
    }
    if not end:
        edge = id_map[age_restriction][0]
    else:  # end
        _edge = id_map[age_restriction][1]
        edge = 235 if _edge == 32 else _edge
    return edge


def make_cause_restrictions(cause):
    restrictions = (
        ("male_only", not cause["female"]),
        ("female_only", not cause["male"]),
        ("yll_only", cause["yll_only"]),
        ("yld_only", cause["yld_only"]),
        (
            "yll_age_group_id_start",
            get_age_restriction_edge(cause["yll_age_start"])
            if not cause["yld_only"]
            else None,
        ),
        (
            "yll_age_group_id_end",
            get_age_restriction_edge(cause["yll_age_end"], end=True)
            if not cause["yld_only"]
            else None,
        ),
        (
            "yld_age_group_id_start",
            get_age_restriction_edge(cause["yld_age_start"])
            if not cause["yll_only"]
            else None,
        ),
        (
            "yld_age_group_id_end",
            get_age_restriction_edge(cause["yld_age_end"], end=True)
            if not cause["yll_only"]
            else None,
        ),
    )
    return tuple(restrictions)


def get_all_risk_metadata():
    risks = gbd.get_rei_metadata(RISK_SET_ID).sort_values("rei_id")
    risks = risks[["rei_id", "level", "rei_name", "parent_id", "most_detailed"]].set_index(
        "rei_id"
    )
    risks["rei_name"] = clean_entity_list(risks["rei_name"])
    risks = risks.join(gbd.get_paf_of_one().set_index("rei_id"))
    risks = risks.join(gbd.get_cause_risk_mapping().set_index("rei_id"))
    risks = risks.join(gbd.get_category_mapping().set_index("rei_id"))
    risks = risks.join(gbd.get_mediation_mapping().set_index("rei_id"))
    risks = risks.join(gbd.get_risk_metadata().set_index("rei_id"))
    risks.rei_calculation_type = risks.rei_calculation_type.map(
        {
            "0": "aggregation",
            "1": "categorical",
            "2": "continuous",
            "3": "custom",
            "4": "direct",
        }
    )
    return risks


def get_risk_data() -> List:
    risks = get_all_risk_metadata()
    causes = get_causes().set_index("cause_id")

    out = []
    # Some polytomous risks have an explicit tmrel category, some do not.
    contain_tmrel = [128, 339]

    for rei_id, risk in risks.iterrows():
        name = risk["rei_name"]

        most_detailed = risk["most_detailed"]
        level = risk["level"]
        parent = risks.at[risk["parent_id"], "rei_name"]

        paf_calculation_type = risk["rei_calculation_type"]
        distribution = (
            risk["exposure_type"].replace(" ", "_")
            if not pd.isnull(risk["exposure_type"])
            else None
        )

        if distribution in ["normal", "lognormal", "ensemble"]:
            levels = None
            scalar = risk["rr_scalar"]
            if pd.isnull(risk["tmred_dist"]):
                tmred = (
                    ("distribution", "draws"),
                    ("min", None),
                    ("max", None),
                    ("inverted", bool(int(risk["inv_exp"]))),
                )
            else:
                tmred = (
                    ("distribution", risk["tmred_dist"]),
                    ("min", risk["tmrel_lower"]),
                    ("max", risk["tmrel_upper"]),
                    ("inverted", bool(int(risk["inv_exp"]))),
                )
        elif distribution == "dichotomous":
            levels = (("cat1", "Exposed"), ("cat2", "Unexposed"))
            scalar = None
            tmred = None
        elif distribution in ["ordered_polytomous", "unordered_polytomous"]:
            try:
                levels = sorted(
                    [(cat, name) for cat, name in risk["category_map"].items()],
                    key=lambda x: int(x[0][3:]),
                )
                max_cat = int(levels[-1][0][3:]) + 1
                if rei_id not in contain_tmrel:
                    levels.append((f"cat{max_cat}", "Unexposed"))
                levels = tuple(levels)
            except AttributeError:  # sometimes the category map is nan
                if rei_id == 341:  # They screwed something up in the rei metadata
                    levels = (
                        ("cat1", "Stage 5 chronic kidney disease squeezed"),
                        ("cat2", "Stage 4 chronic kidney disease squeezed"),
                        ("cat3", "Stage 3 chronic kidney disease squeezed"),
                        ("cat4", "Stage 1-2 chronic kidney disease"),
                        ("cat5", "Unexposed"),
                    )
                else:
                    print(f'No levels found for {risk["rei_name"]}.')
                    levels = tuple()
            scalar = None
            tmred = None
        else:  # It's either a custom risk or an aggregate, so we have to do a bunch of checking.
            if not pd.isnull(risk["category_map"]):  # It's some strange categorical risk.
                levels = sorted(
                    [(cat, name) for cat, name in risk["category_map"].items()],
                    key=lambda x: int(x[0][3:]),
                )
                levels = tuple(levels)
            else:
                levels = None

            scalar = risk["rr_scalar"] if not pd.isnull(risk["rr_scalar"]) else None
            if pd.isnull(risk["tmred_dist"]):
                tmred = None
            else:
                tmred = (
                    ("distribution", risk["tmred_dist"]),
                    ("min", risk["tmrel_lower"]),
                    ("max", risk["tmrel_upper"]),
                    ("inverted", bool(risk["inv_exp"])),
                )

        if risk["affected_cause_ids"] is not np.nan:
            # TODO: WHAT IS CID 311 ??
            affected_causes = tuple(
                causes.at[cid, "cause_name"]
                for cid in risk["affected_cause_ids"]
                if cid in causes.index
            )
        else:
            affected_causes = []
        if risk["affected_rei_ids"] is not np.nan:
            affected_risks = tuple(
                risks.at[rei_id, "rei_name"] for rei_id in risk["affected_rei_ids"]
            )
        else:
            affected_risks = []
        if risk["paf_of_one_cause_ids"] is not np.nan:
            paf_of_one_causes = tuple(
                causes.at[cid, "cause_name"] for cid in risk["paf_of_one_cause_ids"]
            )
        else:
            paf_of_one_causes = []

        sub_risks = risks[risks.parent_id == rei_id].rei_name.tolist()
        restrictions = (
            ("male_only", pd.isnull(risk["female"])),
            ("female_only", pd.isnull(risk["male"])),
            ("yll_only", pd.isnull(risk["yld"])),
            ("yld_only", pd.isnull(risk["yll"])),
            (
                "yll_age_group_id_start",
                risk["yll_age_group_id_start"] if not pd.isnull(risk["yll"]) else None,
            ),
            (
                "yll_age_group_id_end",
                risk["yll_age_group_id_end"] if not pd.isnull(risk["yll"]) else None,
            ),
            (
                "yld_age_group_id_start",
                risk["yld_age_group_id_start"] if not pd.isnull(risk["yld"]) else None,
            ),
            (
                "yld_age_group_id_end",
                risk["yld_age_group_id_end"] if not pd.isnull(risk["yld"]) else None,
            ),
        )

        out.append(
            (
                name,
                rei_id,
                most_detailed,
                level,
                paf_calculation_type,
                affected_causes,
                paf_of_one_causes,
                distribution,
                levels,
                tmred,
                scalar,
                restrictions,
                parent,
                sub_risks,
                affected_risks,
            )
        )
    return out


def get_duplicate_indices(names: List[str]) -> List[int]:
    dup_indices = []
    check = set()
    for i, v in enumerate(names):
        if v not in check:
            check.add(v)
        else:
            dup_indices.append(i)
    return dup_indices


def get_covariate_data() -> CovariateDataSeq:

    covariates = gbd.get_covariate_metadata()
    clean_names = clean_entity_list(covariates.covariate_name)
    covariates.covariate_name = clean_names
    dup_indices = get_duplicate_indices(clean_names)
    covariates = covariates.drop(dup_indices).reset_index(drop=True)

    vals: CovariateData = list(
        zip(
            covariates.covariate_name,
            covariates.covariate_id,
            covariates.by_age,
            covariates.by_sex,
            covariates.dichotomous,
        )
    )
    return vals
