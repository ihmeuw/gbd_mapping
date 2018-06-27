from setuptools import setup, find_packages

setup(
    name='gbd_mapping',
    version='0.5',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'click',
    ],
    entry_points="""
        [console_scripts]
        build_mapping=gbd_mapping_generator.build_mapping:build_mapping
    """,
)
