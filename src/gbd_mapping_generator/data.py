import pandas as pd
import numpy as np


import vivarium_gbd_access.gbd as gbd
from .util import clean_entity_list


CAUSE_SET_ID = 3
RISK_SET_ID = 2
ETIOLOGY_SET_ID = 3


def get_survey_summary(entity: str):
    """
    get the summary result of gbd-data-survey
    :param entity: one of ['cause', 'risk_factor', 'sequela', 'etiology', 'covariate']
    :return: any additional information to notice, e.g., data existence, data range, any violated restriction
    """
    filepath = f'/share/costeffectiveness/gbd_data_survey/GBD_2017/{entity}.hdf'
    return pd.read_hdf(filepath, key='summary')

###############################################
# Canonical mappings between entities and ids #
###############################################


def get_sequelae():
    sequelae = gbd.get_sequela_id_mapping()
    sequelae = pd.DataFrame({'sequela_name': clean_entity_list(sequelae.sequela_name),
                             'sequela_id': sequelae.sequela_id})
    return sequelae.sort_values('sequela_id')


def get_etiologies():
    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies['most_detailed'] == 1]
    etiologies = pd.DataFrame({'rei_name': clean_entity_list(etiologies.rei_name),
                               'rei_id': etiologies.rei_id})
    return etiologies.sort_values('rei_id')


def get_causes(level=None):
    causes = gbd.get_cause_metadata(cause_set_id=CAUSE_SET_ID)
    if level is not None:
        causes = causes[causes.level == level]
    causes = pd.DataFrame({'cause_name': clean_entity_list(causes.cause_name),
                           'cause_id': causes.cause_id})
    return causes.sort_values('cause_id')


def get_risks():
    risks = gbd.get_rei_metadata(rei_set_id=RISK_SET_ID)
    risks = pd.DataFrame({'rei_name':  clean_entity_list(risks.rei_name),
                          'rei_id': risks.rei_id})
    return risks.sort_values('rei_id')


def get_covariates():
    covariates = gbd.get_covariate_metadata().reset_index(drop=True)
    covariates = pd.DataFrame({'covariate_name': clean_entity_list(covariates.covariate_name),
                               'covariate_id': covariates.covariate_id})
    return covariates.sort_values('covariate_id')


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


def get_covariate_list():
    return get_covariates().covariate_name.tolist()


#####################################################
# Functions to organize data for mapping production #
#####################################################

def get_sequela_data():
    sequelae = gbd.get_sequela_id_mapping()
    return list(zip(clean_entity_list(sequelae.sequela_name),
                    sequelae.sequela_id,
                    sequelae.modelable_entity_id,
                    clean_entity_list(sequelae.healthstate_name),
                    sequelae.healthstate_id))


def get_etiology_data():
    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies['most_detailed'] == 1]
    data_survey = get_survey_summary('etiology')
    assert len(etiologies) == len(data_survey)

    etiologies = etiologies.merge(data_survey, on='rei_id')
    return list(zip(clean_entity_list(etiologies.rei_name),
                    etiologies.rei_id,
                    etiologies.paf_yll_exist,
                    etiologies.paf_yld_exist,
                    etiologies.paf_yll_in_range,
                    etiologies.paf_yld_in_range))


