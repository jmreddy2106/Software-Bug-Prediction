import os
import time

from flask import Flask, render_template, request, redirect, url_for
import final
import model

app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def hello_world():
    img_name = 'img' + str(time.time()) + '.jpg'
    if request.method == 'POST':
        link = request.form['url']
        name = request.form['name']
        select = request.form['label']
        opt = int(request.form['clf'])

        for filename in os.listdir('static/'):
            if filename.startswith('img'):  # not to remove other images
                os.remove('static/' + filename)

        final.extract_data(link, name)
        clf, data = model.model(select, opt, img_name, name)
        filename, res = model.predict_user_file(clf, name, select)
        print(filename)
        return render_template('index.html', i=img_name, data=data, filename=filename, res=res, le=len(res))
    return render_template('index.html', i=None, le=0)


@app.route('/index<name>')
def res(name):
    return  render_template('hi.html')


if __name__ == '__main__':
    app.run()
