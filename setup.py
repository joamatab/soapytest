from distutils.core import setup


setup(
    name='soapytest',
    packages=[  'soapytest',
                'soapytest.wfs',
                'soapytest.atmosphere',
                'soapytest.plotting'],
    description='Tests agaisnt theory of the Soapy AO simulation',
    long_description=open('README.md').read(),
)
