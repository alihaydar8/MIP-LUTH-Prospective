import re
import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
import spacy  # pip install spacy
import mysql.connector  # pip install mysql-connector-python

nlp = spacy.load('fr_core_news_md')

def database_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="hypermedia",
        password="hypermedia",
        database="hypermedia"
        )
    mydb.cursor().execute("drop table if exists mots")
    mydb.cursor().execute("CREATE TABLE IF NOT EXISTS mots (id int PRIMARY KEY  COMMENT '',str VARCHAR(255) COMMENT '',occ int(4) DEFAULT NULL) DEFAULT CHARSET utf8mb4 COMMENT '' ")
    mydb.commit()
    return mydb

def database_liste(liste_element,mydb):
    id= 1
    for element in liste_element :
        mydb.cursor().execute("INSERT INTO mots (id,str,occ) VALUES (%s,%s,%s)",(id,element[0],element[1]))
        id = id +1
    mydb.commit()


def remplire_liste_fichier(liste_vide,fichier_vide_nom):
    fichier_vide = open(fichier_vide_nom, "r",encoding='utf-8')
    for line in fichier_vide:
        for element_vide in line.split() :
            liste_vide.append(element_vide)

def  display_liste(liste_element):
    for element in liste_element :
        print (element)

def occurrences_lsite (liste_element):
    occ_liste = []
    for elemnet in liste_element :
        occ_liste.append((elemnet[0],liste_element.count(elemnet)))
    occ_liste = list(set(occ_liste))
    return occ_liste

def main():

    liste_element = []
    liste_vide = []
    fichier_vide_nom ="./fichier/vide/fichier_vide.txt"
    remplire_liste_fichier(liste_vide,fichier_vide_nom)

    # Ajouter au tableau les liens à indexed
    liste_url = []
    for url in liste_url:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching page")
            exit()

        soup = BeautifulSoup(response.content, 'html.parser')

        for element in re.split("[' ’]",soup.title.string) :
            element =  re.sub('[".,!?();:]','',element)
            if len(element)>2 and element.lower() not in liste_vide  :
                liste_element.append((nlp(element)[0].lemma_,3))
        
        for script in soup(['style', 'script', 'head', 'title', 'meta']):
            script.extract()

        for line in soup.get_text().split() :
            for element in re.split("[\'\"’]\n",line) :
                element =  re.sub('[.’,!?();:]','',element)
                if len(element)>2 and element.lower() not in liste_vide  :
                    liste_element.append((nlp(element)[0].lemma_,1))
    

    f =open("fichier.txt")
    for line in f :
        for element in re.split("[' ’]",line) :
            element =  re.sub('[.,!?();:]','',element)
            if len(element)>2 and element.lower() not in liste_vide  :
                liste_element.append((nlp(element)[0].lemma_,3))

    f.close()

    print(len(liste_element))
    liste_element = occurrences_lsite(liste_element)
    print(len(liste_element))
    # display_liste(liste_element)

    # # # # # # # # # # #  partie base de donnée # # # # # # # # # # # # 
    mydb = database_connection()
    database_liste(liste_element,mydb)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
if __name__ == '__main__' :
    main()
