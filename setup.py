from setuptools import setup, find_packages

setup(
    name="feuille",
    version="0.1",
    author="FeuilleDev",
    description="The official Feuille CLI",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'feuille=feuille.feuille:main',
        ],
    },
    install_requires=[],
)
