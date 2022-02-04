import requests
from bs4 import BeautifulSoup
import json

titre=input("Entrez le titre d'un film: ")

file= open("main2.html", "w")
file.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <link rel="stylesheet" href="style.css">
    <title>Python Parsing</title>
</head>
<body>''')


pages = [{'page':'imdb','url_search':f'https://www.imdb.com/find?q={titre}&ref_=nv_sr_sm','url_in':'https://www.imdb.com'},{'page':'rotten','url_search':f'https://www.rottentomatoes.com/search?search={titre}','url_in':''}]

json_array = {'base':{},'results':[]}

for index, page in enumerate(pages):
    url = page['url_search']
    request = requests.get(f'{url}')
    soupdata = BeautifulSoup(request.content, "html.parser")

    # Pour le site IMDB
    if (page['page'] == 'imdb'):
        result = soupdata.find("table", class_="findList").find_all('tr')[0].find('a').get('href')

        # Concaténer le début de l'url d'IMDB
        url = page['url_in']
        request_2 = requests.get(f'{url}{result}')
        soupdata_2 = BeautifulSoup(request_2.content, "html.parser")

        # Récupération des données
        titre = soupdata_2.find('h1')
        image = soupdata_2.find('div',class_='ipc-poster__poster-image').find('img', class_='ipc-image').get('src')
        note = soupdata_2.find('span',class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV")
        annee = soupdata_2.find('span',class_="TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex")
        synopsys = soupdata_2.find('span',class_="GenresAndPlot__TextContainerBreakpointXL-sc-cum89p-2 eqbKRZ")

        # Dictionnaire du résultat
        json_array['base'] = {'titre': titre.text, 'image': image,'annee':annee.text,'synopsys':synopsys.text}
        json_array['results'].append({'site':'imdb','note':note.text })

       
#         file.write(f'''
#             <container class="wrap">
#                 <div class="wrap_left">
#                     <p>{titre}</p>
#                     <img src="{image}" />
#                 </div>
#                 <div class="wrap_right">
#                     <div class="wrap_imdb">
#                         IMDB
#                     </div>
#                     <div class="wrap_rotten">
#                         ROTTEN
#                     </div>

#                 </div>
#             </container>
#             </body>
#             </html>
# ''')
        

    #Pour le site RottenTomatoes
    if (page['page'] == 'rotten'):
        result = soupdata.find('search-page-result').find('ul').find_all('search-page-media-row')[0].find('a').get('href')
        request_2 = requests.get(f'{result}')
        soupdata_2 = BeautifulSoup(request_2.content, "html.parser")

        # Récupération des données
        note_audience = soupdata_2.find('score-board').get('audiencescore')
        note_critic = soupdata_2.find('score-board').get('tomatometerscore')

        # Dictionnaire du résultat
        json_array['results'].append({'site':'rotten','note_audience':note_audience,'note_critic':note_critic })

print(json_array)

file.write(f''' <div class="card mb-3" style="max-width: 80%; margin: 100px auto 0 auto;">
        <div class="row g-0">
            <div class="col-md-4" style="text-align:center;">
                <img src="{image}" class="img-fluid rounded-start">
            </div>
            <div class="col-md-8">
            <div class="card-body">
                <h5 class="card-title">{titre} ({annee})</h5>
                <p class="card-text">{synopsys}</p>
            </div>
            <div class="d-flex justify-content-around">
            <div class="card text-dark bg-light mb-3" style="width: 18rem;display:inline-block;">
                <div class="card-header">Note IMDB <span class="card-title">
                <svg style="width:20%;" class="ipc-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 32"><rect width="100%" height="100%" rx="4" fill="#F5C518"/><path d="M8 25h5V7H8zM24 7l-1 8-1-4-1-4h-6v18h4V13l2 12h3l2-12v12h4V7h-6ZM32 25V7h8c2 0 3 1 3 3v12c0 2-1 3-3 3h-8Zm6-15h-1v12l1-1V10ZM52 12h1c2 0 3 1 3 3v7c0 2-1 3-3 3h-1l-2-1-1 1h-4V7h5v6l2-1Zm-1 8v-6l-1 1v7h1v-2Z"/></svg>
                </span></div>
                <div class="card-body">
                    
                    <p class="card-text text-center">{note}/10</p>
                </div>
            </div>
            <div class="card text-dark bg-light mb-3" style="width: 18rem;display:inline-block;">
                <div class="card-header">Notes Rotten Tomatoes <span class="card-title">
                <svg style="width:10%;" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 80 80"><defs><path id="a" d="M0 0h77v64H0z"/></defs><g fill="none" fill-rule="evenodd"><g transform="translate(1 16)"><mask id="b" fill="#fff"><use xlink:href="#a"/></mask><path d="M77 27C76 15 70 5 60 0v1c-6-3-17 6-24 1 0 2 0 10-12 10 2-2 3-6 1-8-5 4-7 5-17 3-5 6-9 15-8 25 1 21 21 33 41 32 20-2 37-16 36-37" fill="#FA320A" mask="url(#b)"/></g><path d="M42 11c4-1 16 0 20 5l-1 1c-6-3-16 6-24 2 0 1 0 9-11 10l-1-1c2-2 3-6 1-8-5 4-8 6-19 3v-1l12-6 2-1H11v-1c4-5 12-7 17-4l-6-7 6-3 4 9c4-6 11-7 15-2h-1c-2 0-4 3-4 4" fill="#00912D"/></g></svg>
                </span></div>
                <div class="card-body text-center">
                    <p class="card-text mr-1 mb-0" style="display: inline-block;">Critic: <span>{note_critic}</span></p> | 
                    <p class="card-text" style="display: inline-block;">Audience: <span>{note_audience}</span></p>
                </div>
            </div>
        </div>

        </div>
        </div>''')
with open('json_data.json', 'w') as outfile:
    json.dump(json_array, outfile)




# <div class="row">
#     <div class="col-md-4 bg-secondary">
#         <div class="well text-danger">
#             <h1>{titre}</h1>
#             <img src="{image}"/>
#             <p>{synopsys}</p>
#         </div>
#     </div>
#     <div class="col-md-8 d-flex align-content-center">
#         <div class="row h-auto">
#             <div class="col-md-6 bg-secondary">
#                 <div class="well">2</div>
#             </div>
#         </div>
#         <div class="row h-auto">
#             <div class="col-md-6 bg-secondary">
#                 <div class="well">3</div>
#             </div>
#         </div>
#     </div>
# </div>
# </body>
# </html>


