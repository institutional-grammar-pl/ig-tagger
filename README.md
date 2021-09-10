# [Institutional Grammar 2.0](https://arxiv.org/abs/2008.08937) annotator

Python tool for processing and tagging sentences with IG 2.0 syntax. 


# Manual

## Installation

1.  Create a virtual environment:

        python -m venv .env

2.  Activate the virtual environment:

        source .env/bin/activate

3.  Install dependencies:

        pip install -r requirements.txt or pip install -r requirements_linux.txt
        python3 -m spacy download en_core_web_sm

## Chain of tools

Possible tasks are executed as shell commands on files:

> `python ig_script.py <task_type> <input_file_path> <output_file_path> --some-additional-option`

### Split text document into sentences

Input:
>	Plain .txt file with text.
Output:
>	Plain .txt file with sentences separated by new empty lines. 
Command:
>        `python ig_script.py atomize input_text.txt sentences.txt --split_type rule_based`
About:
Complex sentences with enumerations are splitted into atomic sentences when it is possible. (xxx xxx (a) ccc, (b) vvv” -> “xxx xxx ccc”, “xxx xxx vvv”).

Split type possible values: ‘ml’, ‘rule_based’. ML variant uses special tool ([Spacy library](https://spacy.io)) for recognizing beginnings and ends of sentences in text. Rule based variant uses simple matching based on capital letter and period at the end of the sentence (regular expressions). 

These two are different aproaches and can give different results. Basic option is rule_based, but it is recommended to compare results on each use case.

Both splits recognize enumeration based on a, b, c… or 1, 2, 3… to split bigger sentences into smaller ones. Which is implemented as matching such expressions (xxx xxx (a) ccc, (b) vvv”) in sentence, then splitting and constructing new sentences from extracted parts (“xxx xxx ccc”, “xxx xxx vvv”).

### Split sentence document into constitutive/regulative
Input:
>	Plain .txt file with sentences separated by new lines.
Output:
>	.tsv file with 2 columns: ['sentence_type', 'text'].

        python ig_script.py classify sentences.txt classified_sentences.txt

### IG tagging:

        python ig_script.py tag classified_sentences_constitutive.txt tagged_constitutive.tsv --sentence_type constitutive
        python ig_script.py tag classified_sentences_regulative.txt  tagged_regulative.tsv --sentence_type regulative

4.  Merge two files:
	
	


