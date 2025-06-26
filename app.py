#%% imports
import random
import json
from functools import partial

import gradio as gr

from app_data import LANGUAGES, CONTINENTS, RESULTS
from game import GAME
from layout import theme, css
 
#%% UI
def continent_choices(lang):
    """return a list of tuples (name, continent code) of continents in the selected language"""
    continent_rev = [(v[lang],k) for k,v in CONTINENTS.items()]
    return continent_rev
 
def language_choices(lang):
    """return a list of tuples (name, language code) of available languages/translations in the selected language"""
    language_rev = [(v[lang],k) for k,v in LANGUAGES.items()]
    return language_rev
 
class Assets():
    """creating class only for encapsulating assets to make the code more readable"""
    # site gadgets
    next_btn = gr.Button("Next", variant="primary")
    reset_btn = gr.Button("Reset")
    select_language = gr.Dropdown(language_choices('eng'), label="Language", interactive=True) 
    select_continent = gr.Dropdown(  continent_choices('eng'), label="Continent", interactive=True)
    show_flag = gr.Checkbox(label="Show Flag", value=True)
    show_capital = gr.Checkbox(label="Show Capital", value=True)
    num_choices = gr.Slider(value=5, minimum=2, maximum=20, label="Number of alternatives", step=1, interactive=True)

    username_input = gr.Textbox(label="Choose your user name!", submit_btn="Ok",container=True) 
    user_settings = gr.HTML() # display of some user settings

    # game gadgets
    choices = gr.Radio([], show_label=False, interactive=True, elem_classes='choices') # alternatives
    locator =gr.HTML(container=True , elem_classes='image-locator' )
    flag = gr.HTML( min_height='50px')
    capital = gr.HTML()
    result = gr.HTML()
    score = gr.HTML(container=True) 
    

class Functions( ):
    """creating class only for encapsulating functions to make the code more readable"""
    def save_settings(self, key, value, user_data):
        user_data[key] = value
        return user_data

    def click_next(self, user_data):
        # check if next button pressed without answering
        game = json.loads(user_data["game"])
        # print(f'{game['result'] = }')
        if game['result'] == None:
            user_data["skipped_counter"] += 1
        return user_data
         
    def next_country_game(self, user_data):
        # print(user_data)
        game = GAME(ctry_set=user_data['ctry_set'], language=user_data['language'], num=user_data['num_choices'])
        # print(f'{type(user_data["game"] )=}')
        user_data["game"] = game 

        # update UI
        country = game.correct_country
        locator = self.locator_value(country.locator)

        flag = gr.HTML(self.flag_value(country.flag), visible=user_data['show_flag'])
        capital = gr.HTML(self.capital_value(country.capital), visible=user_data['show_capital'])
        choices = gr.Radio(choices=game.countries_names, value = None, interactive=True)
        result = gr.HTML(self.result_value())    
        return choices, locator, flag, capital, result, user_data
    
    def check_answer(self, user_answer, user_data):
        # game logic
        game = json.loads(user_data["game"])
        if user_answer == game['correct_name']:
            result = True
        else:
            result = False  

        game['user_answer'] = user_answer
        game['result'] = result
        user_data.update({'game': json.dumps(game)})
  
        if result: 
            user_data["correct_counter"] += 1
        else:
            user_data["wrong_counter"]  += 1

        # update UI
        choice_labels = list()
        for c in game['countries_names']:
            # always show correct answer independently of the result
            if  c == game['correct_name']:
                choice_labels.append(f'{c}  ✔')
            # show incorrect answer for wrong answer
            elif c == user_answer and not result:
                choice_labels.append(f'{c}  ✘')
            else: # choices that were not selected and not correct nor incorrect
                choice_labels.append(c)

        choices = gr.Radio(choices=choice_labels, interactive=False)
        score = self.score_value(user_data)
        lang = user_data['language']
        message = random.choice(RESULTS[result][lang])
        color = 'vars(--gr-theme-primary)' if result else 'red'
        result = gr.HTML( self.result_value(color, message)) 

        return result, choices, gr.HTML(score), user_data

    def reset_score(self, user_data):
        user_data["correct_counter"] = 0
        user_data["wrong_counter"] = 0
        user_data["skipped_counter"] = 0
        return  self.next_country_game(user_data)

    def display_user_data(self, user_data):
        # print(user_data)
        username = user_data.get("username")
        if not username:
            username = 'User'

        # update defaults values for gadgets, based on user settings
        ctry_set = user_data.get("ctry_set")
        lang = user_data.get("language")
        flag = user_data.get("show_flag")
        capital = user_data.get("show_capital")
        num = user_data.get("num_choices")
        continents = continent_choices(lang)
        select_continent = gr.Dropdown(value=ctry_set, choices=continents)
        # languages = language_choices(lang)
        # select_language = gr.Dropdown(value=lang, choices=languages)

        # Human readable text
        language = LANGUAGES[lang][lang]
        continent = CONTINENTS[ctry_set][lang]
        user_info = self.user_settings_value(username, language, continent)
        
        score = self.score_value(user_data) # this might be removed 
        return gr.HTML(user_info), lang, select_continent, flag, capital, num, score
    
    # helpers for display values
    def user_settings_value(self, username, language, continent):
        text = f"""
        <p>Hello <strong>{username}</strong>!</p>
        <p>Settings:</p>
        <ul>
        <li>Language: <strong>{language}</strong></li>
        <li>Continent: <strong>{continent}</strong></li>
        </ul>"""
        return text

    def flag_value(self, url):
        return f'<img src={url} width="40%" height="auto">'
    
    def locator_value(self, url):
        return f'<img src={url} class="image-locator" style="width: 600px; height: auto; ">'
    
    def score_value(self, user_data):
        correct = user_data["correct_counter"]
        wrong = user_data["wrong_counter"]
        skipped = user_data["skipped_counter"]
 
        style = 'border: 0px; text-align: center;'
        html = f"""
        <table style="width:100%; border: 0px;">
            <tr style="border: 0px;">
                <th style="{style}" >correct : {correct}</th>
                <th style="{style}" >wrong : {wrong} </th>
                <th style="{style}" >skipped : {skipped}</th>
            </tr>
        </table>
        """
        return html
    
    def result_value(self, color = None, message = None):
        template = """<span style="font-weight: bold; margin:auto; display:table;font-size: 1.25em; color: {color}; ">{message}</span>"""
        if not message:
            message = ''
        if not color:
            color = 'black'
        return template.format(color=color, message=message)
    
    def capital_value(self, capital):
        return f'<span style="font-weight: bold;display:table;font-size: 1.25em;">{capital}</span>'
             
 
