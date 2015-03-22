from StringIO import StringIO
from xml.etree.cElementTree import Element, ElementTree

class XMLGenerator(object):
    def to_xml(self, obj):
        root = Element('response')
        self.data_to_xml(root, obj)
        tree = ElementTree(root)
        stream = StringIO()
        tree.write(stream, 'UTF-8')
        return '<?xml version="1.0"?>' + stream.getvalue()

    def data_to_xml(self, parent, data):
        if isinstance(data, (list, tuple)):
            self.list_to_xml(parent, data)
        if isinstance(data, dict):
            self.dict_to_xml(parent, data)
        else:
            parent.text = unicode(data)

    def dict_to_xml(self, parent, dict):
        for key, value in dict.iteritems():
            node = Element(key)
            parent.append(node)
            self.data_to_xml(node, value)

    def list_to_xml(self, parent, list):
        for x in list:
            node = Element('item')
            parent.append(node)
            self.data_to_xml(node, x)