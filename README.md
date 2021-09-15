# Institutional Grammar 2.0 annotator

# About
Python tool for processing and tagging sentences with [IG 2.0 syntax](https://arxiv.org/abs/2008.08937) with additional tools for text cleaning, preprocessing and postprocessing. 

# Contributions

The tool is based on the results of previous work on Institutional Grammar annotation:
1. Group project for the previous version of IG syntax and Polish language - [link](https://github.com/rzepinskip/ig-annotator) 
2. Work by Aleksandra Wichrowska on developing rules for English language and new IG 2.0 syntax - [link](https://github.com/airi314/annotator/tree/master)


# Manual

The package can be used within `import igannotator` with object-oriented operations included in `igannotator.backend` and file operations included in `igannotator.frontend`. 

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
```


## Chain of command-line tools **ig-cli**

Possible tasks are executed as shell commands on files:

```
ig-cli <task_type> <input_file_path> <output_file_path> --some-additional-option
```

### Help
To show information about possible commands, arguments and options execute:
```
ig-cli -h
```

----------------------------------------------------------

### Split text document into sentences

**Input**:

Plain .txt file with text.

**Output**:
	
Plain .txt file with sentences separated by new empty lines. 

**Command**:
```
ig-cli atomize input_text.txt sentences.txt --split_type rule_based
```

**About**:

Complex sentences with enumerations are splitted into atomic sentences when it is possible. (xxx xxx (a) ccc, (b) vvv” -> “xxx xxx ccc”, “xxx xxx vvv”).

Split type possible values: ‘ml’, ‘rule_based’. ML variant uses  a special tool ([Spacy library](https://spacy.io)) for recognizing the beginnings and ends of sentences in text. Rule-based variant uses simple matching based on capital letter and period at the end of the sentence (regular expressions). 

These two are different approaches and can give different results. The basic option is rule_based, but it is recommended to compare results on each use case.

Both splits recognize enumeration based on a, b, c… or 1, 2, 3… to split bigger sentences into smaller ones. Which is implemented as matching such expressions (xxx xxx (a) ccc, (b) vvv”) in the sentence, then splitting and constructing new sentences from extracted parts (“xxx xxx ccc”, “xxx xxx vvv”).

----------------------------------------------------------

### Assign sentence type
**Input**:

Plain .txt file with sentences separated by new lines.

**Output**:

.tsv file with 2 columns: ['sentence_type', 'text'].

**Command**:
```
ig-cli classify sentences.txt classified_sentences.txt
```

**About**:

Sentences are classified as regulative (`r`) or constitutive (`c`). For this purpose, simple ML model is prepared trained on a small annotated dataset. The output file should be reviewed and corrected manually.

[The ML model](https://github.com/institutional-grammar-pl/policydemic-annotator/blob/rc_07_2021/sentence_type_classifier.joblib) can be changed/retrained as a new file with serialized Python object with `.predict(self, sentences: List[str]) -> List[bool]` method and returns True for regulative sentences. Corrected files can be gathered for building better classifier.

----------------------------------------------------------

### IG tagging:
**Input**:

.tsv file with 3 columns ['sentence no.', text, 'sentence_type'] compatible with results of `classify` command.

**Output**:

.tsv file with tagged sentences

**Command**:
```
ig-cli tag classified_sentences.txt tagged_sentences.tsv
```
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
	
### Comparison of results
Comparison between files (e.g. for quality/error assessment) is possible via other tools such as (`diff` - command line tool, [diffchecker](https://www.diffchecker.com) - web tool)

