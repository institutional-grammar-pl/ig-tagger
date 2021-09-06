policydemic-annotator
===========
Institutional Grammar annotator package.

Usage
-----

Installation
------------
1. Create a virtual environment::

    python -m venv .env

2. Activate the virtual environment::

    source .env/bin/activate

3. Install dependencies::

    pip install -r requirements.txt or pip install -r requirements_linux.txt
    python3 -m spacy download en_core_web_sm

Usage
-------

	``python ig_script.py <task_type> <input_file_path> <output_file_path>``

1. Split text document into sentences (xxx xxx (a) ccc, (b) vvv” -> “xxx xxx ccc”, “xxx xxx vvv”)::

	python ig_script.py atomize input_text.txt sentences.txt --split_type spacy
	
Split type possible values: 'spacy', 'regex'. Spacy variant uses special tool (Spacy library) for recognizing beginings and ends of sentences in text. Regex variant uses simple matching based on capital letter and period at the end of the sentence (Regular expressions). These two are different aproaches and can give different results. Basic option is regex, but the idea is to compare results during real work.

Both splits recognizer enumeration based on a, b, c... or 1, 2, 3... to split bigger sentences into smaller ones. Which is  implemented as matching such expressions (xxx xxx (a) ccc, (b) vvv” -> “xxx xxx ccc”, “xxx xxx vvv”) in sentence, then splitting and constructing new sentences from extracted parts.

2. Split sentence document into constitutive/regulative files. Two new file will be created _constitutive and _regulative::

	python ig_script.py classify sentences.txt classified_sentences.txt
	
3. Tag both type of sentences::

	python ig_script.py tag classified_sentences_constitutive.txt tagged_constitutive.txt --sentence_type constitutive
	python ig_script.py tag classified_sentences_regulative.txt  tagged_regulative.txt --sentence_type regulative
	
4. Merge two files::

	
	


