# [Institutional Grammar 2.0](https://arxiv.org/abs/2008.08937) annotator

Python tool for processing and tagging sentences with IG 2.0 syntax. 


# Manual

## Installation

1.  Create a virtual environment:
>	python -m venv .env

2.  Activate the virtual environment:

>	source .env/bin/activate

3.  Install dependencies:

>	pip install -r requirements.txt or pip install -r requirements_linux.txt
>       python3 -m spacy download en_core_web_sm

## Chain of tools

Possible tasks are executed as shell commands on files:

>	python ig_script.py <task_type> <input_file_path> <output_file_path> --some-additional-option

### Split text document into sentences

**Input**:

Plain .txt file with text.

**Output**:
	
Plain .txt file with sentences separated by new empty lines. 

**Command**:
>	python ig_script.py atomize input_text.txt sentences.txt --split_type rule_based

**About**:

Complex sentences with enumerations are splitted into atomic sentences when it is possible. (xxx xxx (a) ccc, (b) vvv” -> “xxx xxx ccc”, “xxx xxx vvv”).

Split type possible values: ‘ml’, ‘rule_based’. ML variant uses special tool ([Spacy library](https://spacy.io)) for recognizing beginnings and ends of sentences in text. Rule based variant uses simple matching based on capital letter and period at the end of the sentence (regular expressions). 

These two are different aproaches and can give different results. Basic option is rule_based, but it is recommended to compare results on each use case.

Both splits recognize enumeration based on a, b, c… or 1, 2, 3… to split bigger sentences into smaller ones. Which is implemented as matching such expressions (xxx xxx (a) ccc, (b) vvv”) in sentence, then splitting and constructing new sentences from extracted parts (“xxx xxx ccc”, “xxx xxx vvv”).

### Assign sentence type
**Input**:

Plain .txt file with sentences separated by new lines.

**Output**:

.tsv file with 2 columns: ['sentence_type', 'text'].

**Command**:

>	python ig_script.py classify sentences.txt classified_sentences.txt

**About**:

Sentences are classified as regulative (`r`) or constitutive (`c`). For this purpose simple ML model is prepared trained on small annotated dataset. Output file should be reviewed and corrected manually.

[The ML model](https://github.com/institutional-grammar-pl/policydemic-annotator/blob/rc_07_2021/sentence_type_classifier.joblib) can be changed/retrained as a new file with serialized Python object with `.predict(sentences: List[str]) -> List[bool]` method and returns True for regulative sentences. Corrected files can be gathered for building better  classifier.

### IG tagging:
Input:
>
Output:
>
Command:
>	python ig_script.py tag classified_sentences_constitutive.txt tagged_constitutive.tsv
About:


### Conversion to horizontal Excel format of IG document
Input:
>
Output:
>
Command:
>	
About:	
	


