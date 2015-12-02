from flask import Flask,redirect,url_for,render_template

#the name of the application package 

app = Flask(__name__) 

@app.route('/') 
def index(): 
    return render_template('index.html')

@app.route('/linemap') 
def linemap():
    return render_template('linemap.html')

if __name__=='__main__':
    app.debug=True
    app.run()
