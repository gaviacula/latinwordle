import re, sys

class FullFormLexicon:
    """ A minimal trie that trie to store a big set of words """

    def __init__(self, adict={}):
        self.d=adict
        
    def addWord(self, word):
        this=self.d
        for ch in word:
            this=this.setdefault(ch, {})
        this["end"]=True
            
    def lookUp(self, word):
        this=self.d
        for ch in word:
            if ch in this:
                this=this[ch]
            else:
                return False
        return (this.get("end", False))