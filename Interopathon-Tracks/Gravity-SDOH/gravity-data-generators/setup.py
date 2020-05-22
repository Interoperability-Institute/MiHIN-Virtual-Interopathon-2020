from setuptools import find_packages, setup

setup(
    name='mihin-gravity-data-generators',
    version='0.0.1',
    author='James Folkerth',
    author_email='james.folkerth@interoperabilityinstitute.org',
    description='Synthetic data generators to support Gravity SDOH connectathon scenarios',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)