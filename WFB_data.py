#%% imports
import re 

import requests
from bs4 import BeautifulSoup
import pandas as pd

import restcountries_data as rc

"""
Locator and flag images for each country are accessed directly via URLs from the CIA World Factbook (WFB). 
These URLs are constructed using country codes assigned by the WFB, which are **non-standard** and differ from ISO codes.

To obtain these WFB-specific country codes:
- Parse the source code of the following page (manually saved as HTML):
    https://www.cia.gov/the-world-factbook/references/flags-of-the-world/
    (stored locally as: data/Flags_WFB.htm)

Notes:
- Problem: The locator image for "Akrotiri and Dhekelia" (AD) was not found.
- Limitation: Fetching the page via `requests` only returns the first 12 countries.

### Tasks:
1. Parse `data/Flags_WFB.htm` to extract:
   - WFB country name
   - Country code (used in URLs)
   - Flag image URL
   - Locator image URL

2. Enrich this data with standard ISO codes:
   - Fetch data from the REST Countries API:
     https://restcountries.com/v3.1/independent?status=true
   - Merge by matching WFB country names with the "common name" field from REST Countries.
   - Add the standard `cca3` code to each WFB entry.

### Optional:
Additional information about each country can be retrieved by requesting WFB `.json` files. Example URLs:
- https://www.cia.gov/the-world-factbook/page-data/countries/argentina/flag/page-data.json
- https://www.cia.gov/the-world-factbook/page-data/countries/angola/factsheets/page-data.json
"""
#%% Functions
FLAG_PATTERN = re.compile(r'\/(.{2})-flag.(jpg|png|gif)$')
EXCLUDED_COUNTRIES = ['AD']

# map WFB country names to restcountries (rc) common names
MAP =   {'Bahamas, The': 'Bahamas',
        'Cabo Verde': 'Cape Verde',
        'Congo, Democratic Republic of the': 'DR Congo',
        'Gambia, The': 'Gambia',
        "Cote d'Ivoire": 'Ivory Coast',
        'Micronesia, Federated States of': 'Micronesia',
        'Korea, North': 'North Korea',
        'Korea, South': 'South Korea',
        'Congo, Republic of the': 'Republic of the Congo',
        'Sao Tome and Principe': 'São Tomé and Príncipe',
        'Turkey (Turkiye)': 'Turkey',
        'Holy See (Vatican City)': 'Vatican City',
        'Burma': 'Myanmar',
        'Curacao':'Curaçao',
        'Falkland Islands (Islas Malvinas)' : 'Falkland Islands',
        'Saint Barthelemy' : 'Saint Barthélemy' ,
        'Saint Helena, Ascension, and Tristan da Cunha' : 'Saint Helena, Ascension and Tristan da Cunha',
        'Virgin Islands' : 'United States Virgin Islands',
        }

def wfb_data():
    """
    Return list of dictionaries, where each dictionary represents a country with the following keys:
      - country : name of the country used by WFB in english
      - href : url to the country page in WFB
      - code : the country code used by WFB (not standard)
      - flag : url to the flag image
      - locator: url to the locator image

    source code of the webpage:
      - https://www.cia.gov/the-world-factbook/references/flags-of-the-world/ source code 
      - retrieved here from local file data/Flags_WFB.htm

    """
    with open("data/Flags_WFB.htm") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    countries_soup =soup.find_all('div', class_='col-lg-4' )

    countries = []
    for c in countries_soup:
        country_href = c.find('a').get('href')
        # check for end of list
        if country_href == 'https://www.instagram.com/cia':
            break
        country = c.find('span', attrs={'class': 'image-title'}).text
        flag_href = c.find('img').get('src')
        code = re.search(FLAG_PATTERN, flag_href).group(1)

        dic = {
            'country': country,
            'href': country_href,
            'code': code,
            'flag': f'https://www.cia.gov/the-world-factbook/static/flags/{code}-flag.jpg',
            'locator': f'https://www.cia.gov/the-world-factbook/static/locator-maps/{code}-locator-map.jpg',

        }
        if code not in EXCLUDED_COUNTRIES:
            countries.append(dic)
    return countries

def countries_data():
    """
    Return list of dictionaries as by wfb_data but with the following additional keys to standardize country codes and allowing to merge with other datasets:
      - cca3 : alpha-3 code (from restcountries)
      - cca2 : alpha-2 code (from restcountries)
    
    Only countries with standard country codes are kept.
    """

    wfb_countries = pd.DataFrame(wfb_data())
    wfb_codes =  standard_country_code()
    merged = pd.merge( wfb_codes, wfb_countries,how='left', on='country' )
   
    return  merged.to_dict(orient='records')
 
def standard_country_code():
    """Merge WFB data with restcountries data to get the standard country code linked to WFB country names 

    returns:
        DataFrame with columns ['country', 'cca3', 'cca2'],
        where:
            - country: name of the country used by WFB in english
            - cca3: alpha-3 code
            - cca2: alpha-2 code
    """

    rc_data = rc.load_data_by_status('independent') + rc.load_data_by_status('non_independent')

    rc_subset = list()
    for country in rc_data:
        dic = {
            'name': country.get('name').get('common'),
            'cca3': country.get('cca3'),
            'cca2': country.get('cca2')
        }
        rc_subset.append(dic)

    rc_df = pd.DataFrame(rc_subset)
    wfb_df = pd.DataFrame(wfb_data())
    # yield wfb_df

    wfb_df['name'] = wfb_df['country'] 
    wfb_df['name'] = wfb_df['name'].replace(MAP)
    merged = pd.merge(rc_df, wfb_df, how='outer', on='name')
    # yield merged
    wfb_codes = merged[[ 'country','cca3','cca2']].dropna()
    # yield wfb_codes

    return  wfb_codes
    
def fetch_assets_country(country):
    """Request and save the locator and flag images of a country locally.

    Images are saved in data/locators and data/flags folders as {code}.jpg
    
    args:
        country: dictionary with keys ['country', 'href', 'code', 'flag', 'locator'] as returned by wfb_data
    
    note:
        - This is not really used for the project, but it is useful for testing
    """
    for asset in 'locator', 'flag':
        file = f'data/{asset}s/{country["code"]}.jpg'
        print(file)
        url =  country[asset]
        response = requests.get(url)
        if response.status_code == 200:
            with open(file, "wb") as f:
                f.write(response.content)
            print(f'{country["country"]} {asset} FOUND')
        else:
            print(f'{country["country"]} {asset} NOT found')
    

def fetch_assets_all_countries():
    """Request and save the locator and flag images for all countries"""
    countries = countries_data()
    for country in countries:
        fetch_assets_country(country)


#%% 
if __name__ == '__main__':

    countries = countries_data()
  






 


    
         
 

 

# %%
""