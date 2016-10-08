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

class Message:
    courriel_texte = """{0}

Date : {2}

Lien : {1} 

---
Résumé
--- 
{3} 
""" 
    courriel_html = """<html> 
<body> 
<h1><a href="{1}">{0}</a></h1> 
<p><a href="{1}">{1}</a> / <br />{2}</p> 
<p>{3}</p> 
</body> 
</html> 
"""
    msg = None 
    sujet = "" 
    expediteur = ""
    m_texte = ""
    m_html = ""
    m_article = ""
    f_entree = {} 
    def __init__(self,data):
        self.flux_id = data["flux_id"]
        self.flux_titre = data["flux_titre"]
        self.sujet = data["sujet"]
        self.destinataire = data["destinataire"] 
        self.article = data["article"]
        self.f_entree = data["entree"]
        self.msg = MIMEMultipart()
        self.msg['Subject'] = self.sujet #f_entree["title"]
        self.msg['From'] = formataddr(
            (
                self.flux_titre,
                self.flux_id+'@fluxrss.nothus.fr' 
            ),  
            "utf8"
        ) 
        self.msg['To'] = self.destinataire
        self.msg.attach(
            MIMEText(
                self.courriel_html.format(
                    self.f_entree["title"],
                    self.f_entree["link"],
                    datetime.strptime(
                        self.f_entree["published"],
                        "%a, %d %b %Y %H:%M:%S %z"
                    ).strftime("%d-%m-%Y %H:%M:%S %z"), 
                    self.f_entree["summary"]
                ).encode("utf-8"),
                'html',
                "utf-8" 
            )
        )
        self.msg.attach(
            MIMEText(
                self.courriel_texte.format(
                    self.f_entree["title"],
                    self.f_entree["link"],
                    datetime.strptime(
                        self.f_entree["published"],
                        "%a, %d %b %Y %H:%M:%S %z"
                    ).strftime("%d-%m-%Y %H:%M:%S %z"), 
                    self.f_entree["summary"]
                ),
                'plain' 
            )
        ) 
        part = MIMEApplication(
            self.article,
            Name="article-{0}.html".format(self.flux_id)
        )
        part['Content-Disposition'] = 'attachment; filename="article-{0}.html"'.format(self.flux_id) 
        self.msg.attach(part)

        #print(self.msg) 




        
