#!/usr/bin/python 

""" 
figurative speech detection 
By: Dominic Doyle 
05.04.2016
""" 
from pattern.en import wordnet , lexeme , parsetree , singularize
from pattern.search import search 
from sys import argv





def upward_chain(synsets, recur= False):
    """ 
    upward chains query through hypernyms in the wordnet
     
    recur = False -> first roots 
    
    """
    
    roots = []
    
    if recur:
        for syn in synsets:
            roots += [match for match in syn.hypernyms(recursive=True)]
    
        #print "recursive roots {0} for {1}".format(roots, synsets)
    else:
        for syn in synsets:
            roots += [match for match in syn.hypernyms()]
        print "first roots {0} for {1}".format(roots, synsets)
    
    return roots
        




def is_descendant(NP1, NP2, ancest=False):
    """ 
    bool ancest: search deeper than immediate ancestor
    Params: synsets
    determines from a query , if N1 has an ancestor in 
    the chain assuming NP1 are already regierested in the wn
    check if immediate descendant 
    
    returns either: ancestral or immediate
    """ 
    
    detect = '' 
    
    if NP2[0].synonyms[0] in [entry.synonyms[0] for entry in upward_chain(NP1, ancest)]:
        
        
        
        if ancest: 
            print "{n2} is an ancestral hypernym of {n1}".format(n2=NP2, n1=NP1)
        else:
            print "{n2} is an immediate hypernym of {n1}".format(n2=NP2, n1=NP1)
        
            
        return True
    else:
        return False
        
def detect_figa(phrase):
    """ 
    detects if a phrase is a 'simple' example 
    of figurative speech, fact , falsehood, or generalization
    
    NP1  + conj('is')  + NP2 
    
    """ 
    
    #check for pattern..  
    
    #a type of|an example of (took that out for now) {[one ]?} 
    criteria =  '{NP}' + ' ' + '{is|are|was|were}' + ' ' +'{NP}'
    parset =  parsetree(phrase)
    hits =  search(criteria, parset)  
    status = ""
 
    print "Parse tree: {pt}".format(pt=parset)
    
    #check for subphrases inside of phrases
    for hit in hits:
        print "NP1: {grp1}".format(grp1=hit.group(1))
        print "conj: {conj}".format(conj=hit.group(2))
        print "NP2: {grp2}".format(grp2=hit.group(3)) 
        
        
        NP1 =hit.group(1) #word objects
        conj=hit.group(2)
        NP2 =hit.group(3)
        
        
        
        syn1 = unify_query(NP1)
        syn2 = unify_query(NP2)  
        
        
        #determine relation of objects
        status  = determine_relation(syn1, syn2)
        
        
    #apply detection checks    
    return status    
        

def determine_relation(syn1, syn2):
    
    relation = ''
    
    #both are registered
    if len(syn1) > 0 and len(syn2) > 0:
        #verifiable results 
        
        print 'Common Ancestor: {0}'.format(wordnet.ancestor(syn1[0], syn2[0]))
        print 'Similarity measure between synsets: {0}'.format(wordnet.similarity(syn1[0], syn2[0]))
        
        
        if is_descendant(syn1, syn2):
            relation = "is a verifiable fact"
        elif is_descendant(syn1, syn2, True):
            relation = "is a verifiable true over-generalization"
        elif is_descendant(syn2, syn1):
            relation = "is a verifiable falsehood"
        elif is_descendant(syn2, syn1, True):
            relation = "is a verifiable false over-generalization"
        else:
            relation = "figurative speech (two entries, with no roots)"
        
    else:
        relation = "undetermined, entries not in wordnet" 
    
    return relation
        
        

def build_wn_query(wds):
    """
    build wn query from a set of words
    
    1) remove/ignore determiners  
    2) concat adj. nouns/compound words with white space 
    3) singular ...  
    
    due to the tagging base , there are strangely JJ's being identified as NP chunks 
    .. This will fix the problem for figurative love; however, I may need more 
    testing to see how far it reaches or  wd.type =='JJ' ..I would also 
    have to change the grammar to match adjp.. I really am uncertain about it 
    """ 
    query = ''  
    nouns = [wd for wd in wds if wd.type == 'NN' 
                              or wd.type == 'NNP' 
                              or wd.type == 'NNS' 
                              or wd.type == 'NNP-PERS'
                              or wd.type == 'NNP-LOC']
    
    print nouns
    if len(nouns) > 1:
        
        for noun in nouns:
            query += noun.string
            query += ' ' 
    else: 
        query =  nouns[0].string 
    
    return query.strip()    
        
    
def unify_query(query):
    """ 
    a peek of sorts .. 
    param: list of Word objs 
    return: synset entry from wn
    """
    
    
    
    #build query from 
    query = build_wn_query(query)
    print 'wordnet query: {0}'.format(query)
  
    s = wordnet.synsets(singularize(query), pos=wordnet.NOUN)
    
    if len(s) == 0:
        
        #this is a bit hacky.. it's based on the assumption, if it fails, it may be a two word NN 
        #i.e. thrill ride fails, ride doesn't 
        print 'no entry for {0}..'.format(query) 
        
        s = wordnet.synsets(singularize(query.split()[1]), pos=wordnet.NOUN)
        if len(s) == 0:
             print 'no entry for {0}'.format(query.split()[1]) 
    
        
    
    return s

def main(args):
    
    """ 
    her eyes were jewels :figurative detected (correct)
    a car is a vehicule  : non figurative detected (correct) 
    success is a bastard : figurative (incorrect)
    
    """
    wout = open(args[2] + ".txt", 'a+')
    
    
    with open(args[1], 'r') as f:
        lines = f.readlines()
       
        for num, ex in enumerate(lines):
            
            print "example: {0}".format(ex) 
            wout.write(str(num) + ") " + ex)
            wout.write( " -> " + detect_figa(ex))
            wout.write("\n")
        f.close()
        wout.close()
if __name__ == '__main__':
    main(argv)
