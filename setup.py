from setuptools import setup, find_packages

setup(
    name='bingle',
    version='0.1.3',
    author='junhee',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'bingle': ['ai_caller/api_spec/*.json']
    },
    include_package_data=True,
    install_requires=[
        'pandas>=2.2.3',
        'pyarrow>=18.1.0',
        'numpy>=1.26.2',
        'requests>=2.32.3'
    ]
)
