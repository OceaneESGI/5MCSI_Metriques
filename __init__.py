from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/historigramme/")
def histogramme():
    return render_template("historigramme.html")


import requests
from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Route pour récupérer les commits et les organiser par minute
@app.route('/commits/')
def commits():
    # Appel de l'API GitHub pour récupérer les commits
    url = 'https://api.github.com/repos/907075/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Dictionnaire pour compter les commits par minute
    commit_count_per_minute = {}

    # Parcourir les commits pour extraire les minutes
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minute = extract_minutes(commit_date)
        
        # Incrémenter le compteur pour cette minute
        if minute in commit_count_per_minute:
            commit_count_per_minute[minute] += 1
        else:
            commit_count_per_minute[minute] = 1

    # Retourner les résultats sous forme de JSON
    return jsonify(commit_count_per_minute)

# Route pour extraire la minute d'un commit à partir de sa date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour afficher le graphique dans la page HTML
@app.route('/rapport_commits/')
def rapport_commits():
    return render_template('commits_graph.html')


if __name__ == "__main__":
  app.run(debug=True)
