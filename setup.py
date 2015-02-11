try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'NBA GBling',
    'author': 'mdhart',
    'author_email': 'mattdhart@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['nba'],
    'include_package_data': True,
    'scripts': [],
    'name': 'nba'
}

setup(**config)

