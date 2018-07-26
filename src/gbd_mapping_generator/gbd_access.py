import os
import platform
import warnings

import pandas as pd


GBD_ROUND_ID = 4

AUXILIARY_DATA_FOLDER = "{j_drive}/Project/Cost_Effectiveness/CEAM/Auxiliary_Data/{gbd_round}"

FILES = {
    'Risk Data': {
        'path': 'metadata/risk_variables.xlsx',
        'source': '/home/j/WORK/05_risk/central/documentation/GBD\ 2016/risk_variables.xlsx',
        'owner': 'Kelly Cercy <kcercy@uw.edu>'
    },
    'Risk Standard Deviation Meids': {
        'path': 'metadata/risk_exposure_sd_mapping.csv',
        'owner': 'Zane Rankin <zrankin@uw.edu>',
    },
}


def auxiliary_file_path(name, **kwargs):
    template_parameters = dict(kwargs)
    if platform.system() == "Windows":
        template_parameters['j_drive'] = "J:"
    elif platform.system() == "Linux":
        template_parameters['j_drive'] = "/home/j"
    elif platform.system() == "Darwin":
        template_parameters['j_drive'] = "/home/j"
    else:
        raise IOError
    raw_path = FILES[name]['path']
    return os.path.join(AUXILIARY_DATA_FOLDER, raw_path).format(**template_parameters), FILES[name].get('encoding')


def get_data_from_auxiliary_file(file_name: str, **kwargs) -> pd.DataFrame:
    """Gets data from our auxiliary files, i.e. data not accessible from the gbd databases."""
    kwargs = dict(kwargs)
    kwargs['gbd_round'] = {4: 'GBD_2016'}[GBD_ROUND_ID]
    path, encoding = auxiliary_file_path(file_name, **kwargs)
    file_type = path.split('.')[-1]
    if file_type == 'csv':
        data = pd.read_csv(path, encoding=encoding)
    elif file_type in ('h5', 'hdf'):
        data = pd.read_hdf(path, encoding=encoding)
    elif file_type == 'dta':
        data = pd.read_stata(path, encoding=encoding)
    elif file_type == 'xlsx':
        data = pd.read_excel(path, encoding=encoding)
    else:
        raise NotImplementedError("File type {} is not supported".format(file_type))
    return data


def get_sequela_set_version_id(gbd_round_id: int) -> int:
    """Grabs the sequela set version associated with a particular gbd round."""
    from db_tools import ezfuncs

    warnings.filterwarnings("default", module="db_tools")

    q = """
        SELECT gbd_round_id,
               sequela_set_version_id
        FROM epi.sequela_set_version_active
        """
    return ezfuncs.query(q, conn_def='epi').set_index('gbd_round_id').at[gbd_round_id, 'sequela_set_version_id']


def get_cause_risk_set_version_id(gbd_round_id: int) -> int:
    """Grabs the version id associated with a cause risk mapping for a particular gbd round."""
    from db_tools import ezfuncs
    warnings.filterwarnings("default", module="db_tools")

    q = f"""
         SELECT cause_risk_set_version_id
         FROM shared.cause_risk_set_version_active
         WHERE gbd_round_id = {gbd_round_id}
         """
    return ezfuncs.query(q, conn_def='epi').at[0, 'cause_risk_set_version_id']


def get_cause_etiology_mapping(gbd_round_id: int) -> pd.DataFrame:
    """Get a mapping between the diarrhea and lri cause ids and the rei_ids associated with their etiologies."""
    from db_tools import ezfuncs
    warnings.filterwarnings("default", module="db_tools")

    # FIXME: This table has not been updated with the round 4 mapping, but Joe Wagner assures
    # me that the mapping did not change from round 3.  He's going to update the table, then we
    # should remove this.
    if gbd_round_id == 4:
        gbd_round_id = 3

    q = f""" 
        SELECT rei_id,
               cause_id
        FROM shared.cause_etiology
        WHERE gbd_round_id = {gbd_round_id}
        AND cause_id in (302, 322)
        """
    return ezfuncs.query(q, conn_def='epi')


def get_healthstate_mapping() -> pd.DataFrame:
    """Get a mapping between healthstate ids and the healthstate names.

    Notes
    -----
    This mapping is stable between gbd rounds.
    """
    from db_tools import ezfuncs
    warnings.filterwarnings("default", module="db_tools")

    q = """
        SELECT healthstate_id,
               healthstate_name
        FROM epi.healthstate
        """
    return ezfuncs.query(q, conn_def='epi')


def get_cause_me_id_mapping() -> pd.DataFrame:
    """Get a mapping between causes and epi/dismod models"""
    from db_tools import ezfuncs
    warnings.filterwarnings("default", module="db_tools")

    q = """SELECT modelable_entity_id,
                  cause_id, 
                  modelable_entity_name
           FROM epi.modelable_entity_cause
           JOIN epi.modelable_entity USING (modelable_entity_id)"""
    return ezfuncs.query(q, conn_def='epi')


def get_cause_risk_mapping(cause_risk_set_version_id: int) -> pd.DataFrame:
    """Get a mapping between risk ids and cause ids for a particular gbd round."""
    from db_tools import ezfuncs
    warnings.filterwarnings("default", module="db_tools")

    q = f"""SELECT cause_id,
                    rei_id
            FROM shared.cause_risk_hierarchy_history
            WHERE cause_risk_set_version_id = {cause_risk_set_version_id}
         """
    return ezfuncs.query(q, conn_def='epi')


def get_sequela_id_mapping(model_version: int) -> pd.DataFrame:
    """Grabs a mapping between sequelae ids and their associated names, me_ids, cause_ids, and healthstate_ids."""
    from db_tools import ezfuncs
    warnings.filterwarnings("default", module="db_tools")

    q = f"""SELECT sequela_id,
                   sequela_name,
                   modelable_entity_id,
                   cause_id, 
                   healthstate_id
            FROM epi.sequela_hierarchy_history
            WHERE sequela_set_version_id = {model_version}"""
    return ezfuncs.query(q, conn_def='epi')


def get_rei_metadata(rei_set_id: int) -> pd.DataFrame:
    """Gets a whole host of metadata associated with a particular rei set and gbd round"""
    import db_queries
    warnings.filterwarnings("default", module="db_queries")

    return db_queries.get_rei_metadata(rei_set_id=rei_set_id, gbd_round_id=GBD_ROUND_ID)


def get_cause_metadata(cause_set_id: int) -> pd.DataFrame:
    """Gets a whole host of metadata associated with a particular cause set and gbd round"""
    import db_queries
    warnings.filterwarnings("default", module="db_queries")

    return db_queries.get_cause_metadata(cause_set_id=cause_set_id, gbd_round_id=GBD_ROUND_ID)


def get_risk(risk_id: int):  # FIXME: I don't know how to properly annotate the return type
    """Gets a risk object containing info about the exposure distribution type and names of exposure categories."""
    # TODO: Change to using gbd_artifacts
    from risk_utils.classes import risk

    warnings.filterwarnings("default", module="risk_utils")

    return risk(risk_id=risk_id, gbd_round_id=GBD_ROUND_ID)


def get_covariate_metadata() -> pd.DataFrame:
    from db_tools import ezfuncs
    warnings.filterwarnings("default", module="db_tools")

    q = """SELECT covariate_id,
                  covariate_name,
                  group_display,
                  by_age, 
                  by_sex,
                  dichotomous,
                  covariate_type
           FROM shared.covariate
           JOIN shared.covariate_type USING (covariate_type_id)
           WHERE inactive = 0"""
    return ezfuncs.query(q, conn_def='epi')
