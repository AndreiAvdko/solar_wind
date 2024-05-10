from setuptools import setup, find_packages

setup(
    name='solar_wind',
    version='0.1',
    python_requires='>=3.8.0, <3.11.0',
    packages=find_packages(where='solar_wind'),
    package_dir={'': 'solar_wind'},
    package_data={
        # "mypkg": ["*.txt"],
        # "mypkg.data": ["*.rst"],
        'solar_wind': ['*.json'],
        'test_data_validation.test_data': ['*.csv', '*.dat'],
        'solar_wind.model': ['*.pkl'],
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
