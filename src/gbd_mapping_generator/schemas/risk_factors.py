from pandera import DataFrameSchema, Column, Check, Index

risk_schema = DataFrameSchema(
    index=Index(int, name="rei_id",  unique=True),
    columns={
        "level": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=0.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=4.0, raise_warning=False, ignore_na=True
                ),
            ],
        ),
        "rei_name": Column(
            dtype="str",
        ),
        "parent_id": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=82.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=381.0, raise_warning=False, ignore_na=True
                ),
            ],
        ),
        "most_detailed": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=0.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1.0, raise_warning=False, ignore_na=True
                ),
            ],
        ),
        "age_specific_exp": Column(
            dtype="object",
            nullable=True,
        ),
        "exposure_type": Column(
            dtype="object",
            nullable=True,
        ),
        "female": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1.0, raise_warning=False, ignore_na=True
                ),
            ],
        ),
        "has_sev": Column(
            dtype="object",
            nullable=True,
        ),
        "inv_exp": Column(
            dtype="object",
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
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1.0, raise_warning=False, ignore_na=True
                ),
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
            dtype="object",
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
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=True,
        ),
        "yld_age_group_id_end": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=8.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=388.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=True,
        ),
        "yld_age_group_id_start": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=2.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=389.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=True,
        ),
        "yll": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=True,
        ),
        "yll_age_group_id_end": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=8.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=388.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=True,
        ),
        "yll_age_group_id_start": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=2.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=389.0, raise_warning=False, ignore_na=True
                ),
            ],
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
    coerce=True,
    strict=True,
)
