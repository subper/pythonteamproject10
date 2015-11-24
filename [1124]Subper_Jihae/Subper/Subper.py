from flask import Flask, request, session, g, url_for, redirect, \
    render_template, abort, flash

app = Flask(__name__)


@app.route('/search', methods = ['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/search/result', methods = ['GET', 'POST'])
def search_result():
    input = request.form['input']
    category = request.form['category']
    return render_template('search_result.html', name = input, cate = category)

if __name__ == '__main__':
    app.debug = True        #개발할 때만 이렇게
    app.run(host='127.0.0.1', port=5000)

