from flask import Flask, json,request
import base64
from hashlib import sha1
import hmac
import binascii
#from datetime import datetime,timedelta
import datetime
import requests
import pytz


base_url="https://timetableapi.ptv.vic.gov.au"
key = b"your api key"
devid="your developer id"

def sign_request(raw):

    raw=raw.encode('utf-8')
    hashed = hmac.new(key, raw, sha1)
    return hashed.hexdigest()

def timeshift(m):
    shifted = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(m))
    shifted=shifted.strftime("%Y-%m-%dT%H:%M:%SZ")
    return str(shifted)


def timezoneshift(td):
    td=datetime.datetime.strptime(td, "%Y-%m-%dT%H:%M:%SZ")
    ttd=td.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Australia/Melbourne"))
    ttd=ttd.strftime ("%Y-%m-%dT%H:%M:%SZ")
    return ttd


app = Flask(__name__)
@app.route('/ptv/bus/')
def get_bus():
    uri="/v3/departures/route_type/2/stop/31824?direction_id=63&look_backwards=false&date_utc="+timeshift(request.args.get("shift"))+"&max_results="+request.args.get("limit")+"&devid="+devid
    signature=sign_request(uri)
    url=base_url+uri+"&signature="+signature
    r=requests.get(url)
    r=r.json()
    shedules=[]
    for t in r["departures"]:
        shedules.append(timezoneshift(t["scheduled_departure_utc"]))
    return json.dumps(shedules)


@app.route('/ptv/train/')
def get_train():
    uri="/v3/departures/route_type/0/stop/1202/route/14?direction_id=1&look_backwards=false&date_utc="+timeshift(request.args.get("shift"))+"&max_results="+request.args.get("limit")+"&devid="+devid
    signature = sign_request(uri)
    url = base_url + uri + "&signature=" + signature
    r = requests.get(url)
    r = r.json()
    shedules = []
    for t in r["departures"]:
        shedules.append(timezoneshift(t["scheduled_departure_utc"]))
    return json.dumps(shedules)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
