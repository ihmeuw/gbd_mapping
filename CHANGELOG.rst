**3.0.4 - 02/15/22**

 - Autoformat code with black and isort.
 - Add black and isort checks to CI.

**3.0.3 - 02/12/22**

 - Bugfix in risk data access.
 - Modernize CI.
 - Squash warnings in doc building
 - Fix remote doc builds.
 - Rebuild mappings.

**3.0.2 - 5/21/21**

 - Bugfix: update for gbd_access dependency

**3.0.1 - 1/6/21**

 - Bugfix: don't install extras

**3.0.0 - 1/5/21**

 - Update to GBD 2019
 
**2.1.0 - 11/18/19**

 - Be consistent about rate names.

**2.0.4 - 06/18/19**

 - Add CI script to handle upstream dependencies properly.
 - Update metadata.

**2.0.3 - 04/09/19**

 - Remove incorrect risk categories from previous GBD rounds.

**2.0.2 - 02/24/19**

 - Remove unused coverage gaps.
 - Have coverage gap inherit from modelable entity.
 - Use sorted list for coverage gaps to fix order.

**2.0.1 - 02/14/19**

 - Update dependencies.

**2.0.0 - 02/11/19**

 - Update all cause, covariate, coverage_gap, etiology and risk_factor mappings
   to include the GBD 2017 metadata.
 - Update all the mappings to include the gbd_summary results.
 - Rename risk as risk_factor.
 - Fix the recursion and nan errors.

**1.0.13 - 01/04/19**

 - Remove covariate flag.
 - Add CI branch synchronization

**1.0.12 - 12/7/18**

 - Add coverage_gap of lack_of_eggs

**1.0.11 - 11/28/18**

 - Add non_exclusive_breastfeeding relative risk to lack_of_breastfeeding_promotion

**1.0.10 - 11/15/18**

 - Documentation dependency update.

**1.0.9 - 11/13/18**

 - Add coverage_gap of lack_of_vitamin_a_fortification

**1.0.8 - 10/26/18**

 - Add a ``kind`` field to entities.
 - Update covariates and coverage gaps mappings
 - Remove HealthcareEntity
 - Unpin click version

**1.0.7 - 10/12/18**

 - Change setup.py
 - Add coverage_gap of lack_of_immediate_assessment_and_stimulation exposure
 - Add coverage_gap of lack_of_immediate_assessment_and_stimulation relative risk to (neonatal_preterm_birth_complications)

**1.0.6 - 10/12/18**

 - Fix requirements.txt (add the click version)

**1.0.5 - 09/12/18**

 - Add coverage_gap of lack_of_breastfeeding_promotion exposure
 - Add coverage_gap of lack_of_lipid_lowering_therapy exposure

**1.0.4 - 09/06/18**

 - Remove none from causes
 - Change risks to risk_factors
 - Make coverage_gap available

**1.0.3 - 08/22/18**

 - Use __about__ in docs
 - Split gbd_access into a separate package
 - Removing lingering paths
 - Fix GbdRecord.to_dict
 - Update auxiliary data calls
 - Add measles

**1.0.2 - 07/26/18**

 - Fix deployment issues

**1.0.0 - 07/25/18**

 - Initial release
