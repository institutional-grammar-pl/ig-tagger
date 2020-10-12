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

Installation (version 2 - based on python package)
------------
1. Add execution rights for building script::

    chmod +x ./build.sh

2. Run build script::

    ./build.sh

Example 
-------

1. Run annotation for example (sentence are separated by empty line)::

    python ig_annotator.py data/simple_example.txt simple_example-ouput.xml

2. Run annotation for `nauka_1.txt` file::

    python stanfordForGoldStandard.py 

3. If you have installed ``igannotator`` as python package there is an option to run tool directly from CLI::

    ig_annotator INPUT OUTPUT
