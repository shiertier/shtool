#setup.py
from setuptools import setup, find_packages

setup(
    name='shtool',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shsftp = shtool.shsftp:main',
            'shzip = shtool.shzip:main',
        ],
    },
    install_requires=[
        'pyzipper',
        'paramiko',
    ],
)
