#!/usr/bin/python3
# ----------------------------
# flask project for pyplot demo
# ----------------------------

import flask 
import os 


DEBUG    = os.environ.get('DEBUG', True)
HOST     = os.environ.get('HOST', '0.0.0.0')
PORT     = int(os.environ.get('PORT', 8080))
TMPL_DIR = os.path.abspath('html_templates')

app = flask.Flask(__name__, template_folder = TMPL_DIR)

import random, time
random.seed()

@app.route('/')
def home():
    """ collection of tries """
    return flask.render_template('index.html')

# static and images :
@app.route('/static/<path:path>')
def send_static(path):
    """ static file: return the file without parsing """
    return send_from_directory('static', path)

@app.route('/json/mydataset')
def return_json_dataset():
    """ return a demo dataset in json format """
    time.sleep (3)
    DATASET = { 'data': [] }
    for i in range (0,6):
      DATASET['data'].append (  { 'time': 1638893700 + 10*i, 'value':  random.randint(10, 15) } )
    return DATASET

# -------------------
# matplotlib corner 
# -------------------

# pandas for array management
# pyplot as plotter
import pandas as pd
import matplotlib.pyplot as plt

GRAPH_FOLDER = 'static/img/'         # where image should be written (should be readable by flask)

@app.route('/matplotlib_demo', methods = ['GET', 'POST'])
def matplotlib_demo ():
    """ transform the dataset into an image with matplotlib and insert the image's name into the html file """
    png_file = GRAPH_FOLDER + '/' + 'my_plot.png'
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig(png_file)
    return flask.render_template('matplotlib.html',  img = '/' + png_file)

@app.route('/csv/<dataset>', methods = ['GET', 'POST'])
def plot_form_csv(dataset):
    """ same as above with data taken from publio datasources in csv format """
    png_file = GRAPH_FOLDER + '/' + 'my_plot.png'
    try:
        series = pd.read_csv(dataset + '.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
    except:
        return  flask.render_template('not_found.html')
    series.plot()
    plt.savefig(png_file)
    plt.close()
    return flask.render_template('matplotlib.html',  img = '/' + png_file)


if __name__ == '__main__':
       """ run the app """
       app.run(debug = DEBUG, host = HOST, port = PORT)