def get_cause_data():
    sequelae = gbd.get_sequela_id_mapping().sort_values('sequela_id')

    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies['most_detailed'] == 1].sort_values('rei_id')

    cause_etiology_map = gbd.get_cause_etiology_mapping()
    cause_me_map = gbd.get_cause_me_id_mapping()
    cause_me_map['cause_name'] = clean_entity_list(cause_me_map['modelable_entity_name'])
    cause_me_map = cause_me_map[['modelable_entity_id', 'cause_name']].set_index('cause_name')

    causes = gbd.get_cause_metadata(cause_set_id=CAUSE_SET_ID)
    causes = pd.DataFrame({'cause_name': clean_entity_list(causes.cause_name),
                           'cause_id': causes.cause_id,
                           'parent_id': causes.parent_id,
                           'most_detailed': causes.most_detailed,
                           'level': causes.level,
                           'male': causes.male.replace({np.NaN: False, 1: True}),
                           'female': causes.female.replace({np.NaN: False, 1: True}),
                           'yll_only': causes.yll_only.replace({np.NaN: False, 1: True}),
                           'yld_only': causes.yld_only.replace({np.NaN: False, 1: True}),
                           'yll_age_start': causes.yll_age_start.replace({np.NaN: 0}),
                           'yll_age_end': causes.yll_age_end,
                           'yld_age_start': causes.yld_age_start.replace({np.NaN: 0}),
                           'yld_age_end': causes.yld_age_end})
    causes = causes.set_index('cause_name').join(cause_me_map).sort_values('cause_id').reset_index()

    cause_data = []
    for _, cause in causes.iterrows():
        name = cause['cause_name']
        cid = cause['cause_id']
        parent = causes.set_index('cause_id').at[cause['parent_id'], 'cause_name']
        dismod_id = cause['modelable_entity_id']
        most_detailed = cause['most_detailed']
        level = cause['level']
        restrictions = make_cause_restrictions(cause)

        eti_ids = cause_etiology_map[cause_etiology_map.cause_id == cid].rei_id.tolist()
        associated_etiologies = clean_entity_list(etiologies[etiologies.rei_id.isin(eti_ids)].rei_name)
        associated_sequelae = clean_entity_list(sequelae[sequelae.cause_id == cid].sequela_name)
        sub_causes = causes[causes.parent_id == cid].cause_name.tolist()

        cause_data.append((name, cid, dismod_id, most_detailed, level, parent, restrictions,
                           associated_sequelae, associated_etiologies, sub_causes))

    return cause_data


def make_cause_restrictions(cause):
    id_map = {0.0: [2, None],
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
              65.0: [18, 17],
              95.0: [235, 32]}

    restrictions = (
        ('male_only', not cause['female']),
        ('female_only', not cause['male']),
        ('yll_only', cause['yll_only']),
        ('yld_only', cause['yld_only']),
        ('yll_age_group_id_start', id_map[cause['yll_age_start']][0] if not cause['yld_only'] else None),
        ('yll_age_group_id_end', id_map[cause['yll_age_end']][1] if not cause['yld_only'] else None),
        ('yld_age_group_id_start', id_map[cause['yld_age_start']][0] if not cause['yll_only'] else None),
        ('yld_age_group_id_end', id_map[cause['yld_age_end']][1] if not cause['yll_only'] else None)
    )
    return tuple(restrictions)


