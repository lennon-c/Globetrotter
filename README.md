---
title: Globetrotter
app_file: app.py
sdk: gradio
sdk_version: 5.34.2
short_description: Test your geography skills and guess the correct country.
emoji: 🌍
colorFrom: blue
pinned: true
---

## 🌍 **Globetrotter**

**Globetrotter** is an educational game where your goal is to **guess the correct country** based on its **map** — and optionally its **flag** and **capital city**.

It’s a **multilingual game**, currently supporting:  
English, Spanish, German, French, and Russian.

🔗 **Play it here:** [huggingface.co/spaces/clennonz/Globetrotter](https://huggingface.co/spaces/clennonz/Globetrotter)

---

##  **Source of Data**

- **[REST Countries API](https://restcountries.com/):**  
    Used for country lists, ISO codes, country name translations, and capital cities (in English).
    
- **[Wikidata](https://www.wikidata.org/):**  
    SPARQL queries are used to retrieve capital city names in multiple languages.  
    👉 [Example query – Spanish](https://query.wikidata.org/#SELECT%20%3Fcountry%20%3Fcca3%20%3Fcapital%0A%20%20%20%20%20%20%20%20%3FcountryLabel%20%3FcapitalLabel%0AWHERE%20%7B%0A%20%20%3Fcountry%20wdt%3AP31%20wd%3AQ6256.%0A%20%20OPTIONAL%20%7B%20%20%3Fcountry%20wdt%3AP36%20%3Fcapital.%20%20%7D%0A%20%20OPTIONAL%20%7B%20%20%3Fcountry%20wdt%3AP298%20%3Fcca3.%20%20%7D%0A%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20%0A%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%22.%0A%20%20%7D%0A%7D%0A%0AORDER%20BY%20%3FcountryLabel%0A)
    
- **ChatGPT:**  
    Used to fill in missing capital translations where Wikidata did not provide results.
    
- **[CIA World Factbook](https://www.cia.gov/the-world-factbook/):**  
    Used for country flag images and locator (map) images.
    

---

## **About This Project**

This is a personal project built to explore the capabilities of [**Gradio**](https://www.gradio.app/).

Gradio makes it easy to build and share web applications:

- You can serve it locally on your own machine.
- Or host it for free using [**Hugging Face Spaces**](https://huggingface.co/spaces).