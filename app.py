# coding: utf-8
from flask import Flask,url_for,render_template,request,redirect
from form import RegistrationForm,SearchForm
import os
from whois import getreversewhois
from md5 import crack
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app=Flask(__name__)

username="Doggy"
password="Doggy"



@app.route('/',methods=["GET","POST"])
def login():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data==username and form.password.data==password:
            return render_template("admin.html",r=1,data="请输入网站域名",isactive1="active")
        else:
            return render_template('base.html',data="pass_error")
    elif request.method == 'POST' and not form.validate():
            return render_template("base.html",data="not_legitimate")
    else:
        return render_template('index.html')

@app.route('/whois',methods=["GET","POST"])
def whois():
    if request.method == 'GET':
        return render_template("admin.html",r=1,data="请输入网站域名",isactive1="active")
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template("whois.html",success=1,data=form.search.data,r=1,reverses=getreversewhois(form.search.data))

@app.route('/md5',methods=["GET","POST"])
def md5():
    if request.method == 'GET':
        return render_template("admin.html",r=2,data="请输入MD5",isactive2="active")
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template("md5.html",r=2,data=form.search.data,items=crack(form.search.data))

if __name__ == '__main__':
    app.debug=True
    app.run()