import pandas as pd
import numpy as np


import vivarium_gbd_access.gbd as gbd
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
    data = get_covariate_data()
    data = {c[0]: c[1] for c in data}

    covariates = pd.DataFrame.from_dict(data, orient='index').reset_index()
    covariates = covariates.rename(columns={'index':'covariate_name', 0:'covariate_id'})
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
    data_survey = gbd.get_survey_summary('sequela', SURVEY_LOCATION_ID)
    assert len(sequelae) == len(data_survey)
    sequelae = sequelae.merge(data_survey, on='sequela_id')
    dw = gbd.get_auxiliary_data('disability_weight', 'sequela', 'all')
    sequelae['disability_weight_exists'] = sequelae['healthstate_id'].apply(lambda h: bool(h in set(dw.healthstate_id)))
    return list(zip(clean_entity_list(sequelae.sequela_name),
                    sequelae.sequela_id,
                    sequelae.modelable_entity_id,
                    clean_entity_list(sequelae.healthstate_name),
                    sequelae.healthstate_id,
                    sequelae.disability_weight_exists,
                    sequelae.incidence_exists,
                    sequelae.prevalence_exists,
                    sequelae.birth_prevalence_exists,
                    sequelae.incidence_in_range,
                    sequelae.prevalence_in_range,
                    sequelae.birth_prevalence_in_range))


