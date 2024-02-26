import random, re, sys, pickle

from colorama import Fore, Style, Back

def normalize(aword):
    return re.sub("V", "U", re.sub("J", "I", aword.upper()))
    
def buildWdict(corpus, minimum=2, disallowCap=True):
    wcount={}
    res={}
    for w in corpus.wordIter():
        word=w.word
        if word.isalpha() and not (disallowCap and word[0].isupper()):
            nw=normalize(word)
            wcount[nw]=wcount.get(nw, 0)+1
        
    for word, freq in wcount.items():
        if freq>=minimum:
            length=len(word)
            res.setdefault(length, set()).add(word)    
    return res

class Wordle:
    def __init__(self, wdict, wlength, ffl=None):
        self.wdict=wdict
        self.bagofwords=self.wdict.get(wlength, set())
        self.wlength=wlength
        self.ffl=ffl
        
    def getLetters(self):
        acceptable=False
        while(acceptable==False):
            letters=normalize(input(f"{self.wlength} letters, please!\n").upper())
            if self.isAcceptable(letters.lower()):
                acceptable=True
            else:
                print (f"{letters} not recognized")
        return letters
        
    def play(self, rounds=6, target=None):
        usedletters={}
        if target==None:
            target=random.sample(self.bagofwords, 1)[0].upper()
        else:
            target=target
        
        for _ in range(rounds):
            self.printAlphabet(usedletters)
            letters=self.getLetters()
            fdbckstr=[]
            matches=self.getMatches(letters, target)
            partials=self.getPartials(letters, target, matches)
            
            # update usedletters
            for partial in partials:
                usedletters[letters[partial]]=1
            for match in matches:
                usedletters[letters[match]]=2
            for letter in letters:
                usedletters.setdefault(letter, -1)
            
            for num in range(self.wlength):
                guessltr=letters[num]
                if num in matches:
                    fdbckstr.append(f"{Fore.GREEN}{guessltr}")
                elif num in partials:
                    fdbckstr.append(f"{Fore.YELLOW}{guessltr}")
                else:
                    fdbckstr.append(f"{Style.RESET_ALL}{guessltr}")
                    
            print (" ".join(fdbckstr))
            if letters==target:
                print (f"{Style.RESET_ALL}Congratulations!")
                return 
                            
        print (f"Solution would have been: {target.upper()}")
        
        return
            
    def getMatches(self, letters, target):
        res=set()
        for i, (l, t) in enumerate(zip(letters, target)):
            if l==t:
                res.add(i)
        return res
        
    def getPartials(self, letters, target, matches):
        res=set()
        targetLetters=list(target)
        for m in matches:
            targetLetters[m]=""
        for i, l in enumerate(letters):
            if not i in matches and l in targetLetters:
                res.add(i)
                targetLetters.remove(l)
        return res
        
    def isAcceptable(self, astr):
        if not len(astr)==self.wlength:
            return False
        if self.ffl:
            return bool(self.ffl.lookUp(astr) or astr.upper() in self.bagofwords)
        else:
            return (astr.upper() in self.bagofwords)
            
    def printAlphabet(self, used):
        alphab=[]
        for letter in "ABCDEFGHILMNOPQRSTUXYZ":
            if used.get(letter)==2:
                alphab.append(f"{Back.GREEN}{Fore.BLACK}{letter}{Style.RESET_ALL}")
            elif used.get(letter)==1:
                alphab.append(f"{Back.YELLOW}{Fore.BLACK}{letter}{Style.RESET_ALL}")
            elif used.get(letter)==-1:
                alphab.append(f"{Back.BLACK}{Fore.BLACK}{letter}{Style.RESET_ALL}")
            else:
                alphab.append(f"{Back.WHITE}{Fore.BLACK}{letter}{Style.RESET_ALL}")
        print ("\t\t"+" ".join(alphab[:11]))
        print ("\t\t"+" ".join(alphab[11:]))
        print (f"{Style.RESET_ALL}")
        
        
if __name__ == "__main__":
    
    defaultLength=5
    defaultWdict="wordlewords.latin"
    defaultFullFormName="ffl2.pickle"
    
    for arg in sys.argv[1:]:
        try:
            defaultLength=int(arg)
        except:
            pass
    
    wdict=pickle.load(open(defaultWdict, "rb"))
    ffl=pickle.load(open(defaultFullFormName, "rb"))
    w=Wordle(wdict, defaultLength, ffl)
    w.play()
    
        
        