from setuptools import setup, find_packages

setup(
    name="bevos",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==6.7",
        "requests==2.13.0",
        "semantic_version==2.6.0"
    ],
    entry_points='''
        [console_scripts]
        bevos=bevos.main:cli
    '''
)
