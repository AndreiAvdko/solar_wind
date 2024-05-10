from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='solar_wind',
    version='0.1',
    python_requires='>=3.8.0, <3.11.0',
    packages=find_namespace_packages(),
    # package_dir={"": "solar_wind"}, возникает ошибка
    include_package_data=True,
    package_data={
        '': ['*.json', '*.dat', '*.csv'],
        'test_data_validation.test_data.correct_timestamps': ['*.csv'],
    },
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
