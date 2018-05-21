from myapp import app
from flask import render_template, request, redirect, make_response, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import required, length, Email
import logging
import json
import urllib, urllib2
from myapp.models.search import Search

MASHAPE_KEY = 'your-mashape-key'


class LoginForm(FlaskForm):
    username = StringField('Username', [Email(), required()])
    password = PasswordField('Password', [length(min=8, max=30), required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('login', [required()])



class MyForm(FlaskForm):
    city = StringField('city name', [required()])
    submit = SubmitField('search', [required()])


@app.route('/login', methods=['GET'])
def show_login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def submit_login():
    form = LoginForm(request.form)
    if not form.validate():
        return render_template('login.html', form=form), 400

    session['user'] = form.username.data
    return redirect('/')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['user']
    return redirect('/')


@app.route('/search', methods=['GET'])
def show_form():
    form = MyForm()
    return render_template('data.html', form=form)


@app.route('/search', methods=['POST'])
def submit_form():
    form = MyForm(request.form)
    if not form.validate():
        return render_template('data.html', form=form), 400

    city_inserted = form.city.data

    # save city data in the Datastore
    qry = Search.query(Search.city == city_inserted).get()
    if not qry:
        newc = Search(city=city_inserted, counter=1)
        newc.put()
        logging.info('Correctly added {} in the Datastore.'.format(city_inserted))
    else:
        qry.counter = qry.counter+1
        qry.put()
        logging.info('Correctly updated {} in the Datastore.'.format(city_inserted))

    # use AirportsFinder API
    url = 'https://cometari-airportsfinder-v1.p.mashape.com/api/airports/by-text'
    params = urllib.urlencode({'text': city_inserted})
    my_url = '{}?{}'.format(url, params)
    logging.info('My url: {}'.format(my_url))

    req = urllib2.Request(my_url)
    req.add_header('X-Mashape-Key', MASHAPE_KEY)
    req.add_header('Accept', 'application/json')
    urlopen = urllib2.urlopen(req)
    content = urlopen.read()
    risp = make_response(content)
    risp2 = json.loads(content)
    risp.headers['content-type'] = 'application/json;charset=UTF-8'

    # retrieve all the airport info
    list_info = []
    for each in risp2:
        datadic = {}
        datadic['name'] = each['name']
        datadic['code'] = each['code']

        # use TimeZone info API
        url2 = 'https://tehuano-time-zone-v1.p.mashape.com/api2/timezone'
        myurl = '{}/{}/{}'.format(url2, each['location']['latitude'], each['location']['longitude'])
        req2 = urllib2.Request(myurl)
        req2.add_header('X-Mashape-Key', MASHAPE_KEY)
        req2.add_header('Accept', 'application/json')
        urlop = urllib2.urlopen(req2)
        infozone = urlop.read()
        datadic['time zone info'] = infozone
        list_info.append(datadic)
    logging.info('list_info: {}'.format(list_info))

    return render_template('response.html', listinfo=list_info, city=city_inserted)



