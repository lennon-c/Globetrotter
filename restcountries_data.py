#%% imports
import requests
import json



#%% Functions
def download_data_independent():
    response = requests.get("https://restcountries.com/v3.1/independent?status=true")
    response.raise_for_status()
    with open('data/restcountries_independent.json', 'w', encoding='utf-8') as fp:
        json.dump(response.json(), fp)

    return response.json()

def download_data_non_independent():
    """Download and save data for non-independent countries"""
    response = requests.get("https://restcountries.com/v3.1/independent?status=false")
    response.raise_for_status()
    with open('data/restcountries_non_independent.json', 'w', encoding='utf-8') as fp:
        json.dump(response.json(), fp)

    return response.json()

def load_data_by_status(status='independent'):
    """Load data from file
    
    args:
        status: 'independent' or 'non_independent'
    """
    file = f'data/restcountries_{status}.json'
    with open(file, 'r', encoding='utf-8') as fp:
        return json.load(fp)
  
    
def countries_data():
    """Returns a list of countries data, with some selected fields."""

    rc_subset = list()
    for status in 'independent', 'non_independent':
        rc = load_data_by_status(status=status)
        for country in rc:
            dic = {
                'cca3': country.get('cca3'),
                'cca2': country.get('cca2'),
                'region': country.get('region'),
                'subregion': country.get('subregion'),
                'capital': country.get('capital'),
                'continents': country.get('continents'),
                'status': status,
                'common_eng': country.get('name').get('common'),
                'official_eng': country.get('name').get('official'),
         
            }

            for lang in 'spa', 'fra', 'deu', 'rus':
                dic[f'common_{lang}'] = None
                dic[f'official_{lang}'] = None
                if translations:= country.get('translations'):
                    if lang_dict:= translations.get(lang):
                        dic[f'common_{lang}'] = lang_dict.get('common')
                        dic[f'official_{lang}'] = lang_dict.get('official')
    
            rc_subset.append(dic)

    return rc_subset

#%% Main

if __name__ == '__main__':
    countries = countries_data()
 
 
 

 



 




   
 
 
