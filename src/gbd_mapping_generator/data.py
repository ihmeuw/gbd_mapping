import pandas as pd
import numpy as np

import vivarium_gbd_access.gbd as gbd
from .util import clean_entity_list, clean_risk_me


GBD_ROUND_ID = gbd.GBD_ROUND_ID
CAUSE_SET_ID = 3
REI_SET_ID = 2
ETIOLOGY_SET_ID = 3

###############################################
# Canonical mappings between entities and ids #
###############################################


def get_sequelae():
    version_id = gbd.get_sequela_set_version_id(GBD_ROUND_ID)
    sequelae = gbd.get_sequela_id_mapping(version_id)
    sequelae = pd.DataFrame({'sequela_name': clean_entity_list(sequelae.sequela_name),
                             'sequela_id': sequelae.sequela_id})
    return sequelae.sort_values('sequela_id')


def get_etiologies():
    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies['most_detailed'] == 1]
    etiologies = pd.DataFrame({'rei_name': clean_entity_list(etiologies.rei_name),
                               'rei_id': etiologies.rei_id})
    return etiologies.sort_values('rei_id')


def get_causes():
    causes = gbd.get_cause_metadata(cause_set_id=CAUSE_SET_ID)
    causes = causes[causes.most_detailed == 1]
    causes = causes.append(pd.DataFrame({'cause_name': ['all_causes'], 'cause_id': [294]}), ignore_index=True)
    causes = pd.DataFrame({'cause_name': clean_entity_list(causes.cause_name),
                           'cause_id': causes.cause_id})
    causes = causes[causes['cause_name'] != 'none']
    return causes.sort_values('cause_id')


def get_risks():
    risks = gbd.get_rei_metadata(rei_set_id=REI_SET_ID)
    risks = risks[((risks['most_detailed'] == 1) | (risks['rei_id'] == 339)) & ~(risks['rei_id'].isin([334, 335]))]
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
    version_id = gbd.get_sequela_set_version_id(GBD_ROUND_ID)
    sequelae = gbd.get_sequela_id_mapping(version_id)
    healthstate_data = gbd.get_healthstate_mapping()
    sequelae = sequelae.join(healthstate_data.set_index('healthstate_id'), on='healthstate_id')

    return list(zip(clean_entity_list(sequelae.sequela_name),
                    sequelae.sequela_id,
                    sequelae.modelable_entity_id,
                    clean_entity_list(sequelae.healthstate_name),
                    sequelae.healthstate_id))


def get_etiology_data():
    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies['most_detailed'] == 1]
    return list(zip(clean_entity_list(etiologies.rei_name), etiologies.rei_id))


def get_cause_data():
    version_id = gbd.get_sequela_set_version_id(GBD_ROUND_ID)
    sequelae = gbd.get_sequela_id_mapping(version_id).sort_values('sequela_id')

    etiologies = gbd.get_rei_metadata(rei_set_id=ETIOLOGY_SET_ID)
    etiologies = etiologies[etiologies['most_detailed'] == 1].sort_values('rei_id')

    cause_etiology_map = gbd.get_cause_etiology_mapping(GBD_ROUND_ID)
    cause_me_map = gbd.get_cause_me_id_mapping()
    cause_me_map['cause_name'] = clean_entity_list(cause_me_map['modelable_entity_name'])
    cause_me_map = cause_me_map[['modelable_entity_id', 'cause_name']].set_index('cause_name')

    causes = gbd.get_cause_metadata(cause_set_id=CAUSE_SET_ID)
    causes = causes[((causes.most_detailed == 1) | (causes.cause_id == 294)) & ~(causes.cause_id == 740)]
    causes = pd.DataFrame({'cause_name': clean_entity_list(causes.cause_name),
                           'cause_id': causes.cause_id,
                           'male': causes.male.replace({np.NaN: False, 1: True}),
                           'female': causes.female.replace({np.NaN: False, 1: True}),
                           'yll_only': causes.yll_only.replace({np.NaN: False, 1: True}),
                           'yld_only': causes.yld_only.replace({np.NaN: False, 1: True}),
                           'yll_age_start': causes.yll_age_start.replace({np.NaN: 0}),
                           'yll_age_end': causes.yll_age_end,
                           'yld_age_start': causes.yld_age_start,
                           'yld_age_end': causes.yld_age_end})
    causes = causes.set_index('cause_name').join(cause_me_map).sort_values('cause_id').reset_index()

    cause_data = []
    for _, cause in causes.iterrows():
        name = cause['cause_name']
        if name == 'none':
            continue
        cid = cause['cause_id']
        dismod_id = cause['modelable_entity_id']

        restrictions = [('male_only', not cause['female']), ('female_only', not cause['male'])]
        restrictions.extend([('yll_only', cause['yll_only']), ('yld_only', cause['yld_only'])])
        if cause['yll_only']:
            restrictions.extend([('yll_age_start', cause['yll_age_start']), ('yll_age_end', cause['yll_age_end'])])
        elif cause['yld_only']:
            restrictions.extend([('yld_age_start', cause['yld_age_start']), ('yld_age_end', cause['yld_age_end'])])
        else:
            restrictions.extend([('yll_age_start', cause['yll_age_start']), ('yll_age_end', cause['yll_age_end'])])
            restrictions.extend([('yld_age_start', cause['yld_age_start']), ('yld_age_end', cause['yld_age_end'])])
        restrictions = tuple(restrictions)

        eti_ids = cause_etiology_map[cause_etiology_map.cause_id == cid].rei_id.tolist()
        associated_etiologies = clean_entity_list(etiologies[etiologies.rei_id.isin(eti_ids)].rei_name)
        associated_sequelae = clean_entity_list(sequelae[sequelae.cause_id == cid].sequela_name)
        cause_data.append((name, cid, dismod_id, restrictions, associated_sequelae, associated_etiologies))

    return cause_data


