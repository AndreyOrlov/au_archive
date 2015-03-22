import urllib2
from xml.etree import cElementTree as ET

def getValue(code, date = None):
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    if not date is None:
        url += "?date_req=" + date
    xml = ET.fromstring(urllib2.urlopen(url).read())

    for el in xml.getiterator("Valute"):
        if el[1].text == code:
            return el[4].text
    return None
