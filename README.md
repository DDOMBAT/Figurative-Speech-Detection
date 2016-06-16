# Figurative-Speech-Detection
Experiments extracting semantic information from the WordNet


Installation: 
-------------- 

pip install -r requirements.txt 

About: 
--------------
Using the semantic relationships between entries in the wordnet to 
to extract semantic relationships between synset entries. This work is meant to
serve as a proof of concept of how strengthening the wordnet in terms  of accuracy 
and vastness can be beneficial to provide researchers/developers with more 
information about simple semantic relationships between objects in simple phrases.

As with all Knowledge Bases, the inference of this system is limited by the 
totality of it's own enumeration. In other words, I cannot make inferences about 
terms that are not in the WordNet. In addition, all the inferences made my program are 
not necessarily correct semantically.

I am using the wordnet to detect simple examples of 
figurative speech. 

How it works:

Grammar: NP1 + conj('is') + NP2 

Examples 
----------


A car is a motor vehicle  -> fact   
A vehicle is a car  -> a false overgeneralization 
Love is war -> figurative speech



Definitions 
--------------

Fact 

If NP2 is a direct Hypernym of NP1

Falsehood 

If NP1 is a direct Hypernym of NP2

Generalization 

An indirect hypernym and fact or falsehood 

Figurative 

Two Wordnet entries with non-common roots 


Factors limiting the  semantic relationships between entries in the wordnet: 
---------------------------------------

-The accuracy of Pattern's POS Tagger   

i.e. (love is a nutrient) 

Parse tree: [Sentence('Love/NN/B-NP/O is/VBZ/B-VP/O a/DT/O/O nutrient/JJ/B-ADJP/O')]

-limited by entries in WordNet 

i.e. (entries not in WordNet)

-No support for pronouns/people 

i.e. The gender problem (she was George Washington... is figurative?)


-deep philosophical questions 

Your brain is a computer
 -> figurative speech (two entries, with no roots) 

-using recursive roots of the word net to make inferences 
 
The kids were monkeys on the jungle gym
 -> is a verifiable falsehood
 


Dependencies: 
--------------------
 
Pattern 2.6


How To Use:
-------------------- 

Syntax:  python program, sentences to check, name of ouput file

In Terminal:

python figur_detection.py common_metaphors.txt common_meta_test  



Future Developments 
--------------------- 

Develop web interface for user friendly processing  