def load_risk_params():
    # Read in our parameter data sheet and filter out etiologies/aggregate risks/impairments
    risk_params = gbd.get_auxiliary_data(measure='metadata', entity_type='risk_factor', entity_name='risk_variables')
    risk_params = risk_params[~np.isnan(risk_params.rei_id)]

    risk_params.loc[risk_params.risk_type == 0, 'calc_type'] = 'unknown'
    risk_params.loc[risk_params.risk_type == 1, 'calc_type'] = 'categorical'
    risk_params.loc[(risk_params.risk_type == 2) & pd.isnull(risk_params.calc_type) , 'calc_type'] = 'unknown'
    risk_params.loc[risk_params.risk_type == 3, 'calc_type'] = 'unknown'  # FIXME : Only air_pm
    risk_params.loc[:, 'rei_id'] = risk_params.rei_id.astype(int)

    base = ['rei_id', 'calc_type']
    tmred = ['inv_exp', 'tmred_dist', 'tmred_para1', 'tmred_para2']
    param = ['rr_scalar', 'minval', 'maxval', 'maxrr',]
    restrictions = ['yll_only', 'yld_only', 'female_only', 'male_only']
    columns_of_interest = base + tmred + param + restrictions

    risk_params = risk_params[columns_of_interest]
    # Get the canonical mapping between rei_ids and risk names and add the names to our data
    risks = get_risks()
    risks = risks.set_index('rei_id').join(risk_params.set_index('rei_id')).reset_index()
    return risks


def get_cause_risk_mapping():
    cause_risk_mapping = gbd.get_cause_risk_mapping(gbd.get_cause_risk_set_version_id(GBD_ROUND_ID))
    causes = get_causes()
    risks = get_risks()

    mapping = cause_risk_mapping.set_index('cause_id').join(causes.set_index('cause_id')).reset_index()
    mapping = mapping[mapping.cause_name.notnull() & (mapping.cause_name != 'all_causes')]
    mapping = risks.set_index('rei_id').join(mapping.set_index('rei_id'), how='left').reset_index()

    return mapping


