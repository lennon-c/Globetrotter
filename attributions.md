 

## Data Sources for Globetrotter

The information used in **Globetrotter** is compiled from a variety of reliable, publicly accessible datasets:

### Country Names, Capitals, and Translations

- **Primary source:** 
    - [REST Countries API](https://restcountries.com/) This open-source dataset provides comprehensive country metadata, including official and common country names, continent, ISO codes, translations of country names in several languages, and capital cities in English.
    
- **Capital city translations:**  
    - Retrieved from **Wikidata** using SPARQL queries ([example query – Spanish](https://query.wikidata.org/#SELECT%20%3Fcountry%20%3Fcca3%20%3Fcapital%0A%20%20%20%20%20%20%20%20%3FcountryLabel%20%3FcapitalLabel%0AWHERE%20%7B%0A%20%20%3Fcountry%20wdt%3AP31%20wd%3AQ6256.%0A%20%20OPTIONAL%20%7B%20%20%3Fcountry%20wdt%3AP36%20%3Fcapital.%20%20%7D%0A%20%20OPTIONAL%20%7B%20%20%3Fcountry%20wdt%3AP298%20%3Fcca3.%20%20%7D%0A%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20%0A%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%22.%0A%20%20%7D%0A%7D%0A%0AORDER%20BY%20%3FcountryLabel%0A)) to obtain capital names in multiple languages.
    
- **Supplementary translations:**  
    - For capital cities whose translations are not available via Wikidata, additional translations are generated using ChatGPT.
    These translations are listed in the `capitals_additional.json` file.
 
### Flags and Maps

- Flag and locator map images are sourced from the **CIA World Factbook**.  
    According to the CIA:
    
    > “Factbook images and photos – obtained from a variety of sources – are in the public domain and are copyright free.”  
    > — _CIA World Factbook_
    

These assets are used under public domain terms, with no copyright restrictions.

 