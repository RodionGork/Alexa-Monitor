import flask
import urllib2
import re
import time
from google.appengine.ext import db

class LastRecord(db.Model):
    appid = db.StringProperty()
    value = db.IntegerProperty()

class Record(db.Model):
    appid = db.StringProperty()
    value = db.IntegerProperty(required = True)
    timestamp = db.IntegerProperty(required = True)

app = flask.Flask(__name__)
app.config['DEBUG'] = False

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/list')
def records():
    try:
        limit = int(flask.request.args['points'])
    except:
        limit = 30
    dummy_data = '1438740841:447050 1438708441:447380 1438409640:450395 1438323240:446102' \
            + ' 1438233243:449181 1438146840:466935 1438060442:468417 1437966842:463188' \
            + ' 1437887641:463264 1437808443:463211 1437718440:453469 1437635640:451887' \
            + ' 1437549242:450392 1437455641:450314 1437362041:448258 1437286442:440935' \
            + ' 1437218040:435965 1437135244:457139 1437034444:455177 1437016387:451144'
    if 'localhost' in flask.request.url_root:
        res = dummy_data.split(' ')
        res = res[:limit]
    else:
        q = db.GqlQuery('SELECT * FROM Record ORDER BY timestamp DESC LIMIT ' + str(limit))
        q.fetch(limit = 30)
        res = []
        for e in q:
            res.append(str(e.timestamp) + ':' + str(e.value))
    return flask.Response(' '.join(res), mimetype = 'text/plain')

@app.route('/capture')
def capture():
    resp = urllib2.urlopen('http://www.alexa.com/siteinfo/codeabbey.com')
    page = resp.read()
    m = re.search('ranked\snumber\s([\d\,]+)\sin\sthe\sworld', page)
    rank = int(m.group(1).replace(',', ''))
    q = db.GqlQuery('SELECT * FROM LastRecord')
    lastValue = q.get()
    if lastValue != None:
        prevRank = lastValue.value
    else:
        prevRank = -1
        lastValue = LastRecord()
    if prevRank == rank:
        return 'Not updated'
    lastValue.value = rank
    db.put(lastValue)
    record = Record(value = rank, timestamp = int(time.time()), appid = 'codeabbey')
    record.put()
    return 'New value: ' + str(rank)

@app.route('/update-records')
def updateRecords():
    q = db.GqlQuery('SELECT * FROM Record')
    q.fetch(limit = 30)
    for e in q:
        e.appid = 'codeabbey'
        e.put()
    q = db.GqlQuery('SELECT * FROM LastRecord')
    q.fetch(limit = 30)
    for e in q:
        e.appid = 'codeabbey'
        e.put()
    return 'Successfully updated'

@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, nothing at this URL.', 404
