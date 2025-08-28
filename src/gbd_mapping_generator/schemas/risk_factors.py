from pandera import DataFrameSchema, Column, Check, Index

risk_schema = DataFrameSchema(
    index=Index(int, name="rei_id",  unique=True),
    columns={
        "level": Column(
            dtype="int64",
            checks=[
                Check.between(0, 4)
            ],
        ),
        "rei_name": Column(
            dtype="str",
        ),
        "parent_id": Column(
            dtype="int64",
        ),
        "most_detailed": Column(
            dtype="int64",
            checks=[
                Check.isin([0, 1])
            ],
        ),
        "age_specific_exp": Column(
            dtype="object",
            checks=[
                Check.isin(['0', '1'])
            ],
            nullable=True,
        ),
        "exposure_type": Column(
            dtype="str",
            nullable=True,
        ),
        "female": Column(
            dtype="int64",
            checks=[
                Check.isin([0, 1])
            ],
        ),
        "has_sev": Column(
            dtype="object",
            checks=[
                Check.isin(['0', '1'])
            ],
            nullable=True,
        ),
        "inv_exp": Column(
            dtype="object",
            checks=[
                Check.isin(['0', '1'])
            ],
            nullable=True,
        ),
        "lancet_label": Column(
            dtype="str",
        ),
        "lancet_label_short": Column(
            dtype="str",
        ),
        "male": Column(
            dtype="float64",
            checks=[
                Check.isin([0, 1])
            ],
            nullable=True,
        ),
        "rei_calculation_type": Column(
            dtype="str",
        ),
        "rr_scalar": Column(
            dtype="object",
            nullable=True,
        ),
        "rrmax_at_sequela_level": Column(
            dtype="object",
            nullable=True,
        ),
        "rrmax_from_parent_rei": Column(
            dtype="object",
            nullable=True,
        ),
        "tmred_dist": Column(
            dtype="str",
            nullable=True,
        ),
        "tmrel_lower": Column(
            dtype="object",
            nullable=True,
        ),
        "tmrel_upper": Column(
            dtype="object",
            nullable=True,
        ),
        "unit": Column(
            dtype="str",
            nullable=True,
        ),
        "yld": Column(
            dtype="float64",
            checks=[
                Check.isin([0, 1])
            ],
            nullable=True,
        ),
        "yld_age_group_id_end": Column(
            dtype="float64",
            nullable=True,
        ),
        "yld_age_group_id_start": Column(
            dtype="float64",
            nullable=True,
        ),
        "yll": Column(
            dtype="float64",
            checks=[
                Check.isin([0, 1])
            ],
            nullable=True,
        ),
        "yll_age_group_id_end": Column(
            dtype="float64",
            nullable=True,
        ),
        "yll_age_group_id_start": Column(
            dtype="float64",
            nullable=True,
        ),
        "paf_of_one_cause_ids": Column(
            dtype="object",
            nullable=True,
        ),
        "affected_cause_ids": Column(
            dtype="object",
        ),
        "category_map": Column(
            dtype="object",
            nullable=True,
        ),
        "affected_rei_ids": Column(
            dtype="object",
            nullable=True,
        ),
    },

    strict=True,
)