#%% LAYOUT

with open("instructions.md", "r", encoding="utf-8") as f:
    instructions = f.read()
    
with open("attributions.md" , "r", encoding="utf-8") as f:
    attributions  = f.read()
 
with gr.Blocks(css=css, theme=theme) as demo:
    DEFAULTS = dict(username=None
                          , language='eng'
                          , ctry_set='all'
                          , correct_counter=0, wrong_counter=0, skipped_counter=0
                          , show_flag=True
                          , show_capital=True
                          , num_choices=5
                          , game = repr(GAME('all', 'eng')))
    
    user_data = gr.BrowserState({**DEFAULTS})
    app = Assets()

    with gr.Sidebar(open=False):
        gr.Markdown(f"""# Globetrotter """)
        app.user_settings.render()
        app.select_language.render()
        app.select_continent.render()
        app.show_flag.render()
        app.show_capital.render()
        app.num_choices.render()
        app.username_input.render()

    with gr.Tab('Game'):
        with gr.Row(variant="panel", show_progress=False,equal_height=True):
            with gr.Column(scale=4):
                with gr.Row(show_progress=False):
                    app.flag.render()
                    app.capital.render()
            with gr.Column(scale=3,show_progress=False):
                app.score.render() 
                
        with gr.Row(variant="panel", show_progress=False):
            with gr.Column(scale=4):
                app.locator.render()
            with gr.Column(scale=3,show_progress=False):
                app.result.render()
                app.choices.render()

                with gr.Row(show_progress=False):
                    app.next_btn.render()
                    app.reset_btn.render()

    with gr.Tab( "Instructions"):
        gr.Markdown(instructions)

    with gr.Tab( "Attributions"):
        gr.Markdown(attributions)

    # HANDLERS
    fn =  Functions()

    # list of outputs and inputs
    output_list = [app.choices, app.locator, app.flag, app.capital, app.result, user_data]
    display_user_data = dict(fn=fn.display_user_data
                        , inputs=user_data
                        , outputs=[app.user_settings, app.select_language, app.select_continent, app.show_flag, app.show_capital, app.num_choices, app.score], show_progress=False)
    
    next_country_game = dict(fn=fn.next_country_game
                                , inputs=user_data
                                , outputs= output_list
                                , show_progress=False)
    
    # initial display
    demo.load(**display_user_data).then(**next_country_game)

    # when user changes settings
    actions = [
        (app.username_input, 'username', 'submit', True),
        (app.select_language, 'language', 'input', True),
        (app.select_continent, 'ctry_set', 'input', True),
        (app.show_flag, 'show_flag', 'select', False),
        (app.show_capital, 'show_capital', 'select', False),
        (app.num_choices, 'num_choices', 'input', True),
    ]

    for component, key, action, re_display in actions:
        event_hook = getattr(component, action)
        pipe = event_hook(partial(fn.save_settings, key), [component, user_data], [user_data])
        if re_display:
            pipe = pipe.then(**display_user_data)
        pipe.then(**next_country_game)

    # buttons actions
    (app.next_btn.click(fn.click_next
                        , [user_data]
                        , [user_data]).
                        then(**display_user_data).
                        then(**next_country_game))
    
    (app.reset_btn.click(fn.reset_score
                        , [user_data]
                        , output_list
                        , show_progress=False)
                        .then(**display_user_data))

    # when user answers the game
    app.choices.select(fn.check_answer
                        , [app.choices, user_data]
                        , [app.result,app.choices, app.score, user_data]
                        , show_progress=False)
 
demo.launch(share=True)
