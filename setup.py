from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

setup(
    name='AutoBuy',
    version='0.1.0',
    author='Yassine',
    author_github='https:github.com/fulanii',
    description='A ClI Tool that allows the automation of buying products from online ecommerce sites',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[line.strip() for line in open('requirements.txt').readlines() if not line.startswith('#')],
    entry_points={
        'console_scripts': [
            'autobuy=src.main:main'
        ]
    },
)

