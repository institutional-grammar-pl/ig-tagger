import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="igannotator",
    version="1.2.0",
    url=" ",
    license='MIT',

    author="Aleksandra Wichrowska, Karol Saputa",
    author_email=" ",

    description="Institutional Grammar 2.0 annotation package.",
    long_description=read("README.md"),

    packages=find_packages(exclude=('tests',)),

    entry_points={
        "console_scripts": [
            "ig-cli = igannotator.ig_script:main"
        ]
    },

    install_requires=[
        "stanza==1.2.2",
        "pandas==1.3.3",
        "spacy==3.1.1",
        "joblib==1.0.1",
        "scikit-learn==0.23.1"
    ],

    package_data={"igannotator": ["sentence_type_classifier.joblib"]},

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
