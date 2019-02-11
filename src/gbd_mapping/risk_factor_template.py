"""Mapping templates for GBD risk factors.

This code is automatically generated by gbd_mapping_generator/risk_builder.py

Any manual changes will be lost.
"""
from typing import Tuple, Union

from .id import reiid, scalar
from .base_template import ModelableEntity, GbdRecord, Categories, Tmred, Restrictions
from .cause_template import Cause


class RiskFactor(ModelableEntity):
    """Container for risk GBD ids and metadata."""
    __slots__ = ('name', 'kind', 'gbd_id', 'level', 'most_detailed', 'distribution',
                 'population_attributable_fraction_calculation_type', 'restrictions', 'exposure_exists',
                 'exposure_standard_deviation_exists', 'exposure_year_type', 'relative_risk_exists',
                 'relative_risk_in_range', 'population_attributable_fraction_yll_exists',
                 'population_attributable_fraction_yll_in_range', 'population_attributable_fraction_yld_exists',
                 'population_attributable_fraction_yld_in_range', 'affected_causes',
                 'population_attributable_fraction_of_one_causes', 'parent', 'sub_risk_factors',
                 'affected_risk_factors', 'categories', 'tmred', 'relative_risk_scalar', )

    def __init__(self,
                 name: str,
                 kind: str,
                 gbd_id: reiid,
                 level: int,
                 most_detailed: bool,
                 distribution: Union[str, None],
                 population_attributable_fraction_calculation_type: str,
                 restrictions: Restrictions,
                 exposure_exists: Union[bool, None],
                 exposure_standard_deviation_exists: Union[bool, None],
                 exposure_year_type: Union[str, None],
                 relative_risk_exists: Union[bool, None],
                 relative_risk_in_range: Union[bool, None],
                 population_attributable_fraction_yll_exists: Union[bool, None],
                 population_attributable_fraction_yll_in_range: Union[bool, None],
                 population_attributable_fraction_yld_exists: Union[bool, None],
                 population_attributable_fraction_yld_in_range: Union[bool, None],
                 affected_causes: Tuple[Cause, ...],
                 population_attributable_fraction_of_one_causes: Tuple[Cause, ...],
                 parent: Union["RiskFactor", None] = None,
                 sub_risk_factors: Tuple["RiskFactor", ...] = None,
                 affected_risk_factors: Tuple["RiskFactor", ...] = None,
                 categories: Categories = None,
                 tmred: Tmred = None,
                 relative_risk_scalar: scalar = None, ):
        super().__init__(name=name,
                         kind=kind,
                         gbd_id=gbd_id)
        self.name = name
        self.kind = kind
        self.gbd_id = gbd_id
        self.level = level
        self.most_detailed = most_detailed
        self.distribution = distribution
        self.population_attributable_fraction_calculation_type = population_attributable_fraction_calculation_type
        self.restrictions = restrictions
        self.exposure_exists = exposure_exists
        self.exposure_standard_deviation_exists = exposure_standard_deviation_exists
        self.exposure_year_type = exposure_year_type
        self.relative_risk_exists = relative_risk_exists
        self.relative_risk_in_range = relative_risk_in_range
        self.population_attributable_fraction_yll_exists = population_attributable_fraction_yll_exists
        self.population_attributable_fraction_yll_in_range = population_attributable_fraction_yll_in_range
        self.population_attributable_fraction_yld_exists = population_attributable_fraction_yld_exists
        self.population_attributable_fraction_yld_in_range = population_attributable_fraction_yld_in_range
        self.affected_causes = affected_causes
        self.population_attributable_fraction_of_one_causes = population_attributable_fraction_of_one_causes
        self.parent = parent
        self.sub_risk_factors = sub_risk_factors
        self.affected_risk_factors = affected_risk_factors
        self.categories = categories
        self.tmred = tmred
        self.relative_risk_scalar = relative_risk_scalar