def get_risk_data():
    risks = gbd.get_rei_metadata(RISK_SET_ID).sort_values('rei_id')
    risks = risks[['rei_id', 'level', 'rei_name', 'parent_id', 'most_detailed']].set_index('rei_id')
    risks['rei_name'] = clean_entity_list(risks['rei_name'])
    risks = risks.join(gbd.get_paf_of_one().set_index('rei_id'))
    risks = risks.join(gbd.get_cause_risk_mapping().set_index('rei_id'))
    risks = risks.join(gbd.get_category_mapping().set_index('rei_id'))
    risks = risks.join(gbd.get_mediation_mapping().set_index('rei_id'))
    risks = risks.join(gbd.get_risk_metadata().set_index('rei_id'))

    causes = get_causes().set_index('cause_id')

    out = []

    for rei_id, risk in risks.iterrows():
        name = risk['rei_name']

        most_detailed = risk['most_detailed']
        level = risk['level']
        parent = risks.at[risk['parent_id'], 'rei_name'] if level > 0 else None

        distribution = risk['exposure_type'] if not risk['exposure_type'] is np.nan else 'none'

        if distribution in ['normal', 'lognormal', 'ensemble']:
            levels = None
            scalar = risk['rr_scalar']
            if risk['tmred_dist'] is np.nan:
                tmred = (('distribution', 'draws'),
                         ('min', None),
                         ('max', None),
                         ('inverted', bool(risk['inv_exp'])))
            else:
                tmred = (('distribution', risk['tmred_dist']),
                         ('min', risk['tmrel_lower']),
                         ('max', risk['tmrel_upper']),
                         ('inverted', bool(risk['inv_exp'])))
        elif distribution == 'dichotomous':
            levels = (('cat1', 'exposed'),
                      ('cat2', 'unexposed'))
            scalar = None
            tmred = None
        elif 'polytomous' in distribution:
            levels = sorted([(cat, name) for cat, name in risk['category_map'].items()],
                            key=lambda x: int(x[0][3:]))
            max_cat = int(levels[-1][0][3:]) + 1
            levels.append((f'cat{max_cat}', 'unexposed'))
            levels = tuple(levels)
            scalar = None
            tmred = None
        else:  # It's either a custom risk or an aggregate, so we have to do a bunch of checking.
            if risk['category_map'] is not np.nan:  # It's some strange categorical risk.
                levels = sorted([(cat, name) for cat, name in risk['category_map'].items()],
                                key=lambda x: int(x[0][3:]))
                max_cat = int(levels[-1][0][3:]) + 1
                levels.append((f'cat{max_cat}', 'unexposed'))
                levels = tuple(levels)
            else:
                levels = None

            scalar = risk['rr_scalar'] if risk['rr_scalar'] is not np.nan else None
            if risk['tmred_dist'] is np.nan:
                tmred = None
            else:
                tmred = (('distribution', risk['tmred_dist']),
                         ('min', risk['tmrel_lower']),
                         ('max', risk['tmrel_upper']),
                         ('inverted', bool(risk['inv_exp'])))

        if risk['affected_cause_ids'] is not np.nan:
            affected_causes = (causes.at[cid, 'cause_name'] for cid in risk['affected_cause_ids'])
        else:
            affected_causes = []
        if risk['affected_rei_ids'] is not np.nan:
            affected_risks = [risks.at[rei_id, 'rei_name'] for rei_id in risk['affected_rei_ids']]
        else:
            affected_risks = []
        if risk['paf_of_one_cause_ids'] is not np.nan:
            paf_of_one_causes = [causes.at[cid, 'cause_name'] for cid in risk['paf_of_one_cause_ids']]
        else:
            paf_of_one_causes = []

        restrictions = (('male_only', risk['female'] is np.nan),
                        ('female_only', risk['male'] is np.nan),
                        ('yll_only', risk['yld'] is np.nan),
                        ('yld_only', risk['yll'] is np.nan),
                        ('yll_age_group_id_start', risk['yll_age_group_id_start'] if risk['yll'] else None),
                        ('yll_age_group_id_end', risk['yll_age_group_id_end'] if risk['yll'] else None),
                        ('yld_age_group_id_start', risk['yld_age_group_id_start'] if risk['yld'] else None),
                        ('yld_age_group_id_end', risk['yld_age_group_id_end'] if risk['yld'] else None))

        out.append((name, rei_id, most_detailed, level, parent,
                    affected_causes, paf_of_one_causes, affected_risks,
                    distribution, levels, tmred, scalar,
                    restrictions))
    return risks





def get_covariate_data():
    covariates = gbd.get_covariate_metadata()
    data_survey = get_survey_summary('covariate')

    assert set(covariates.covariate_id) == set(data_survey.covariate_id)
    covariates = covariates.merge(data_survey, on='covariate_id')
    return list(zip(clean_entity_list(covariates.covariate_name),
                    covariates.covariate_id,
                    covariates.group_display,
                    covariates.covariate_type,
                    covariates.by_age,
                    covariates.by_sex,
                    covariates.dichotomous,
                    covariates.data_exist,
                    covariates.lower_value_exist,
                    covariates.upper_value_exist,
                    covariates.mean_value_exist,
                    covariates.sex_restriction_violated,
                    covariates.age_restriction_violated,))


def get_coverage_gap_metadata(coverage_gap):
    return gbd.get_coverage_gap_metadata(coverage_gap)


def get_coverage_gap_list():
    return sorted(gbd.get_coverage_gap_list())


def get_coverage_gap_data():
    out = []
    for c in gbd.get_coverage_gap_list():
        metadata = get_coverage_gap_metadata(c)

        gbd_id = metadata['gbd_id'] if 'gbd_id' in metadata else None
        restrictions = tuple((k, v) for k, v in metadata['restrictions'].items())
        levels = tuple((k, v) for k, v in metadata['levels'].items())

        affected_causes = metadata.get('affected_causes') if 'affected_causes' in metadata else []
        affected_risk_factors = metadata.get('affected_risk_factors') if 'affected_risk_factors' in metadata else []

        out.append((c, gbd_id, metadata['distribution'], restrictions, levels, affected_causes,
                    affected_risk_factors))

    return out
