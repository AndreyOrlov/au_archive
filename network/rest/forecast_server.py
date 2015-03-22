import httplib
import json
from datetime import date, timedelta
import time

from sklearn import linear_model

def predict(code):
    values = []
    count = 10
    for i in xrange(count, 0, -1):
        try:
            val_date = (date.today() - timedelta(i)).strftime("%d.%m.%Y")
            conn = httplib.HTTPConnection("localhost:8080")
            conn.request("GET", "/rate?code=" + code + "&date=" + val_date, None, {"accept": "application/json"})
            response = conn.getresponse()
            if  response.status == 200:
                dict = json.loads(response.read())
                if len(dict) == 1:
                    val = float(dict[code].replace(",", "."))
                    values.append(val)
        except:
            print "error"

    if len(values) >= 0:
        regr = linear_model.LinearRegression()
        x = [[i] for i in xrange(count)]
        regr.fit(x, values)
        return regr.predict([count + 1])
    return -1

def sent(code, value):
    try:
        conn = httplib.HTTPConnection("localhost:8080")
        conn.request("PUT", "/queries?code=" + code + "&value=" + str(value),
                                None, {"accept": "application/json"})
        response = conn.getresponse()
        response.read()
    except:
        return

def run():
    while True:
        try:
            conn = httplib.HTTPConnection("localhost:8080")
            conn.request("GET", "/queries", None, {"accept": "application/json"})
            response = conn.getresponse()
            dict = json.loads(response.read())
            if dict["queries"] != "empty":
                for code in dict["queries"]:
                    value = predict(code)
                    if value == -1:
                        continue
                    sent(code, value)
        except:
            continue
        time.sleep(5)

if __name__ == "__main__":
    run()