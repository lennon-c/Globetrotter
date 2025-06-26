import random
import json
 
from app_data import COUNTRIES_SETS, CONTINENTS, data, wiki_df, CAPITALS_OTHERS

#%% Data
class CTRY():
    """country class holding country data"""
    def __init__(self, cca3, language='eng'):
        self.cca3 = cca3
        # display language (no countries official language)
        self.lang = language
        self.name = data.loc[cca3, f'common_{language}']
        self.official = data.loc[cca3, f'official_{language}']
        self.capital = self.capital_names()
        self.continent = self.continent_names()
        self.flag = data.loc[cca3, 'flag']
        self.locator = data.loc[cca3, 'locator']

    def continent_names(self):
         codes =data.loc[self.cca3, 'Continents code']  
         names = [CONTINENTS[code][self.lang] for code in codes]
         return f'{", ".join(names)}'
    
    def capital_names(self):
        # from restcountries
        if self.lang == 'eng':
            names = data.loc[self.cca3, 'capital_eng']
            if not names:
                names = ['-']
        else:
            # from Wiki
            try: 
                names = wiki_df.loc[self.cca3, f'capital_{self.lang}']
            # from other sources (CHATGPT)
            except:
                names = CAPITALS_OTHERS.get(self.cca3, {}).get(self.lang)
                if names is None:
                    names = ['-']
                else:
                    names = [names]

        return f'{", ".join(names)}'

#%% Game Logic and Data
class GAME():
    def __init__(self, ctry_set='all', language='eng', num=5):
        self.ctry_set = ctry_set
        self.language = language
        self.num = num
        self.correct_country, self.countries = self.get_countries() # self.countries 
        self.countries_names = [country.name for country in self.countries]
        self.correct_name: str = self.correct_country.name
        self.user_answer: str|None = None # country name guessed
        self.result: bool|None = None # populated by check_answer

    def get_countries(self):
        random.shuffle(COUNTRIES_SETS[self.ctry_set])
        countries_sample = COUNTRIES_SETS[self.ctry_set][:self.num]
        countries = [CTRY(country, language=self.language) for country in countries_sample]
        country = countries[0]
        random.shuffle(countries)
        return country, countries
  
    def __repr__(self):
        """Custom serialization for nested objects.
        
        Required to be able to store the game in gradio session/browser state.
        """
        def simplify(obj):
            """Recursively simplify objects for serialization"""
            if hasattr(obj, '__dict__'):
                return {k: simplify(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, (list, tuple)):
                return [simplify(v) for v in obj]
            else:
                return obj

        data = simplify(self)
        return json.dumps(data )
 
      