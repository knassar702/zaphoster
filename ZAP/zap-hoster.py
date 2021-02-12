# The sendingRequest and responseReceived functions will be called for all
# requests/responses sent/received by ZAP, including automated tools (e.g.
# active scanner, fuzzer, ...)

# Note that new HttpSender scripts will initially be disabled
# Right click the script in the Scripts tree and select "enable"

# 'initiator' is the component the initiated the request:
#      1   PROXY_INITIATOR
#      2   ACTIVE_SCANNER_INITIATOR
#      3   SPIDER_INITIATOR
#      4   FUZZER_INITIATOR
#      5   AUTHENTICATION_INITIATOR
#      6   MANUAL_REQUEST_INITIATOR
#      7   CHECK_FOR_UPDATES_INITIATOR
#      8   BEAN_SHELL_INITIATOR
#      9   ACCESS_CONTROL_SCANNER_INITIATOR
#     10   AJAX_SPIDER_INITIATOR
# For the latest list of values see the HttpSender class:
# https://github.com/zaproxy/zaproxy/blob/master/zap/src/main/java/org/parosproxy/paros/network/HttpSender.java
# 'helper' just has one method at the moment: helper.getHttpSender() which
# returns the HttpSender instance used to send the request.
#
# New requests can be made like this:
# msg2 = msg.cloneAll() # msg2 can then be safely changed without affecting msg
# helper.getHttpSender().sendAndReceive(msg2, false)
# print('msg2 response code =' + msg2.getResponseHeader().getStatusCode())

"""
ZAP-HOSTER : Change Host header value in zaproxy | by: khaled nassar @knassar702
add this script in httpsender tab :D
bye
"""
import os,re,json
from base64 import b64encode

host = 'localhost:3051'

'''
GET https://knassar702.github.io/ HTTP/1.1
Host: knassar702.github.io
User-agent: Firefox test
For Change host header
---
GET https://knassar702.github.io/
Host: knassar702.github.io
User-agent: Firefox test
ZAP-HOST: localhost
ZAP-HOST will be removed and the host header will be change to his value
GET https://knassar702.github.io/ HTTP/1.1
Host: localhost
User-agent: Firefox test
----
follow redirects with  ZAP-REDIRECT header
GET https://knassar702.github.io/
Host: knassar702.github.io
User-agent: Firefox test
ZAP-HOST: localhost
ZAP-REDIRECT: anything
'''

def sendingRequest(msg, initiator, helper):
    header = msg.getRequestHeader().toString().replace('\r','')
    body = msg.getRequestBody().toString()
    method = header.partition('\n')[0].split(' ')
    req = {'method':method[0],
'url':method[1],
'data':body,
'redirect':False,
'headers':header
}
#for
    js = json.dumps(req,indent=4)
    r = b64encode(js)
    cmd = "curl {} -d the_req='{}'".format(host,r)
    print('Execute :> $  '+cmd)
    f = os.popen(cmd).read()
   # print('--------------\nOUTPUT:\n')
   # print(f) 



def responseReceived(msg, initiator, helper):
    # Debugging can be done using print like this
    o = os.popen('curl {}/l'.format(host)).read()
    j = json.loads(o)
    msg.setResponseHeader(j['headers'])
    msg.setResponseBody(j['content'])
