#!/usr/bin/env python3

from flask import Flask,jsonify,request
from base64 import b64decode as dc
import requests,re,json


host = 'localhost'
port = 3051
debug = False

requests.packages.urllib3.disable_warnings()


app = Flask(__name__)


def geth(headers):
    headers = headers.replace('\\n', '\n')
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers


def make_req(the_req):
    try:
        header = geth(the_req['headers'])
        if 'ZAP-HOST' in header:
            header['Host'] = header['ZAP-HOST']
            del header['ZAP-HOST']
        if 'ZAP-REDIRECT' in header:
            the_req['redirect'] = True
#            print(the_req)
            del header['ZAP-REDIRECT']
        else:
            the_req['redirect'] = False
            #print(header)
#        print(header)
        r = requests.Request(the_req['method'],the_req['url'],data=the_req['data'],headers=header)
        se = requests.Session()
        req = r.prepare()
        try:
            v = se.send(
                req,
                verify=False,
                timeout=20,
                allow_redirects=the_req['redirect']
                )
            return v
        except Exception as e:
            return f'ZAP-HOSTER:> {e}'
    finally:
        pass


#proxies={'http':'http://localhost:8080','https':'https://localhost:8080'},
@app.route('/',methods=['POST'])
def index():
    r = request.form
    ar = ''
    req = r['the_req']
    req = dc(req)
    req = json.loads(req)
    #make_req(req)
    #return 'hi'
    m = make_req(req)
    if 'content' in dir(m):
        if 'ZAP-H' not in m.content.decode():
            for h,v in m.headers.items():
                ar += f'{h}: {v}\n'
            ar += m.content.decode()
            return ar
    return 'gg'

 

app.run(host=host,port=port,debug=debug)
