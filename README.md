# Institutional Grammar 2.0 annotator
[![PyPI Latest Release](https://img.shields.io/pypi/v/igannotator.svg)](https://pypi.org/project/igannotator/)

# About
Python tool for processing and tagging sentences with [IG 2.0 syntax](https://arxiv.org/abs/2008.08937) with additional tools for text cleaning, preprocessing and postprocessing. 


# Manual

## Installation

1. Create a virtual environment:

```
python -m venv .env
```
2. Activate the virtual environment:
```
source .env/bin/activate
```

3. Install package
```  
python -m pip install --upgrade pip
python -m pip install igannotator
ig-cli
```


## Chain of command-line tools **ig-cli**

Possible tasks are executed as shell commands on files:

```
ig-cli <task_type> <input_file_path> -o output_file_path --some-additional-option
```

### Help
To show information about possible commands, arguments and options execute:
```
ig-cli -h
```

----------------------------------------------------------

### Split text document into sentences

**Input**:

Plain **.txt** file with text.

**Output**:
	
Plain **.txt** file with sentences separated by new empty lines or **.tsv** file with ['sentence no.', 'sentence_type', 'text'] columns
(with optional parameter `--format=tsv`)

**Command**:
```
ig-cli atomize input_text.txt
ig-cli atomize input_text.txt sentences.txt --split_type ml
ig-cli atomize input_text.txt --format txt
```

**Optional parameters**

* --format (txt/tsv)
* --output_file_path 
* --split_type (ml/rule_based)

**About**:

Complex sentences with enumerations are splitted into atomic sentences when it is possible. (xxx xxx (a) ccc, (b) vvv” -> “xxx xxx ccc”, “xxx xxx vvv”).

Split type possible values: ‘ml’, ‘rule_based’. ML variant uses  a special tool ([Spacy library](https://spacy.io)) for recognizing the beginnings and ends of sentences in text. Rule-based variant uses simple matching based on capital letter and period at the end of the sentence (regular expressions). 

These two are different approaches and can give different results. The basic option is rule_based, ml can do better with lower quality text because of considering whole sentence structure (not only dots and capital letters).

Both splits recognize enumeration based on a, b, c… or 1, 2, 3… to split bigger sentences into smaller ones. Which is implemented as matching such expressions (xxx xxx (a) ccc, (b) vvv”) in the sentence, then splitting and constructing new sentences from extracted parts (“xxx xxx ccc”, “xxx xxx vvv”). 

For example:

 1. The employee is subject to  (1) a Federal quarantine order related to COVID-19 (2) a Federal isolation order related to COVID-19.

 2. The employee is subject to a Federal quarantine order related to COVID-19.

 3. The employee is subject to a Federal isolation order related to COVID-19.

Sentences 2-3 are extracted from sentence 1 based on `(1) (2)` pattern.


----------------------------------------------------------

### Assign sentence type
**Input**:

Plain **.txt** file with sentences separated by new lines or **.tsv** file with 3 columns ['sentence no.', 'sentence_type', 'text']. (Based on file extension)

**Output**:

**.tsv** file with 3 columns: ['sentence no.', 'sentence_type', 'text'].

**Command**:
```
ig-cli classify sentences.tsv
```

**Optional parameters**

* --output_file_path 

**About**:

Sentences are classified as regulative (`r`) or constitutive (`c`). For this purpose, simple ML model is prepared trained on a small annotated dataset. The output file should be reviewed and corrected manually.


----------------------------------------------------------

### IG tagging:
**Input**:

.tsv file with 3 columns ['sentence no.', text, 'sentence_type'] compatible with results of `classify` command.

**Output**:

.tsv file with tagged sentences

**Command**:
```
ig-cli tag classified_sentences.tsv tagged_sentences.tsv
```

**Optional parameters**

* --output_file_path 


**About**:

Tagging is based on natural language processing with linguistic features recognition
and rules constructed for mapping linguistic features to Institutional Grammar tags.
Every sentence is analysed accordingly then results are saved with tags corresponding to each word token.

----------------------------------------------------------

### Conversion to horizontal Excel format of IG document  (in the future)
**Input**:
>
**Output**:
>
**Command**:
>	
**About**:	

----------------------------------------------------------
	
## Comparison of results
Comparison between files (e.g. for quality/error assessment) is possible via other tools such as (`diff` - command line tool (use `diff -h` for detailed instruction), [diffchecker](https://www.diffchecker.com) - web tool)

## Technical information

### Update of models
* **Sentence type classification** - [The ML model](https://github.com/institutional-grammar-pl/policydemic-annotator/blob/master/igannotator/sentence_type_classifier.joblib) can be changed/retrained as a new file with serialized Python object with `.predict(self, sentences: List[str]) -> List[bool]` method and returns True for regulative sentences. Corrected files can be gathered for building better classifier.

### Programming interface

The package can be used within `import igannotator` with object-oriented operations included in `igannotator.backend` and file operations included in `igannotator.frontend`. 
```
from igannotator import backend
backend.get_annotated_sentences(df)
```


# Contributions

The tool is based on the results of previous work on Institutional Grammar annotation:
1. Group project for the previous version of IG syntax and Polish language - [link](https://github.com/rzepinskip/ig-annotator) 
2. Work by Aleksandra Wichrowska on developing rules for English language and new IG 2.0 syntax - [link](https://github.com/airi314/annotator/tree/master)
3. Work by Karolina Seweryn on ML models: constitutive/regulative classification