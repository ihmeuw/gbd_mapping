"""Mapping templates for GBD etiologies.

This code is automatically generated by gbd_mapping_generator/risk_builder.py

Any manual changes will be lost.
"""
from typing import Tuple

from .id import reiid
from .base_template import ModelableEntity, GbdRecord, Levels, Tmred, ExposureParameters, Restrictions
from .cause_template import Cause


class Risk(ModelableEntity):
    """Container for risk GBD ids and metadata."""
    __slots__ = ('name', 'kind', 'gbd_id', 'distribution', 'affected_causes', 'restrictions', 'levels', 'tmred',
                 'exposure_parameters', )

    def __init__(self,
                 name: str,
                 kind: str,
                 gbd_id: reiid,
                 distribution: str,
                 affected_causes: Tuple[Cause, ...],
                 restrictions: Restrictions,
                 levels: Levels = None,
                 tmred: Tmred = None,
                 exposure_parameters: ExposureParameters = None, ):
        super().__init__(name=name,
                         kind=kind,
                         gbd_id=gbd_id)
        self.name = name
        self.kind = kind
        self.gbd_id = gbd_id
        self.distribution = distribution
        self.affected_causes = affected_causes
        self.restrictions = restrictions
        self.levels = levels
        self.tmred = tmred
        self.exposure_parameters = exposure_parameters


