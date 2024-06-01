from setuptools import setup, find_namespace_packages

setup(
    name='solar_wind',
    version='0.1',
    python_requires='>=3.8.0, <3.11.0',
    packages=find_namespace_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json', '*.dat', '*.csv', '*.zip'],
    },
    install_requires=[
        'etna',
        'etna[auto]',
        'spaceweather',
        'pandas',
        'numpy',
        'matplotlib==3.5.2',
        'requests',
        'pytest'
    ],
)
