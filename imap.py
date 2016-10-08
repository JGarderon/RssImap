import hashlib
import os 
from datetime import datetime
import html
import time 

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase 
from email.mime.application import MIMEApplication 
from email.mime.text import MIMEText
import email.encoders as Encoders
from email.header import Header 
from email.utils import formataddr

import sys
import json
import glob

from os.path import basename


### --- Les classes pour notre script principal 
from _messagerie import Messagerie 
from _message import Message 
from _recuperateur import Recuperateur 

### --- Récupération de la liste des flux 
try:
    fluxRSS = []
    with open("./liste.flux","r") as f:
        for l in f:
            fluxRSS.append(l.rstrip('\n\r'))
    f.close()
    if len(fluxRSS)==0:
        raise Exception("... la liste des flux est vide !") 
except:
    print("ERREUR / impossible de récupérer la liste des flux") 
    sys.exit()



### --- Récupération de la liste des messageries 
try:
    messageries = []
    with open("./liste.messageries","r") as f:
        for l in f: 
            try: 
                messageries.append(json.loads(l.rstrip('\n\r')))
            except:
                pass 
    f.close()
    if len(messageries)==0:
        raise Exception("... la liste des messageries est vide !") 
except:
    print("ERREUR / impossible de récupérer la liste des messageries") 
    sys.exit() 


### --- Association des comptes de messagerie à des objets de connexion 
connections = []
for m in messageries:
    connections.append(
        Messagerie(m)
    ) 

### --- Fonction pour faire la correspondance flux / messagerie
def Correspondance(dossier_travail,entrees_index,threadFlux,connexion):
    try:
        connexion.connecter()
        for entree in entrees_index:
            entree_id = basename(entree).split(".")[0] 
            if not os.path.exists(dossier_travail+"/"+entree_id):
                entree_elements = json.loads(open(entree,"r").read()) 
                date = datetime.strptime(
                    entree_elements["published"],
                    "%a, %d %b %Y %H:%M:%S %z"
                ).timestamp() 
                if connexion.ajouter(
                    Message({
                        "flux_id": threadFlux.flux_md5, 
                        "flux_titre": threadFlux.titre, 
                        "sujet": entree_elements["title"],
                        "destinataire": connexion.adresse, 
                        "article": "", 
                        "entree": entree_elements  
                    }).msg,
                    date  
                )=="OK": 
                    with open(dossier_travail+"/"+entree_id,"w"):
                        pass 
        connexion.deconnecter()
    except Exception  as e:
        print("ERREUR / lors de la correspondance : "+str(e)) 

### --- Conservation des threads 
fluxRSSThreads = []

### --- Lancement des threads pour les boucles de récupération
### --- --- ... d'abord les threads de récupération de flux 
try: 
    for flux in fluxRSS:
        print("-- Lancement du Thread pour le flux "+flux) 
        _thread = Recuperateur(flux)
        _thread.start()
        fluxRSSThreads.append(_thread)
    time.sleep(1) 
except Exception as e:
    print("ERREUR / lors du lancement des threads pour la récupération des flux : "+str(e))

print("-- Fin de lancement des threads")   

### --- --- ... enfin la boucle pour que le script "main" ne s'arrête pas
_boucle = True 
while True:
    try: 
        for threadFlux in fluxRSSThreads:
            entrees_index = glob.glob("."+threadFlux.flux_dossier+"/*.index") 
            for connexion in connections: 
                dossier_travail = connexion.dossier+threadFlux.flux_dossier
                if os.path.exists(dossier_travail):
                    Correspondance(
                        dossier_travail, 
                        entrees_index,
                        threadFlux,
                        connexion 
                    )
        time.sleep(60*20) 
    except Exception as e:
        print("ERREUR / lors de l'enregistrement des flux dans les messageries : "+str(e)) 
        _boucle = False 

















##    #
##
##
##
##
##
##
##    
##    try:
##        for f in fluxRSS:
##            f_dossier = hashlib.md5(f.encode("utf8")).hexdigest()
##            f_contenus = feedparser.parse(f)
##            f_tmp = [] 
##            for f_entree in f_contenus["entries"]:
##                f_id = hashlib.md5(f_entree["id"].encode("utf8")).hexdigest()
##                f_date_courriel = datetime.strptime(f_entree["published"],"%a, %d %b %Y %H:%M:%S %z")
##                f_pj = urllib.request.urlopen(f_entree["id"]).read()
##                f_fichier = f_dossier+"/"+f_id
##                
##                f_tmp.append({
##                    "date": f_date_courriel,
##                    "pj": f_pj,
##                    "id": f_id,
##                    "fichier": f_fichier,
##                    "contenu": f_entree,
##                    "msg": msg 
##                })
##            
##            for c in connections:
##                print(c.adresse+" / "+c.dossier)
##                print("./"+c.dossier+"/"+f_dossier)
##                if not os.path.exists("./"+c.dossier):
##                    os.mkdir("./"+c.dossier) 
##                if os.path.exists("./"+c.dossier+"/"+f_dossier):
##                    print("! D'accord pour recevoir ce flux") 
##                    c.connecter() 
##                    for msg_tmp in f_tmp:
##                        print("--tentative d'ajout d'un message "+msg_tmp["contenu"]["title"]) 
##                        msg_tmp["msg"]['To'] = c.adresse 
##                        try:
##                            with open("./"+c.dossier+"/"+f_dossier+"/"+msg_tmp["id"],"r"):
##                                print("... message déjà existant") 
##                        except IOError:
##                            if c.ajouter(
##                                msg_tmp["msg"],
##                                msg_tmp["date"].timestamp() 
##                            )=="OK":
##                              with open("./"+c.dossier+"/"+f_dossier+"/"+msg_tmp["id"],"w"):
##                                print("... message ajouté")
##                            else:
##                                print("... erreur lors de l'enregistrement dans la boîte, pas de nouvelle tentative") 
##                    c.deconnecter()
##                else:
##                    print("! Pas d'accord pour recevoir ce flux") 
##    except Exception as e:
##        print("ERR / "+str(e)) 
##    print("fin et pause...") 
##    time.sleep(20)
##
##