def get_risk_data():
    risks = load_risk_params()
    cause_risk_mapping = get_cause_risk_mapping()

    out = []
    for _, risk in risks.iterrows():
        risk = risk
        name = risk['rei_name']
        rid = risk['rei_id']

        r = gbd.get_risk(risk_id=rid)
        # No more than one of these can be true.
        assert sum([int(r.dichotomous), int(r.polytomous), int(r.continuous)]) <= 1

        distribution_type = risk['calc_type']

        distribution = 'unknown'
        levels = None
        tmred = None
        exp_params = None

        # FIXME: The data disagree about how risk 125 (physical activity) is modeled.  It is actually a continuous
        # risk for the 2016 round despite the fact that the risk utils library thinks it's a polytomous risk.
        if r.continuous or rid == 125:
            # Make sure our risk types agree
            assert distribution_type != 'categorical', f"{r.risk} {distribution_type}"
            distribution = distribution_type if distribution_type != 'unknown' else 'unknown_continuous'
            inv_exp = True if risk['inv_exp'] else False
            tmred = (('distribution', risk['tmred_dist']),
                     ('min', risk['tmred_para1']),
                     ('max', risk['tmred_para2']),
                     ('inverted', inv_exp))
            exp_params = (('scale', risk['rr_scalar']),
                          ('max_rr', risk['maxrr']),)

        elif r.dichotomous:
            assert distribution_type in ['categorical', 'unknown'], f"{r.risk} {distribution_type}"
            distribution = 'dichotomous'
            levels = (('cat1', 'exposed'), ('cat2', 'unexposed'))

        elif r.polytomous:
            is_categorical = distribution_type in ['categorical', 'unknown'] or np.isnan(distribution_type)
            assert is_categorical, f"{r.risk} {distribution_type}"

            params = r.me_df
            # FIXME: Working around some missing information in risk_utils. Already talked to Kelly Cercy about this
            # -J.C. 10/28/17
            if rid == 341:
                params = params.set_index('me_id')
                for cat, (me_id, me_name) in enumerate(zip([16442, 16443, 16444, 16445],
                                                           ['albuminuria', 'stage_iii_chronic_kidney_disease',
                                                            'stage_iv_chronic_kidney_disease',
                                                            'stage_v_chronic_kidney_disease'])):
                    params.at[me_id, 'draw_type'] = 'exposure'
                    params.at[me_id, 'me_name'] = me_name
                    params.at[me_id, 'parameter'] = 'cat' + str(cat + 1)
                params = params.loc[[16442, 16443, 16444, 16445], :]
            elif rid == 339:  # Some categories were combined near the end of the 2016 round.  Clean these up.
                params = params[params.parameter.notnull()]
                params.loc[:, 'cat'] = params.parameter.apply(lambda s: int(s.split('cat')[-1]))
                params = params.sort_values('cat')
                for i in range(1, len(params)+1):
                    params.parameter.iat[i-1] = 'cat' + str(i)
                    me_name = params.me_name.iat[i-1]
                    cleaned_me_name = me_name[19:].split('interpolated')[0][:-2]
                    params.me_name.iat[i-1] = cleaned_me_name
                params = params.reset_index()[['draw_type', 'me_name', 'parameter']]

            else:
                params.loc[:, 'me_name'] = clean_risk_me(params.me_name)

            params = params.loc[params.draw_type == 'exposure', ['me_name', 'parameter']]

            distribution = 'polytomous'

            levels = [("", "") for i in range(len(params))]
            for __, (me_name, param) in params.iterrows():
                idx = int(param.split('cat')[-1])
                levels[idx-1] = (param, me_name)
            levels.append(('cat' + str(len(params) + 1), 'unexposed'))
            levels = tuple(levels)

        restrictions = []
        for restriction in ['male_only', 'female_only', 'yll_only', 'yld_only']:
            if np.isnan(risk[restriction]):
                restrictions.append((restriction, False))
            else:
                restrictions.append((restriction, True))
        restrictions = tuple(restrictions)

        cause_list = cause_risk_mapping.loc[cause_risk_mapping.rei_id == rid, 'cause_name'].tolist()

        out.append((name, rid, distribution, restrictions, cause_list, levels, tmred, exp_params))
    return out


def get_covariate_data():
    covariates = gbd.get_covariate_metadata()
    return list(zip(clean_entity_list(covariates.covariate_name),
                    covariates.covariate_id,
                    covariates.group_display,
                    covariates.covariate_type,
                    covariates.by_age,
                    covariates.by_sex,
                    covariates.dichotomous,))


def get_coverage_gap_metadata(coverage_gap):
    return gbd.get_coverage_gap_metadata(coverage_gap)


_SPECIAL_COVERAGE_GAPS = [
    # HACK: This is in the rei hierarchy but doesn't actually get used and breaks all our patterns
    ('low_measles_vaccine_coverage_first_dose',
     318,
     'dichotomous',
     (('male_only', False), ('female_only', False), ('yll_only', False), ('yld_only', False)),
     (('cat1', 'exposed'), ('cat2', 'unexposed')),
     ['measles', ],
     []),
]


def get_coverage_gap_list():
    return sorted([c[0] for c in _SPECIAL_COVERAGE_GAPS] + gbd.get_coverage_gap_list())


def get_coverage_gap_data():
    out = _SPECIAL_COVERAGE_GAPS

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
