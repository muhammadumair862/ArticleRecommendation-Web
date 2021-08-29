from flask import Flask,render_template,request,redirect,session
import sqlite3
from flask_admin import Admin                       # use to make admin interface
from flask_sqlalchemy import SQLAlchemy             # use for database
from flask_admin.contrib.sqla import ModelView      # use to create table in admin interface

from RecommendationModel import recommendation_func
from Models import *

app=Flask(__name__)
app.secret_key="hello"

admin=Admin(app)

# %%%%%%% Database Configuration %%%%%%%%
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
db=SQLAlchemy(app)


# value1 = '''
# In this paper we consider the application of machine learning of graphical models and feature selection for developing better drug-design strategies. The work discussed in this paper is based on utilizing partial prior knowledge available through KEGG signalling pathway database in tan dim with our recent developed ensemble feature selection methods for a better regularisation of the lasso estimate. This work adds an extra layer of previously unseen knowledge in KEGG signalling pathways that embodies infering the underlying connectivity between gene-families implicated in breast cancer in MAPK-signalling pathway in response to application of anti-cancer drugs "neoadjuvant docetaxel".'''
#
# recommendation_func(value1)

@app.route('/',methods=['POST','GET'])
def login():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        auth=validate_user(username,password)
        if auth:
            session['username']=username
            return render_template("articlerecommendation.html",contex={'user':session['username']})
        else:
            return "<h2>Not Authorize User!!!</h2><br><a href='/'>Back</a>"
    else:
        return render_template('login.html')

@app.route('/signup',methods=['POST','GET'])
def singup():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        pass2=request.form['confirm_pass']
        try:
            if pass2==password:
                insert_user(email,username,password)
                return "<h2>Successfully store Record</h2><br><a href='/'>Go to Sign In</a>"
            else:
                return "<h2>Password Does Not Match!!!</h2><br><a href='/'>Back</a>"
        except:
            return "Unknown Error!!!"
    else:
        return render_template('signup.html')


# %%%%%%  Login for admin  %%%%%%%
@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            auth=validate_admin(username,password)
            if auth:
                return redirect('/admin/')
            else:
                return "<h2>Wrong Credentials!!!</h2><br><a href='/'>Back</a>"
        except:
            return "<h2>Unknown Error</h2><br><a href='/'>Back</a>"

    else:
        return render_template("adminlogin.html")

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/recommendedarticles',methods=["POST","GET"])
def recommendedarticles():
    if request.method=="POST":
        abstract_text=request.form['abstract_text']
        rec_articles=recommendation_func(abstract_text)
        return render_template('recommendedarticles.html',context={'title':rec_articles.title.values,'area':rec_articles.area.values,'abstract':rec_articles.abstract.values,'keywords':rec_articles.author_keywords.values},user=session['username'],abstract=abstract_text,len=10)
    else:
        return redirect('/')


class user(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    email = db.Column(db.String(100))
    password=db.Column(db.String(100))
    auth_user = db.Column(db.String(20))
    def __init__(self,id,email,username,password,auth_user):
        self.id=id
        self.email=email
        self.username=username
        self.password=password
        self.auth_user=auth_user

class article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.Text)
    author_keywords=db.Column(db.Text)
    abstract=db.Column(db.Text)
    area=db.Column(db.Text)
    def __init__(self,title,id,author_keywords,abstract,area):
        self.id=id
        self.title=title
        self.author_keywords=author_keywords
        self.abstract=abstract
        self.area=area

class admin_account(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    password=db.Column(db.String(100))

    def __init__(self, id,username, password):
        self.id = id
        self.username = username
        self.password = password



admin.add_view(ModelView(user,db.session))
admin.add_view(ModelView(article,db.session))
admin.add_view(ModelView(admin_account,db.session))

# %%%%%%%   to run application  %%%%%%%%
if __name__=="__main__":
    db.create_all()          # create tables if not created
    app.run(debug=True)