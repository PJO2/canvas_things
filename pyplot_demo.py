#!/usr/bin/python3
# ----------------------------
# flask project for pyplot demo
# ----------------------------

import flask 
import os 

# pandas for array management
# pyplotas plotter
import pandas as pd
import matplotlib.pyplot as plt


DEBUG    = os.environ.get('DEBUG', True)
HOST     = os.environ.get('HOST', '0.0.0.0')
PORT     = int(os.environ.get('PORT', 8080))
TMPL_DIR = os.path.abspath('html_templates')
GRAPH_FOLDER = 'static/img/'

app = flask.Flask(__name__, template_folder = TMPL_DIR)


import random
random.seed()

# static and images :
@app.route('/static/<path:path>')
def send_static(path):
        return send_from_directory('static', path)

@app.route('/json/mydataset')
def return_dataset():
    DATASET = { 'data': [] }
    for i in range (0,6):
      DATASET['data'].append (  { 'time': 1638893700 + 10*i, 'value':  random.randint(10, 15) } )
    return DATASET



@app.route('/', methods = ['GET', 'POST'])
def home():
    png_file = GRAPH_FOLDER + '/' + 'my_plot.png'
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig(png_file)
    return flask.render_template('index.html',  img = '/' + png_file)


@app.route('/csv/<dataset>', methods = ['GET', 'POST'])
def plot_form_csv(dataset):
    png_file = GRAPH_FOLDER + '/' + 'my_plot.png'
    try:
        series = pd.read_csv(dataset + '.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
    except:
        return  flask.render_template('not_found.html')
    series.plot()
    plt.savefig(png_file)
    plt.close()
    return flask.render_template('index.html',  img = '/' + png_file)


if __name__ == '__main__':
       app.run(debug = DEBUG, host = HOST, port = PORT)

