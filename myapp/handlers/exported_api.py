from myapp.flask_app import app, csrf_protect
from flask import make_response, request
from myapp.models.search import Search
import json
import logging


def raise_error(message='An error occured during a request', errcode=500):
    json_response = {}
    json_response['data'] = []
    json_response['status'] = 'Bad Request'
    json_response['message'] = message
    resp = make_response(json.dumps(json_response, ensure_ascii=True), errcode)
    resp.headers['content-type'] = 'application/json'
    return resp


@app.route('/api/v1.0/stats', methods=['GET'])
def showpop():
    qry = Search.query().order(-Search.counter).fetch(3)
    my_data = []
    for each in qry:
        datadic={}
        datadic['city'] = each.city
        datadic['counter'] = each.counter
        my_data.append(datadic)

    json_response = {}
    json_response['data'] = my_data
    json_response['status'] = 'OK'
    json_response['message'] = 'Succesfully returned the resource.'
    resp = make_response(json.dumps(json_response, ensure_ascii=True), 200)
    resp.headers['content-type'] = 'application/json'
    return resp


@csrf_protect.exempt
@app.route('/api/v1.0/insert', methods=['POST'])
def insert():
    params = request.args
    required_parameters = ['city']

    for r in required_parameters:
        if r not in params:
            return raise_error(message='Missing {} parameter'.format(r), errcode=400)

    city_name = request.args.get('city')
    print city_name
    qry = Search.query(Search.city == city_name).get()
    print qry
    if not qry:
        newc = Search(city=city_name, counter=1)
        newc.put()
        logging.info('Correctly added {} in the Datastore.'.format(city_name))
        json_response = {}
        json_response['status'] = 'OK'
        json_response['message'] = ('Succesfully inserted %s in the Datastore.' % city_name)
        resp = make_response(json.dumps(json_response, ensure_ascii=True), 200)
        resp.headers['content-type'] = 'application/json'
        return resp
    else:
        return raise_error(message='Error: city cannot be saved.', errcode=400)
