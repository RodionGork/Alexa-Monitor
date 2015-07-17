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
    q = db.GqlQuery('SELECT * FROM Record ORDER BY timestamp DESC LIMIT 30')
    q.fetch(limit = 30)
    res = []
    for e in q:
        res.append(str(e.timestamp) + ':' + str(e.value))
    return ' '.join(res)

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
