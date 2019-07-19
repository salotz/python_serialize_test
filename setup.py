from setuptools import setup, find_packages

setup(
    name='serialize_test',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'numpy',
        'pandas',
        'distributed',
        'joblib',
        'dill',
        'cloudpickle',
    ],
    entry_points={
        'console_scripts' : [
            "serialize_test = serialize_test.cli:main"]}
)
