igannotator
===========
Institutional Grammar annotator package.

Authors
-------
New version of annotator for IG 2.0 was written as an extension to ``igannotator`` - written by the group of students during `Text Mining` course at Warsaw University of Technology.

Usage
-----

Installation (version 1 - based on virtual environment)
------------
1. Create a virtual environment::

    python -m venv .env

2. Activate the virtual environment::

    source .env/bin/activate

3. Install dependencies::

    pip install -r requirements.txt

Example 
-------

1. Run annotation for example.txt file (sentence are separated by empty line)::

	python ig_annotator.py data/example.txt data/example.tsv en tsv