def get_etiology_data():
    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies['most_detailed'] == 1]
    data_survey = gbd.get_survey_summary('etiology', SURVEY_LOCATION_ID)

    assert len(etiologies) == len(data_survey)

    etiologies = pd.merge(data_survey, etiologies, left_on=['etiology_id'], right_on=['rei_id']).sort_values(['rei_id'])
    return list(zip(clean_entity_list(etiologies.rei_name),
                    etiologies.rei_id,
                    etiologies.paf_yll_exists,
                    etiologies.paf_yld_exists,
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
    data_survey = gbd.get_survey_summary('cause', SURVEY_LOCATION_ID)
    assert len(causes) == len(data_survey)

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

    causes = causes.merge(data_survey, on='cause_id')
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
        prev_exists = cause['prevalence_exists']
        inc_exists = cause['incidence_exists']
        remission_exists = cause['remission_exists']
        deaths_exists = cause['deaths_exists']
        birth_prevalence_exists = cause['birth_prevalence_exists']
        prev_in_range = cause['prevalence_in_range']
        inc_in_range = cause['incidence_in_range']
        remission_in_range = cause['remission_in_range']
        deaths_in_range = cause['deaths_in_range']
        birth_prev_in_range = cause['birth_prevalence_in_range']
        prev_consistent = cause['prevalence_consistent']
        inc_consistent = cause['incidence_consistent']
        deaths_consistent = cause['deaths_consistent']
        birth_prev_consistent = cause['birth_prevalence_consistent']
        prev_aggregates = cause['prevalence_aggregates']
        inc_aggregates = cause['incidence_aggregates']
        deaths_aggregates = cause['deaths_aggregates']
        birth_prev_aggregates = cause['birth_prevalence_aggregates']

        eti_ids = cause_etiology_map[cause_etiology_map.cause_id == cid].rei_id.tolist()
        associated_etiologies = clean_entity_list(etiologies[etiologies.rei_id.isin(eti_ids)].rei_name)
        associated_sequelae = clean_entity_list(sequelae[sequelae.cause_id == cid].sequela_name)
        sub_causes = causes[causes.parent_id == cid].cause_name.tolist()

        cause_data.append((name, cid, dismod_id, most_detailed, level, parent, restrictions, prev_exists, inc_exists,
                           remission_exists, deaths_exists, birth_prevalence_exists, prev_in_range, inc_in_range,
                           remission_in_range, deaths_in_range, birth_prev_in_range, prev_consistent, inc_consistent,
                           deaths_consistent, birth_prev_consistent, prev_aggregates, inc_aggregates, deaths_aggregates,
                           birth_prev_aggregates, associated_sequelae, associated_etiologies, sub_causes))

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
        ('yld_age_group_id_end', id_map[cause['yld_age_end']][1] if not cause['yll_only'] else None),
        ('violated', tuple(cause['violated_restrictions']))
    )
    return tuple(restrictions)


def get_all_risk_metadata():
    risks = gbd.get_rei_metadata(RISK_SET_ID).sort_values('rei_id')
    risks = risks[['rei_id', 'level', 'rei_name', 'parent_id', 'most_detailed']].set_index('rei_id')
    risks['rei_name'] = clean_entity_list(risks['rei_name'])
    risks = risks.join(gbd.get_paf_of_one().set_index('rei_id'))
    risks = risks.join(gbd.get_cause_risk_mapping().set_index('rei_id'))
    risks = risks.join(gbd.get_category_mapping().set_index('rei_id'))
    risks = risks.join(gbd.get_mediation_mapping().set_index('rei_id'))
    risks = risks.join(gbd.get_risk_metadata().set_index('rei_id'))
    risks.rei_calculation_type = risks.rei_calculation_type.map({'0': 'aggregation',
                                                                 '1': 'categorical',
                                                                 '2': 'continuous',
                                                                 '3': 'custom',
                                                                 '4': 'direct'})
    return risks


def get_risk_data():
    risks = get_all_risk_metadata()
    causes = get_causes().set_index('cause_id')

    data_survey = gbd.get_survey_summary("risk_factor", SURVEY_LOCATION_ID)
    risks = risks.join(data_survey, how='left') 

    out = []

    for rei_id, risk in risks.iterrows():
        name = risk['rei_name']

        most_detailed = risk['most_detailed']
        level = risk['level']
        parent = risks.at[risk['parent_id'], 'rei_name']

        paf_calculation_type = risk['rei_calculation_type']
        distribution = risk['exposure_type'] if not risk['exposure_type'] is np.nan else None

        exposure_exists = risk['exposure_exists']
        exposure_year_type = risk['exposure_year_type']

        paf_yll_exists = risk['paf_yll_exists']
        paf_yll_in_range = risk['paf_yll_in_range']

        paf_yld_exists = risk['paf_yld_exists']
        paf_yld_in_range = risk['paf_yld_in_range']

        if distribution in ['normal', 'lognormal', 'ensemble']:
            exposure_sd_exists = risk['exposure_sd_exists']

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
            exposure_sd_exists = None

            levels = (('cat1', 'exposed'),
                      ('cat2', 'unexposed'))
            scalar = None
            tmred = None
        elif distribution in ['ordered_polytomous', 'unordered_polytomous']:
            exposure_sd_exists = None

            levels = sorted([(cat, name) for cat, name in risk['category_map'].items()],
                            key=lambda x: int(x[0][3:]))
            max_cat = int(levels[-1][0][3:]) + 1
            levels.append((f'cat{max_cat}', 'unexposed'))
            levels = tuple(levels)
            scalar = None
            tmred = None
        else:  # It's either a custom risk or an aggregate, so we have to do a bunch of checking.
            exposure_sd_exists = None
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
            # TODO: WHAT IS CID 311 ??
            affected_causes = tuple(causes.at[cid, 'cause_name'] for cid in risk['affected_cause_ids'] if cid in causes.index)
        else:
            affected_causes = []
        if risk['affected_rei_ids'] is not np.nan:
            affected_risks = tuple(risks.at[rei_id, 'rei_name'] for rei_id in risk['affected_rei_ids'])
        else:
            affected_risks = []
        if risk['paf_of_one_cause_ids'] is not np.nan:
            paf_of_one_causes = tuple(causes.at[cid, 'cause_name'] for cid in risk['paf_of_one_cause_ids'])
        else:
            paf_of_one_causes = []

        if paf_calculation_type in ['continuous', 'categorical', 'custom']:
            rr_exists = risk['rr_exists']
            rr_in_range = risk['rr_in_range']
        else:
            rr_exists = None
            rr_in_range = None

        violated_restrictions = []
        for restr_type in ["exposure_age_restriction_violated", "exposure_sex_restriction_violated",
                           "rr_age_restriction_violated", "rr_sex_restriction_violated",
                           "paf_yll_age_restriction_violated", "paf_yll_sex_restriction_violated",
                           "paf_yld_age_restriction_violated", "paf_yld_sex_restriction_violated"]:
            if risk[restr_type] is not np.nan and risk[restr_type]:
                violated_restrictions.append(restr_type)

        sub_risks = risks[risks.parent_id == rei_id].rei_name.tolist()

        restrictions = (('male_only', risk['female'] is np.nan),
                        ('female_only', risk['male'] is np.nan),
                        ('yll_only', risk['yld'] is np.nan),
                        ('yld_only', risk['yll'] is np.nan),
                        ('yll_age_group_id_start', risk['yll_age_group_id_start'] if risk['yll'] is not np.nan else None),
                        ('yll_age_group_id_end', risk['yll_age_group_id_end'] if risk['yll'] is not np.nan else None),
                        ('yld_age_group_id_start', risk['yld_age_group_id_start'] if risk['yld'] is not np.nan else None),
                        ('yld_age_group_id_end', risk['yld_age_group_id_end'] if risk['yld'] is not np.nan else None),
                        ('violated', violated_restrictions))

        out.append((name, rei_id, most_detailed, level, paf_calculation_type, affected_causes, paf_of_one_causes,
                    distribution, levels, tmred, scalar,
                    exposure_exists, exposure_sd_exists, exposure_year_type, rr_exists, rr_in_range,
                    paf_yll_exists, paf_yll_in_range, paf_yld_exists, paf_yld_in_range,
                    restrictions, parent, sub_risks, affected_risks))
    return out


def get_covariate_data():
    covariates = gbd.get_covariate_metadata()
    data_survey = gbd.get_survey_summary('covariate', SURVEY_LOCATION_ID)
    data_survey = data_survey[data_survey.covariate_id.isin(covariates.covariate_id)]

    covariates = covariates.merge(data_survey, on='covariate_id')
    return list(zip(clean_entity_list(covariates.covariate_name),
                    covariates.covariate_id,
                    covariates.by_age,
                    covariates.by_sex,
                    covariates.dichotomous,
                    covariates.mean_value_exists,
                    covariates.uncertainty_exists,
                    covariates.violated_restrictions))


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