class Risks(GbdRecord):
    """Container for GBD risks."""
    __slots__ = ('unsafe_water_source', 'unsafe_sanitation', 'ambient_particulate_matter_pollution',
                 'household_air_pollution_from_solid_fuels', 'ambient_ozone_pollution', 'residential_radon',
                 'child_underweight', 'iron_deficiency', 'vitamin_a_deficiency', 'zinc_deficiency',
                 'secondhand_smoke', 'alcohol_use', 'high_total_cholesterol', 'high_systolic_blood_pressure',
                 'high_body_mass_index', 'low_bone_mineral_density', 'diet_low_in_fruits', 'diet_low_in_vegetables',
                 'diet_low_in_whole_grains', 'diet_low_in_nuts_and_seeds', 'diet_low_in_milk',
                 'diet_high_in_red_meat', 'diet_high_in_processed_meat', 'diet_high_in_sugar_sweetened_beverages',
                 'diet_low_in_fiber', 'diet_low_in_seafood_omega_3_fatty_acids',
                 'diet_low_in_polyunsaturated_fatty_acids', 'diet_high_in_trans_fatty_acids', 'diet_high_in_sodium',
                 'low_physical_activity', 'occupational_asthmagens',
                 'occupational_particulate_matter_gases_and_fumes', 'occupational_noise', 'occupational_injuries',
                 'occupational_ergonomic_factors', 'non_exclusive_breastfeeding', 'discontinued_breastfeeding',
                 'drug_use_dependence_and_blood_borne_viruses', 'suicide_due_to_drug_use_disorders',
                 'high_fasting_plasma_glucose_continuous', 'high_fasting_plasma_glucose_categorical',
                 'diet_low_in_calcium', 'occupational_exposure_to_asbestos', 'occupational_exposure_to_arsenic',
                 'occupational_exposure_to_benzene', 'occupational_exposure_to_beryllium',
                 'occupational_exposure_to_cadmium', 'occupational_exposure_to_chromium',
                 'occupational_exposure_to_diesel_engine_exhaust', 'occupational_exposure_to_secondhand_smoke',
                 'occupational_exposure_to_formaldehyde', 'occupational_exposure_to_nickel',
                 'occupational_exposure_to_polycyclic_aromatic_hydrocarbons', 'occupational_exposure_to_silica',
                 'occupational_exposure_to_sulfuric_acid', 'smoking_sir_approach', 'smoking_prevalence_approach',
                 'intimate_partner_violence_exposure_approach', 'intimate_partner_violence_direct_paf_approach',
                 'unsafe_sex', 'intimate_partner_violence_hiv_paf_approach',
                 'occupational_exposure_to_trichloroethylene', 'no_access_to_handwashing_facility', 'child_wasting',
                 'child_stunting', 'lead_exposure_in_blood', 'lead_exposure_in_bone',
                 'childhood_sexual_abuse_against_females', 'childhood_sexual_abuse_against_males',
                 'smokeless_tobacco', 'diet_low_in_legumes', 'low_birth_weight_and_short_gestation',
                 'impaired_kidney_function', )

    def __init__(self,
                 unsafe_water_source: Risk,
                 unsafe_sanitation: Risk,
                 ambient_particulate_matter_pollution: Risk,
                 household_air_pollution_from_solid_fuels: Risk,
                 ambient_ozone_pollution: Risk,
                 residential_radon: Risk,
                 child_underweight: Risk,
                 iron_deficiency: Risk,
                 vitamin_a_deficiency: Risk,
                 zinc_deficiency: Risk,
                 secondhand_smoke: Risk,
                 alcohol_use: Risk,
                 high_total_cholesterol: Risk,
                 high_systolic_blood_pressure: Risk,
                 high_body_mass_index: Risk,
                 low_bone_mineral_density: Risk,
                 diet_low_in_fruits: Risk,
                 diet_low_in_vegetables: Risk,
                 diet_low_in_whole_grains: Risk,
                 diet_low_in_nuts_and_seeds: Risk,
                 diet_low_in_milk: Risk,
                 diet_high_in_red_meat: Risk,
                 diet_high_in_processed_meat: Risk,
                 diet_high_in_sugar_sweetened_beverages: Risk,
                 diet_low_in_fiber: Risk,
                 diet_low_in_seafood_omega_3_fatty_acids: Risk,
                 diet_low_in_polyunsaturated_fatty_acids: Risk,
                 diet_high_in_trans_fatty_acids: Risk,
                 diet_high_in_sodium: Risk,
                 low_physical_activity: Risk,
                 occupational_asthmagens: Risk,
                 occupational_particulate_matter_gases_and_fumes: Risk,
                 occupational_noise: Risk,
                 occupational_injuries: Risk,
                 occupational_ergonomic_factors: Risk,
                 non_exclusive_breastfeeding: Risk,
                 discontinued_breastfeeding: Risk,
                 drug_use_dependence_and_blood_borne_viruses: Risk,
                 suicide_due_to_drug_use_disorders: Risk,
                 high_fasting_plasma_glucose_continuous: Risk,
                 high_fasting_plasma_glucose_categorical: Risk,
                 diet_low_in_calcium: Risk,
                 occupational_exposure_to_asbestos: Risk,
                 occupational_exposure_to_arsenic: Risk,
                 occupational_exposure_to_benzene: Risk,
                 occupational_exposure_to_beryllium: Risk,
                 occupational_exposure_to_cadmium: Risk,
                 occupational_exposure_to_chromium: Risk,
                 occupational_exposure_to_diesel_engine_exhaust: Risk,
                 occupational_exposure_to_secondhand_smoke: Risk,
                 occupational_exposure_to_formaldehyde: Risk,
                 occupational_exposure_to_nickel: Risk,
                 occupational_exposure_to_polycyclic_aromatic_hydrocarbons: Risk,
                 occupational_exposure_to_silica: Risk,
                 occupational_exposure_to_sulfuric_acid: Risk,
                 smoking_sir_approach: Risk,
                 smoking_prevalence_approach: Risk,
                 intimate_partner_violence_exposure_approach: Risk,
                 intimate_partner_violence_direct_paf_approach: Risk,
                 unsafe_sex: Risk,
                 intimate_partner_violence_hiv_paf_approach: Risk,
                 occupational_exposure_to_trichloroethylene: Risk,
                 no_access_to_handwashing_facility: Risk,
                 child_wasting: Risk,
                 child_stunting: Risk,
                 lead_exposure_in_blood: Risk,
                 lead_exposure_in_bone: Risk,
                 childhood_sexual_abuse_against_females: Risk,
                 childhood_sexual_abuse_against_males: Risk,
                 smokeless_tobacco: Risk,
                 diet_low_in_legumes: Risk,
                 low_birth_weight_and_short_gestation: Risk,
                 impaired_kidney_function: Risk, ):
        super().__init__()
        self.unsafe_water_source = unsafe_water_source
        self.unsafe_sanitation = unsafe_sanitation
        self.ambient_particulate_matter_pollution = ambient_particulate_matter_pollution
        self.household_air_pollution_from_solid_fuels = household_air_pollution_from_solid_fuels
        self.ambient_ozone_pollution = ambient_ozone_pollution
        self.residential_radon = residential_radon
        self.child_underweight = child_underweight
        self.iron_deficiency = iron_deficiency
        self.vitamin_a_deficiency = vitamin_a_deficiency
        self.zinc_deficiency = zinc_deficiency
        self.secondhand_smoke = secondhand_smoke
        self.alcohol_use = alcohol_use
        self.high_total_cholesterol = high_total_cholesterol
        self.high_systolic_blood_pressure = high_systolic_blood_pressure
        self.high_body_mass_index = high_body_mass_index
        self.low_bone_mineral_density = low_bone_mineral_density
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
        self.occupational_asthmagens = occupational_asthmagens
        self.occupational_particulate_matter_gases_and_fumes = occupational_particulate_matter_gases_and_fumes
        self.occupational_noise = occupational_noise
        self.occupational_injuries = occupational_injuries
        self.occupational_ergonomic_factors = occupational_ergonomic_factors
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
        self.occupational_exposure_to_secondhand_smoke = occupational_exposure_to_secondhand_smoke
        self.occupational_exposure_to_formaldehyde = occupational_exposure_to_formaldehyde
        self.occupational_exposure_to_nickel = occupational_exposure_to_nickel
        self.occupational_exposure_to_polycyclic_aromatic_hydrocarbons = occupational_exposure_to_polycyclic_aromatic_hydrocarbons
        self.occupational_exposure_to_silica = occupational_exposure_to_silica
        self.occupational_exposure_to_sulfuric_acid = occupational_exposure_to_sulfuric_acid
        self.smoking_sir_approach = smoking_sir_approach
        self.smoking_prevalence_approach = smoking_prevalence_approach
        self.intimate_partner_violence_exposure_approach = intimate_partner_violence_exposure_approach
        self.intimate_partner_violence_direct_paf_approach = intimate_partner_violence_direct_paf_approach
        self.unsafe_sex = unsafe_sex
        self.intimate_partner_violence_hiv_paf_approach = intimate_partner_violence_hiv_paf_approach
        self.occupational_exposure_to_trichloroethylene = occupational_exposure_to_trichloroethylene
        self.no_access_to_handwashing_facility = no_access_to_handwashing_facility
        self.child_wasting = child_wasting
        self.child_stunting = child_stunting
        self.lead_exposure_in_blood = lead_exposure_in_blood
        self.lead_exposure_in_bone = lead_exposure_in_bone
        self.childhood_sexual_abuse_against_females = childhood_sexual_abuse_against_females
        self.childhood_sexual_abuse_against_males = childhood_sexual_abuse_against_males
        self.smokeless_tobacco = smokeless_tobacco
        self.diet_low_in_legumes = diet_low_in_legumes
        self.low_birth_weight_and_short_gestation = low_birth_weight_and_short_gestation
        self.impaired_kidney_function = impaired_kidney_function