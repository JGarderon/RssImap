import imaplib
import hashlib
import os 

class Messagerie:
    
    connexion = False 
    prefix = "./messagerie-"
    md5 = None 
    dossier = None 
    adresse = None 
    mdp = None 
    serveur = None 
    port = None 
    dossier = None
    
    def __init__(self,data):
        self.adresse = data["adresse"]
        self.mdp = data["mdp"]
        self.serveur = data["serveur"]
        self.port = data["port"]
        self.box = data["box"]
        self.md5 = hashlib.md5(self.adresse.encode("utf8")).hexdigest() 
        self.dossier = self.prefix+self.md5
        if not os.path.exists(self.dossier):
            os.mkdir(self.dossier)
    
    def connecter(self):
        self.connexion = imaplib.IMAP4(
            self.serveur,
            self.port
        )
        self.connexion.starttls()
        self.connexion.login( 
            self.adresse,
            self.mdp
        )
        self.connexion.select(self.box)
    
    def ajouter(self,msg,date):
        return self.connexion.append(
            self.box,
            None,
            date,
            msg.as_string().encode("utf8")
        )[0] 
    
    def deconnecter(self):
        self.connexion.close()
        self.connexion.logout()

    
