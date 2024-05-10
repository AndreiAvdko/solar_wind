from setuptools import setup, find_packages

setup(
    name='solar_wind',
    version='0.1',
    python_requires='>=3.8.0, <3.11.0',
    packages=find_packages(),
    package_data={
        '': ['*.json', '*.dat', '*.csv'],
        'test_data_validation': ['test_data/*.json', 'test_data/*.dat', 'test_data/*.csv'],
    },
    # package_dir={"": "solar_wind "}, возникает ошибка

    include_package_data=True,
    install_requires=[
        'etna',
        'etna[auto]',
        'spaceweather',
        'pandas',
        'numpy',
        'matplotlib',
        'requests',
        'pytest'
    ],
)
