from setuptools import setup, find_packages

setup(
    name = "filedrop",
    version = "0.1",
    url = 'http://code.penny-arcade.com/projects/filedrop',
    license = 'MIT',
    description = "A file drop off / pickup service",
    author = 'Erik Karulf',
    # Below this line is tasty Kool-Aide provided by the Cargo Cult
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)