from setuptools import setup, find_packages

setup(
    name='solar_wind',
    version='0.1',
    python_requires='>=3.8.0, <3.11.0',
    packages=find_packages(),
    package_data={
        '': ['*.json', '*.dat', '*.csv']
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
