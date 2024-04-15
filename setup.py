from setuptools import setup

setup(
    name='solar_wind',
    version='0.1',
    python_requires='>=3.8.0, <3.11.0',
    packages=['your_package'],
    install_requires=[
        'etna',
        'spaceweather',
        'pandas',
        'numpy',
        'matplotlib',
        'requests',
        'pytest'
    ],
)