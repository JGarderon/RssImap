### --- La gestion du débug facilitée 
from threading import RLock

VerrouAfficheur = RLock()
VerrouEcriture = RLock()
NiveauAfficheur = 99
DebugFichier = open("./log.txt","w") 

##def DebugDeco(niveau=0):
##    def _deco(fct):
##        def wrapped(m):
##            print(niveau) 
##            return fct(m)
##        return wrapped
##    return _deco
##
##@DebugDeco(0)
def DebugAff(n,m):
    with VerrouEcriture:
        DebugFichier.write(str(m)+"\n") 
    if n>=NiveauAfficheur:
        with VerrouAfficheur:
            print(m) 
