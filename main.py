from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from fake_useragent import UserAgent
import time
import csv

# 1- DEMARRER CHROME AVEC LES BONNES OPTIONS
options = Options()
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('prefs', {'profile.managed_default_content_settings.media_stream': 2})
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1200')
options.add_argument('--start-fullscreen')
options.add_argument('--mute-audio')
options.add_extension('./ublock.crx')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-notifications')
options.add_argument('--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies')
options.add_argument('--autoplay-policy=user-required')
ua = UserAgent()
user_agent = ua.random
options.add_argument(f"user-agent={user_agent}")

monpilote = webdriver.Chrome(options=options)
print('Chrome démarré')

# 2- ACCEDER A LA PAGE DE RECHERCHE WIKIPEDIA - URL NECESSAIRE
monpilote.get('https://fr.wikipedia.org/')
time.sleep(2)
monpilote.get('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Recherche')
print('Navigation page de recherche Wikipedia')
time.sleep(3)

# 4- REMPLIR UNE ZONE DE TEXTE DANS UN FORMULAIRE - XPATH NECESSAIRE
recherche = 'Paris Saint-Germain'
mazoneSearch = WebDriverWait(monpilote, timeout=10).until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@id="ooui-php-1"]')))
mazoneSearch.send_keys(recherche)
print('Texte tapé dans le formulaire')
time.sleep(1)

# 5- CLIQUER SUR LE BOUTON "RECHERCHER" DU FORMULAIRE - XPATH NECESSAIRE
monbouton = WebDriverWait(monpilote, timeout=10).until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
time.sleep(0.5)
monbouton.click()
print('Bouton Rechercher cliqué')
time.sleep(3)

# 7- LIRE UNE LISTE D'ELEMENTS DE LA PAGE - XPATH GENERALISE NECESSAIRE
# Liste des titres d'articles
listZoneTitre = WebDriverWait(monpilote, timeout=10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@class="mw-search-result-heading"]/a')))
print('Nombre de résultats trouvés :', len(listZoneTitre))

listTitres = []
for x in listZoneTitre:
    titre = x.text.strip()
    listTitres.append(titre)
    print('Titre:', titre)

# Liste des extraits
listZoneExtrait = monpilote.find_elements(By.XPATH, '//div[@class="searchresult"]')
listExtraits = []
for x in listZoneExtrait:
    extrait = x.text.strip()
    listExtraits.append(extrait)
    print('Extrait:', extrait)

# Liste des infos (taille + date)
listZoneInfo = monpilote.find_elements(By.XPATH, '//div[@class="mw-search-result-data"]')
listInfos = []
for x in listZoneInfo:
    info = x.text.strip()
    listInfos.append(info)
    print('Info:', info)

# APPAREILLER LES LISTES SELON LEUR N° D'INDICE (page 34 du guide)
a = []
a.append(['Titre', 'Extrait', 'Info'])
for i in range(len(listTitres)):
    titre = listTitres[i]
    extrait = listExtraits[i] if i < len(listExtraits) else 'abs'
    info = listInfos[i] if i < len(listInfos) else 'abs'
    r = [titre, extrait, info]
    a.append(r)
    print(len(a), r)

# 8- ENREGISTRER LA LISTE DE LISTE PYTHON EN FICHIER CSV
fichier = open('wikipedia_psg.csv', 'w')
écrivain = csv.writer(fichier, delimiter=',')
écrivain.writerows(a)
fichier.close()
print('Fichier enregistré')

input('Presser une touche pour quitter...')
