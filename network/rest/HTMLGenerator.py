from StringIO import StringIO
from xml.etree.cElementTree import Element, ElementTree
import cbrf_connection

class HTMLGenerator(object):
    def to_html(self, obj):
        root = Element('body')
        self.data_to_html(root, obj)
        tree = ElementTree(root)
        stream = StringIO()
        tree.write(stream, 'UTF-8')
        return "<html>" + stream.getvalue() + "</html>"

    def data_to_html(self, parent, data):
        if isinstance(data, (list, tuple)):
            self.list_to_html(parent, data)
        elif isinstance(data, dict):
            if data.has_key("content"):
                self.main_page(parent, data["tasks"])
            else:
                self.dict_to_html(parent, data)
        elif data == "img":
            self.img_to_html(parent)
        else:
            parent.text = unicode(data)

    def main_page(self, parent, data):
        node = Element('H1')
        node.text = "Rest Service.  Exchange rates"
        parent.append(node)
        eur = cbrf_connection.getValue("EUR")
        usd = cbrf_connection.getValue("USD")
        self.dict_to_html(parent, { "img": {"EUR": eur, "USD": usd}})
        node = Element("H2")
        node.text = "Tasks:"
        parent.append(node)
        self.tasks_to_html(parent, data)

    def img_to_html(self, parent):
        node = Element('img')
        node.attrib = {"src": "http://upload.wikimedia.org/wikipedia/commons/thumb/1/16/CBRF.png/200px-CBRF.png"}
        parent.append(node)

    def tasks_to_html(self, parent, tasks):
        print tasks
        node = Element("table")
        node.attrib = {"border": "1"}
        for id, (code, date) in tasks.iteritems():
            keyTdNode1 = Element("td")
            self.data_to_html(keyTdNode1, id)
            keyTdNode2 = Element("td")
            self.data_to_html(keyTdNode2, code)
            keyTdNode3 = Element("td")
            self.data_to_html(keyTdNode3, date)
            trNode = Element("tr")
            trNode.attrib = {"valign": "top"}
            trNode.append(keyTdNode1)
            trNode.append(keyTdNode2)
            trNode.append(keyTdNode3)
            node.append(trNode)
        parent.append(node)

    def dict_to_html(self, parent, dict):
        node = Element("table")
        for key, value in dict.iteritems():
            keyTdNode1 = Element("td")
            self.data_to_html(keyTdNode1, key)
            keyTdNode2 = Element("td")
            self.data_to_html(keyTdNode2, value)
            trNode = Element("tr")
            trNode.attrib = {"valign": "top"}
            trNode.append(keyTdNode1)
            trNode.append(keyTdNode2)
            node.append(trNode)
        parent.append(node)

    def list_to_html(self, parent, list):
        for x in list:
            node = Element('p')
            parent.append(node)
            self.data_to_html(node, x)