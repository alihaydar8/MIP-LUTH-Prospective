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
    liste_url = ["https://www.francetvinfo.fr/sante/handicap/temoignages-des-etudiants-handicapes-racontent-les-discriminations-a-l-universite-je-passe-plus-de-temps-a-me-battre-pour-mes-droits_4808703.html",
                "https://www.radiofrance.fr/franceinter/ils-sont-etudiants-et-parents-le-casse-tete-de-milliers-de-jeunes-en-france-3576273",
                "https://universites.urbania.ca/article/plaidoyer-pour-aider-les-parents-etudiants",
                "https://www.lemonde.fr/campus/article/2020/01/31/etre-etudiant-et-parent-une-situation-compliquee-a-assumer_6028021_4401467.html",
                "https://inspire-orientation.org/blog/handicap-et-etudes-superieures-comment-surmonter-les-difficultes",
                "https://www.ined.fr/fr/tout-savoir-population/memos-demo/focus/etudier-et-avoir-des-enfants/",
                "https://books.openedition.org/ined/12722?lang=fr#:~:text=Lecture%20%3A%20%C2%AB%20Ensemble%20%C2%BB%20%3A%2029,OVE%2C%20enqu%C3%AAte%20CdV%20de%202016",
                "https://www.ined.fr/fr/tout-savoir-population/memos-demo/focus/etudier-et-avoir-des-enfants",
                "https://www.letudiant.fr/educpros/enquetes/handicap-dans-l-enseignement-superieur-une-prise-de-conscience-et-des-defis-a-relever.html",
                "https://www.letudiant.fr/etudes/fac/a-l-universite-les-etudiants-handicapes-peinent-a-faire-respecter-leur-droit-a-etudier.html",
                "https://www.campusfrance.org/fr/etudiant-situation-handicap-France",
                "https://www.enseignementsup-recherche.gouv.fr/fr/etudiants-en-situation-de-handicap-51299",
                "https://publication.enseignementsup-recherche.gouv.fr/eesr/FR/T243/les_etudiants_en_situation_de_handicap_dans_l_enseignement_superieur/",
                "https://www.service-public.fr/particuliers/vosdroits/F2326#:~:text=Un%20%C3%A9tudiant%20en%20situation%20de,un%20projet%20individuel%20d'int%C3%A9gration.",
                "https://www.space4ourplanet.org/fr/story/les-parents-doivent-encourager-leurs-filles-a-sinteresser-aux-phenomenes-de-lunivers-et-a-nous-aider-a-elucider-leurs-mysteres/",
                "https://e-mediatheque.sqy.fr/Default/doc/SYRACUSE/4029434",
                "https://www.le-site-de.com/l-univers-des-parents-oberhoffen-sur-moder_160191.html",
                "https://www.societe.com/etablissement/l-univers-des-parents-49876054500018.html",
                "https://www.cultura.com/p-parents-dans-un-monde-d-ecrans-comment-vous-brancher-a-l-univers-de-vos-enfants-de-0-a-18-ans-4417685.html",
                "https://www.psychologies.com/Culture/Les-phrases-de-sagesse/Phrases-de-sagesse-Maternite/Une-mere-c-est-vaste-comme-le-monde-Elle-est-l-univers-de-chaque-enfant-qu-elle-a-porte-un-univers-unique-qu-elle-a-invente-a-chaque-maternite    ",
                "https://www.cairn.info/revue-de-l-ofce-2020-3-page-5.htm",
                "https://isere.info-jeunes.fr/etudes-superieures-comment-rebondir-en-cas-de-decrochage",
                "https://www.letudiant.fr/college/difficultes-scolaires-comment-eviter-de-decrocher-completement.html",
                "https://etudiant.lefigaro.fr/article/selon-un-sondage-le-decrochage-scolaire-atteint-un-pic-au-moment-des-vacances-de-la-toussaint_d7d793cc-2cd5-11ec-81bc-f04a2133736d/",
                "https://www.apprendreaapprendre.com/reussite_scolaire/etudiants/",
                "https://diplomeo.com/actualite-echec_etude_superieures",
                "https://mcetv.ouest-france.fr/mon-mag-campus/sante-et-vie-etudiante/etudiant-comment-eviter-le-decrochage-scolaire-et-rester-motive-17112021/",
                "https://www.la-croix.com/Famille/Reussite-scolaire-isolement-etude-mesure-fort-impact-pandemie-eleves-etudiants-2021-10-14-1201180583",
                ]
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