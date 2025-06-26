"""
# Base dataset: REST Countries API
- Includes:
    - Country names (in multiple languages)
    - Official names (in multiple languages)
    - Capital (in English)
    - Continent, region, and subregion (in English)

# Filter:
- Keep only countries for which we have corresponding data from the CIA World Factbook (WFB)
- Extract:
    - Flag URL
    - Locator map URL

# Wikidata:
- Retrieve capital city names in multiple languages for each country
"""

#%% imports
import json

import pandas as pd

import WFB_data as wfb
import wikidata_data as wiki
import restcountries_data as rc

#%% data and constants

with open('data/continents.json', 'r', encoding='utf-8') as f:
    CONTINENTS = json.load(f)
CONTINENTS_rev = {v['eng']:k for k,v in CONTINENTS.items()}

# patches missing capitals in multiple languages from wiki 
with open('data/capitals_additional.json', 'r', encoding='utf-8') as f:
    CAPITALS_OTHERS = json.load(f)

with open('data/languages.json', 'r', encoding='utf-8') as f:
    LANGUAGES = json.load(f)

LANGUAGE_CODES = [('en','eng'), ('es','spa'), ('fr','fra'), ('de','deu'), ('ru','rus')]
LANGUAGE_CODES = dict(LANGUAGE_CODES)

 
rc_df = pd.DataFrame(rc.countries_data()).set_index('cca3') # 250 countries
wfb_df = pd.DataFrame(wfb.countries_data())[[ 'cca3', 'flag', 'locator']].set_index('cca3') # 238 countries
data = pd.concat([rc_df, wfb_df], axis=1, join='inner')  # 238  but 233 capitals
data['Continents code'] = data.continents.map(lambda x: [CONTINENTS_rev[name] for name in x])
data = data.rename(columns={'capital': 'capital_eng'})

wiki_all = wiki.countries_multilang()
wiki_df = wiki.countries_multilang().filter(like='capital', axis=1)
# Harmonize column names
wiki_df.columns = [f'capital_{LANGUAGE_CODES[col[-2:]]}' for col in wiki_df.columns]
del wiki_df['capital_eng']
 
COUNTRIES_SETS = dict()
# print(f'{data.index.tolist() = }')
for cont in CONTINENTS.keys():
    if cont == 'all':  
        COUNTRIES_SETS['all'] = data.index.tolist()
    else:
        df_cont = data[data['Continents code'].map(lambda x: cont in x)]
        COUNTRIES_SETS[cont] = df_cont.index.tolist()
    

with open('data/result.json', 'r', encoding='utf-8') as f:
    RESULTS = json.load(f)
    
RESULTS = {True: RESULTS['true'], False: RESULTS['false']}