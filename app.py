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
            del header['ZAP-REDIRECT']
        else:
            the_req['redirect'] = False
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
            return f'''HTTP/1.1 500 ERROR
Server: ZAP-HOSTER-SERVER
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: 88
Content-Type: text/plain
Connection: Closed



ZAP-HOSTER-ERROR : {e}
        '''
    finally:
        pass


#proxies={'http':'http://localhost:8080','https':'https://localhost:8080'},
nn = {'headers':'','content':''}
@app.route('/',methods=['POST','GET'])
def index():
    global ar,nn
    if request.method == 'GET':
        return '''
<img src=https://kasunkodagoda.gallerycdn.vsassets.io/extensions/kasunkodagoda/owasp-zap-scan/2.0.10/1567001746825/Microsoft.VisualStudio.Services.Icons.Default align=center>
<h1> <a href="https://github.com/knassar702/zaphoster">ZAP-HOSTER</a> - Fix Forcing Host header value</h1>
<h4>by: Khaled Nassar <a href="https://github.com/knassar702">@knassar702</h4></a>

    '''
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
            ar = 'HTTP/'+ str(m.raw.version)[0] + '.' + str(m.raw.version)[1] +' '+str(m.status_code) + m.__dict__['reason']+'\n'
            nn['headers'] = ar
            for h,v in m.headers.items():
                ar += f'{h}: {v}\n'
                nn['headers'] += f'{h}: {v}\n'
            ar += '\n\n'
            ar += m.content.decode()
            nn['content'] = '\n\n'+m.content.decode()
            return ar
    return m


@app.route('/l')
def last_req():
     return jsonify(nn)

app.run(host=host,port=port,debug=debug)
