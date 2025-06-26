
# SPARQL Query => https://query.wikidata.org 
# data on multiple languages, but some countries are missing

#%% imports and constants
  
import requests
import json
import pandas as pd

# SPARQL endpoint and headers
URL = "https://query.wikidata.org/sparql"
HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "WDQueryPython/1.0 (carolina.lennon@gmail.com)"
}
LANGUAGES = ["en", "es", "fr", "de", "ru"]

#%% Functions
def fetch_countries_by_lang(language):
    """Fetch countries code, name and capital by language"""
    # SPARQL query string
    query = f"""
    SELECT ?country ?cca3 ?capital
        ?countryLabel ?capitalLabel
    WHERE {{
    ?country wdt:P31 wd:Q6256.
    OPTIONAL {{ ?country wdt:P36 ?capital. }}
    OPTIONAL {{ ?country wdt:P298 ?cca3. }}

    SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "{language}".
    }}
    }}
    ORDER BY ?countryLabel
    """

    response = requests.get(URL, params={"query": query}, headers=HEADERS)

    # Check and parse
    if response.status_code == 200:
        resp_json = response.json()
        data = resp_json["results"]["bindings"]
        
        # convert to tabular
        tabular = list()
        for row in data:
            tabular.append({
                "country": row.get("countryLabel", {}).get("value", ""),
                "capital": row.get("capitalLabel", {}).get("value", ""),
                "cca3": row.get("cca3", {}).get("value", "")
            })

        # save to JSON file
        file = f"data/countries_{language}_wikidata.json"
        with open(file, "w", encoding="utf-8") as f:
            json.dump(tabular, f, ensure_ascii=False, indent=2)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    
    return tabular

def load_data_by_lang(language):
    file = f"data/countries_{language}_wikidata.json"
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_data_by_lang(language):
    df = pd.DataFrame(load_data_by_lang(language))
    # Remove countries with missing capital and cca3
    df = df[~(df.cca3 == '')]
    df = df[~(df.capital == '')]

    # reduce: capitals to list (more than one capital for country in some cases)
    df = (df.groupby(['country', 'cca3'])['capital']
            .apply(lambda x: x.unique().tolist())
            .reset_index()
            )
 
    # Check that cca3 codes are unique, otherwise merged will not work
    if not df.cca3.is_unique:
        raise ValueError(f"cca3 codes for {language} are not unique")
    
    df = df.set_index("cca3")
    return df

def countries_multilang():
    "Dataframe with all countries labels in multiple languages"
    data = dict()
    for language in LANGUAGES:
        data[language] = clean_data_by_lang(language=language)
        # print(language, data[language].shape)
    
    for language in LANGUAGES:
        data[language].rename(columns={"country": f'name_{language}','capital': f'capital_{language}'}, inplace=True)  
                                       
    df = pd.concat(data.values(), axis=1 )
    return df
 
#%% Main
if __name__ == "__main__":
    countries = countries_multilang()
 
 

 