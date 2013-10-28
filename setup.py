from setuptools import setup

setup(
    name='stillson',
    version='0.1.0',
    author='Mortar Data',
    author_email='info@mortardata.com',
    packages=['stillson'],
    scripts=['stillson/stillson.py'],
    url='http://pypi.python.org/pypi/stillson/',
    license='LICENSE',
    description='Tool for generating config files using a template and environment variables.',
    long_description=open('README.md').read(),
    install_requires=[
        "mako >= 0.8.0",
    ],
)
