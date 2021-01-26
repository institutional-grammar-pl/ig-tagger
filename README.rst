policydemic-annotator
===========
Institutional Grammar annotator package.

New version of annotator for IG 2.0 was written as a part of diploma thesis.
It is an extension to ``igannotator`` - written by the group of students during `Text Mining` course at Warsaw University of Technology.

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

	python main.py data/example.txt data/example.tsv reg

Description of parameters
-------

* ``input``  - path to input file. Sentences in this file should be separated by empty line.

* ``output`` - path to output file

* ``layer`` - which IG layers should be used in annotation. Values 'reg', 'cons' and 'both' are allowed. Default: 'both'.

* ``conllu_path`` - if specified then conllu file will be saved to this path. Default: 'None'