class RiskFactors(GbdRecord):
    """Container for GBD risks."""
    __slots__ = ('unsafe_water_sanitation_and_handwashing', 'unsafe_water_source', 'unsafe_sanitation',
                 'air_pollution', 'ambient_particulate_matter_pollution', 'household_air_pollution_from_solid_fuels',
                 'ambient_ozone_pollution', 'other_environmental_risks', 'residential_radon', 'lead_exposure',
                 'child_and_maternal_malnutrition', 'suboptimal_breastfeeding', 'child_underweight',
                 'iron_deficiency', 'vitamin_a_deficiency', 'zinc_deficiency', 'tobacco', 'smoking',
                 'secondhand_smoke', 'alcohol_use', 'drug_use', 'metabolic_risks', 'high_fasting_plasma_glucose',
                 'high_systolic_blood_pressure', 'high_body_mass_index', 'low_bone_mineral_density', 'dietary_risks',
                 'diet_low_in_fruits', 'diet_low_in_vegetables', 'diet_low_in_whole_grains',
                 'diet_low_in_nuts_and_seeds', 'diet_low_in_milk', 'diet_high_in_red_meat',
                 'diet_high_in_processed_meat', 'diet_high_in_sugar_sweetened_beverages', 'diet_low_in_fiber',
                 'diet_low_in_seafood_omega_3_fatty_acids', 'diet_low_in_polyunsaturated_fatty_acids',
                 'diet_high_in_trans_fatty_acids', 'diet_high_in_sodium', 'low_physical_activity',
                 'occupational_risks', 'occupational_carcinogens', 'occupational_asthmagens',
                 'occupational_particulate_matter_gases_and_fumes', 'occupational_noise', 'occupational_injuries',
                 'occupational_ergonomic_factors', 'childhood_sexual_abuse', 'intimate_partner_violence',
                 'non_exclusive_breastfeeding', 'discontinued_breastfeeding',
                 'drug_use_dependence_and_blood_borne_viruses', 'suicide_due_to_drug_use_disorders',
                 'high_fasting_plasma_glucose_continuous', 'high_fasting_plasma_glucose_categorical',
                 'diet_low_in_calcium', 'occupational_exposure_to_asbestos', 'occupational_exposure_to_arsenic',
                 'occupational_exposure_to_benzene', 'occupational_exposure_to_beryllium',
                 'occupational_exposure_to_cadmium', 'occupational_exposure_to_chromium',
                 'occupational_exposure_to_diesel_engine_exhaust', 'occupational_exposure_to_formaldehyde',
                 'occupational_exposure_to_nickel', 'occupational_exposure_to_polycyclic_aromatic_hydrocarbons',
                 'occupational_exposure_to_silica', 'occupational_exposure_to_sulfuric_acid',
                 'intimate_partner_violence_exposure_approach', 'intimate_partner_violence_direct_paf_approach',
                 'all_risk_factors', 'unsafe_sex', 'intimate_partner_violence_hiv_paf_approach',
                 'environmental_occupational_risks', 'behavioral_risks',
                 'occupational_exposure_to_trichloroethylene', 'no_access_to_handwashing_facility',
                 'child_growth_failure', 'child_wasting', 'child_stunting', 'lead_exposure_in_blood',
                 'lead_exposure_in_bone', 'childhood_sexual_abuse_against_females',
                 'childhood_sexual_abuse_against_males', 'chewing_tobacco', 'diet_low_in_legumes',
                 'short_gestation_for_birth_weight', 'low_birth_weight_for_gestation',
                 'low_birth_weight_and_short_gestation', 'impaired_kidney_function', 'bullying_victimization',
                 'high_ldl_cholesterol', 'high_body_mass_index_in_adults', 'high_body_mass_index_in_children',
                 'particulate_matter_pollution', 'childhood_maltreatment', )

    def __init__(self,
                 unsafe_water_sanitation_and_handwashing: RiskFactor,
                 unsafe_water_source: RiskFactor,
                 unsafe_sanitation: RiskFactor,
                 air_pollution: RiskFactor,
                 ambient_particulate_matter_pollution: RiskFactor,
                 household_air_pollution_from_solid_fuels: RiskFactor,
                 ambient_ozone_pollution: RiskFactor,
                 other_environmental_risks: RiskFactor,
                 residential_radon: RiskFactor,
                 lead_exposure: RiskFactor,
                 child_and_maternal_malnutrition: RiskFactor,
                 suboptimal_breastfeeding: RiskFactor,
                 child_underweight: RiskFactor,
                 iron_deficiency: RiskFactor,
                 vitamin_a_deficiency: RiskFactor,
                 zinc_deficiency: RiskFactor,
                 tobacco: RiskFactor,
                 smoking: RiskFactor,
                 secondhand_smoke: RiskFactor,
                 alcohol_use: RiskFactor,
                 drug_use: RiskFactor,
                 metabolic_risks: RiskFactor,
                 high_fasting_plasma_glucose: RiskFactor,
                 high_systolic_blood_pressure: RiskFactor,
                 high_body_mass_index: RiskFactor,
                 low_bone_mineral_density: RiskFactor,
                 dietary_risks: RiskFactor,
                 diet_low_in_fruits: RiskFactor,
                 diet_low_in_vegetables: RiskFactor,
                 diet_low_in_whole_grains: RiskFactor,
                 diet_low_in_nuts_and_seeds: RiskFactor,
                 diet_low_in_milk: RiskFactor,
                 diet_high_in_red_meat: RiskFactor,
                 diet_high_in_processed_meat: RiskFactor,
                 diet_high_in_sugar_sweetened_beverages: RiskFactor,
                 diet_low_in_fiber: RiskFactor,
                 diet_low_in_seafood_omega_3_fatty_acids: RiskFactor,
                 diet_low_in_polyunsaturated_fatty_acids: RiskFactor,
                 diet_high_in_trans_fatty_acids: RiskFactor,
                 diet_high_in_sodium: RiskFactor,
                 low_physical_activity: RiskFactor,
                 occupational_risks: RiskFactor,
                 occupational_carcinogens: RiskFactor,
                 occupational_asthmagens: RiskFactor,
                 occupational_particulate_matter_gases_and_fumes: RiskFactor,
                 occupational_noise: RiskFactor,
                 occupational_injuries: RiskFactor,
                 occupational_ergonomic_factors: RiskFactor,
                 childhood_sexual_abuse: RiskFactor,
                 intimate_partner_violence: RiskFactor,
                 non_exclusive_breastfeeding: RiskFactor,
                 discontinued_breastfeeding: RiskFactor,
                 drug_use_dependence_and_blood_borne_viruses: RiskFactor,
                 suicide_due_to_drug_use_disorders: RiskFactor,
                 high_fasting_plasma_glucose_continuous: RiskFactor,
                 high_fasting_plasma_glucose_categorical: RiskFactor,
                 diet_low_in_calcium: RiskFactor,
                 occupational_exposure_to_asbestos: RiskFactor,
                 occupational_exposure_to_arsenic: RiskFactor,
                 occupational_exposure_to_benzene: RiskFactor,
                 occupational_exposure_to_beryllium: RiskFactor,
                 occupational_exposure_to_cadmium: RiskFactor,
                 occupational_exposure_to_chromium: RiskFactor,
                 occupational_exposure_to_diesel_engine_exhaust: RiskFactor,
                 occupational_exposure_to_formaldehyde: RiskFactor,
                 occupational_exposure_to_nickel: RiskFactor,
                 occupational_exposure_to_polycyclic_aromatic_hydrocarbons: RiskFactor,
                 occupational_exposure_to_silica: RiskFactor,
                 occupational_exposure_to_sulfuric_acid: RiskFactor,
                 intimate_partner_violence_exposure_approach: RiskFactor,
                 intimate_partner_violence_direct_paf_approach: RiskFactor,
                 all_risk_factors: RiskFactor,
                 unsafe_sex: RiskFactor,
                 intimate_partner_violence_hiv_paf_approach: RiskFactor,
                 environmental_occupational_risks: RiskFactor,
                 behavioral_risks: RiskFactor,
                 occupational_exposure_to_trichloroethylene: RiskFactor,
                 no_access_to_handwashing_facility: RiskFactor,
                 child_growth_failure: RiskFactor,
                 child_wasting: RiskFactor,
                 child_stunting: RiskFactor,
                 lead_exposure_in_blood: RiskFactor,
                 lead_exposure_in_bone: RiskFactor,
                 childhood_sexual_abuse_against_females: RiskFactor,
                 childhood_sexual_abuse_against_males: RiskFactor,
                 chewing_tobacco: RiskFactor,
                 diet_low_in_legumes: RiskFactor,
                 short_gestation_for_birth_weight: RiskFactor,
                 low_birth_weight_for_gestation: RiskFactor,
                 low_birth_weight_and_short_gestation: RiskFactor,
                 impaired_kidney_function: RiskFactor,
                 bullying_victimization: RiskFactor,
                 high_ldl_cholesterol: RiskFactor,
                 high_body_mass_index_in_adults: RiskFactor,
                 high_body_mass_index_in_children: RiskFactor,
                 particulate_matter_pollution: RiskFactor,
                 childhood_maltreatment: RiskFactor, ):
        super().__init__()
        self.unsafe_water_sanitation_and_handwashing = unsafe_water_sanitation_and_handwashing
        self.unsafe_water_source = unsafe_water_source
        self.unsafe_sanitation = unsafe_sanitation
        self.air_pollution = air_pollution
        self.ambient_particulate_matter_pollution = ambient_particulate_matter_pollution
        self.household_air_pollution_from_solid_fuels = household_air_pollution_from_solid_fuels
        self.ambient_ozone_pollution = ambient_ozone_pollution
        self.other_environmental_risks = other_environmental_risks
        self.residential_radon = residential_radon
        self.lead_exposure = lead_exposure
        self.child_and_maternal_malnutrition = child_and_maternal_malnutrition
        self.suboptimal_breastfeeding = suboptimal_breastfeeding
        self.child_underweight = child_underweight
        self.iron_deficiency = iron_deficiency
        self.vitamin_a_deficiency = vitamin_a_deficiency
        self.zinc_deficiency = zinc_deficiency
        self.tobacco = tobacco
        self.smoking = smoking
        self.secondhand_smoke = secondhand_smoke
        self.alcohol_use = alcohol_use
        self.drug_use = drug_use
        self.metabolic_risks = metabolic_risks
        self.high_fasting_plasma_glucose = high_fasting_plasma_glucose
        self.high_systolic_blood_pressure = high_systolic_blood_pressure
        self.high_body_mass_index = high_body_mass_index
        self.low_bone_mineral_density = low_bone_mineral_density
        self.dietary_risks = dietary_risks
        self.diet_low_in_fruits = diet_low_in_fruits
        self.diet_low_in_vegetables = diet_low_in_vegetables
        self.diet_low_in_whole_grains = diet_low_in_whole_grains
        self.diet_low_in_nuts_and_seeds = diet_low_in_nuts_and_seeds
        self.diet_low_in_milk = diet_low_in_milk
        self.diet_high_in_red_meat = diet_high_in_red_meat
        self.diet_high_in_processed_meat = diet_high_in_processed_meat
        self.diet_high_in_sugar_sweetened_beverages = diet_high_in_sugar_sweetened_beverages
        self.diet_low_in_fiber = diet_low_in_fiber
        self.diet_low_in_seafood_omega_3_fatty_acids = diet_low_in_seafood_omega_3_fatty_acids
        self.diet_low_in_polyunsaturated_fatty_acids = diet_low_in_polyunsaturated_fatty_acids
        self.diet_high_in_trans_fatty_acids = diet_high_in_trans_fatty_acids
        self.diet_high_in_sodium = diet_high_in_sodium
        self.low_physical_activity = low_physical_activity
        self.occupational_risks = occupational_risks
        self.occupational_carcinogens = occupational_carcinogens
        self.occupational_asthmagens = occupational_asthmagens
        self.occupational_particulate_matter_gases_and_fumes = occupational_particulate_matter_gases_and_fumes
        self.occupational_noise = occupational_noise
        self.occupational_injuries = occupational_injuries
        self.occupational_ergonomic_factors = occupational_ergonomic_factors
        self.childhood_sexual_abuse = childhood_sexual_abuse
        self.intimate_partner_violence = intimate_partner_violence
        self.non_exclusive_breastfeeding = non_exclusive_breastfeeding
        self.discontinued_breastfeeding = discontinued_breastfeeding
        self.drug_use_dependence_and_blood_borne_viruses = drug_use_dependence_and_blood_borne_viruses
        self.suicide_due_to_drug_use_disorders = suicide_due_to_drug_use_disorders
        self.high_fasting_plasma_glucose_continuous = high_fasting_plasma_glucose_continuous
        self.high_fasting_plasma_glucose_categorical = high_fasting_plasma_glucose_categorical
        self.diet_low_in_calcium = diet_low_in_calcium
        self.occupational_exposure_to_asbestos = occupational_exposure_to_asbestos
        self.occupational_exposure_to_arsenic = occupational_exposure_to_arsenic
        self.occupational_exposure_to_benzene = occupational_exposure_to_benzene
        self.occupational_exposure_to_beryllium = occupational_exposure_to_beryllium
        self.occupational_exposure_to_cadmium = occupational_exposure_to_cadmium
        self.occupational_exposure_to_chromium = occupational_exposure_to_chromium
        self.occupational_exposure_to_diesel_engine_exhaust = occupational_exposure_to_diesel_engine_exhaust
        self.occupational_exposure_to_formaldehyde = occupational_exposure_to_formaldehyde
        self.occupational_exposure_to_nickel = occupational_exposure_to_nickel
        self.occupational_exposure_to_polycyclic_aromatic_hydrocarbons = occupational_exposure_to_polycyclic_aromatic_hydrocarbons
        self.occupational_exposure_to_silica = occupational_exposure_to_silica
        self.occupational_exposure_to_sulfuric_acid = occupational_exposure_to_sulfuric_acid
        self.intimate_partner_violence_exposure_approach = intimate_partner_violence_exposure_approach
        self.intimate_partner_violence_direct_paf_approach = intimate_partner_violence_direct_paf_approach
        self.all_risk_factors = all_risk_factors
        self.unsafe_sex = unsafe_sex
        self.intimate_partner_violence_hiv_paf_approach = intimate_partner_violence_hiv_paf_approach
        self.environmental_occupational_risks = environmental_occupational_risks
        self.behavioral_risks = behavioral_risks
        self.occupational_exposure_to_trichloroethylene = occupational_exposure_to_trichloroethylene
        self.no_access_to_handwashing_facility = no_access_to_handwashing_facility
        self.child_growth_failure = child_growth_failure
        self.child_wasting = child_wasting
        self.child_stunting = child_stunting
        self.lead_exposure_in_blood = lead_exposure_in_blood
        self.lead_exposure_in_bone = lead_exposure_in_bone
        self.childhood_sexual_abuse_against_females = childhood_sexual_abuse_against_females
        self.childhood_sexual_abuse_against_males = childhood_sexual_abuse_against_males
        self.chewing_tobacco = chewing_tobacco
        self.diet_low_in_legumes = diet_low_in_legumes
        self.short_gestation_for_birth_weight = short_gestation_for_birth_weight
        self.low_birth_weight_for_gestation = low_birth_weight_for_gestation
        self.low_birth_weight_and_short_gestation = low_birth_weight_and_short_gestation
        self.impaired_kidney_function = impaired_kidney_function
        self.bullying_victimization = bullying_victimization
        self.high_ldl_cholesterol = high_ldl_cholesterol
        self.high_body_mass_index_in_adults = high_body_mass_index_in_adults
        self.high_body_mass_index_in_children = high_body_mass_index_in_children
        self.particulate_matter_pollution = particulate_matter_pollution
        self.childhood_maltreatment = childhood_maltreatment
