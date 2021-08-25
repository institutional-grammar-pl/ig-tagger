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

	``python ig_script.py <task_type> <input_file_path> <output_file_path>``

1. Split text document into sentences (xxx xxx (a) ccc, (b) vvv” -> “xxx xxx ccc”, “xxx xxx vvv”)::

	python ig_script.py atomize input_text.txt sentences.txt --split_type spacy
	
Split type possible values: 'spacy', 'regex'.

2. Split sentence document into constitutive/regulative files. Two new file will be created _constitutive and _regulative::

	python ig_script.py classify sentences.txt classified_sentences.txt
	
3. Tag both type of sentences::

	python ig_script.py tag classified_sentences_constitutive.txt tagged_constitutive.txt --sentence-type constitutive
	python ig_script.py tag classified_sentences_regulative.txt  tagged_regulative.txt --sentence-type regulative
	


