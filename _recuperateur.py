from threading import Thread 
import feedparser
import hashlib
import os
import time
import urllib
import json 

#flux_entree_date = datetime.strptime(flux_entree["published"],"%a, %d %b %Y %H:%M:%S %z").strftime("%d-%m-%Y %H:%M:%S %z")

class Recuperateur(Thread):

    delais = 60*10 # en secondes  
    
    prefixe = "/flux-"
    flux = None
    flux_md5 = None 
    flux_dossier = None
    titre = None 
    contenus = None
    
    def __init__(self,flux):
        try: 
            Thread.__init__(self) 
            self.flux = flux
            self.flux_md5 = hashlib.md5(self.flux.encode("utf8")).hexdigest() 
            self.flux_dossier = self.prefixe+self.flux_md5 
            if not os.path.exists("./"+self.flux_dossier):
                os.mkdir("./"+self.flux_dossier)
        except Exception as e:
            print("Erreur - module Récupérateur : "+str(e)) 
        
    def run(self): 
        while 1:
            try: 
                print("-- Acquisition du flux "+self.flux)
                self.recuperer()
            except Exception as e:
                print("Erreur - module Récupérateur : "+str(e)) 
            time.sleep(self.delais)
    
    def recuperer(self): 
        self.contenus = feedparser.parse(self.flux) 
        self.titre = self.contenus["feed"]["title"] 
        for entree in self.contenus["entries"]:
            try:
                
                entree_id = hashlib.md5(entree["id"].encode("utf8")).hexdigest()
                print("--- Acquisition de l'item "+self.flux+": "+entree_id)
                
                self.indexer(
                    entree_id,
                    entree 
                )
                
            except Exception as e:

                print(e)
                pass

    def indexer(self,entree_id,entree):
        try:
            
            entree_index = self.flux_dossier+"/"+entree_id

            with open(entree_index+".index","x") as ecriture_index: 
                ecriture_index.write(
                    str(json.dumps(entree)) 
                ) 
            ecriture_index.close()

            entree_article = str(urllib.request.urlopen(entree["id"]).read()) 
            with open(entree_index+".article","w") as ecriture_article:
                ecriture_article.write(
                    entree_article
                ) 
            ecriture_article.close()
            
            return True

        except IOError as e:

            pass 
        
        except Exception as e:

            print(e) 
            return False 

if __name__=="__main__":

    pass 
