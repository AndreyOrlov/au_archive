import json
from time import strptime, strftime
import web
import mimerender
from HTMLGenerator import HTMLGenerator
from XMLGenerator import XMLGenerator
import cbrf_connection

tasks = {}
tasksCounter = 0
forecasts = {}
queries = set()

mimerender = mimerender.WebPyMimeRender()
xmlTree = XMLGenerator()
htmlTree = HTMLGenerator()

render_xml = lambda **args: xmlTree.to_xml(args)
render_json = lambda **args: json.dumps(args)
render_html = lambda **args: htmlTree.to_html(args)

urls = (
    '/', 'Root' ,
    '/task([0-9]*)', 'Task',
    '/rate', 'Rate',
    '/forecast', 'Forecast',
    '/queries', 'Query'
)

app = web.application(urls, globals())

class Root:
    @mimerender (
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def OPTIONS(self):
        web.header('Allow', 'GET, PUT')
        return {"PUT": {"description": "Create task",
                        "parameters": {
                                "code": {"description": "code", "type": "string"},
                                "date": {"description": "date in format dd.mm.yyyy", "type": "string"}}},
                "GET": {"description": "start page"}
               }

    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def PUT(self):
        i = web.input()
        code = i.get("code", None)
        date = i.get("date", None)
        if code is None or date is None:
            raise web.badrequest()
        try:
            struct_time = strptime(date, "%d.%m.%Y")
        except ValueError:
            raise web.badrequest()
        date = strftime("%d.%m.%Y", struct_time)
        global tasksCounter
        global tasksQueue
        id = tasksCounter
        tasksCounter += 1
        tasks[id] = (code, date)
        return {'task_id': id}

    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def GET(self):
        return {"content": "main_page", "tasks": tasks}

class Rate:
    @mimerender (
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def OPTIONS(self):
        web.header('Allow', 'GET')
        return {"GET": {"description": "Create task",
                        "parameters": {
                                "code": {"description": "code", "type": "string"},
                                "date": {"description": "date in format dd.mm.yyyy", "type": "string"}}},
               }

    @mimerender (
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def GET(self):
        i = web.input()
        code = i.get("code")
        date = i.get("date")
        if code is None:
            raise web.badrequest()
        value = cbrf_connection.getValue(code, date)
        if value is None:
            raise  web.notfound()
        return {code: value}

class Task:
    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def OPTIONS(self, id):
        web.header('Allow', 'GET, DELETE, POST')
        return {"GET": {"description": "Get task: difference between current date and saved",
                            "parameters": {"id": {"type": "int"}}},
                "DELETE": {"description": "Delete task", "parameters": {"id": {"type": "int"}}},
                "POST": {"description": "update task",
                         "parameters": {"id": {"type": "int"}, "code":{"type": "string"},
                                        "date": {"description": "date in format dd.mm.yyyy", "type": "string"} }}
                }

    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def GET(self, id):
        id = int(id)
        date = None
        code = None
        if tasks.has_key(id):
            (code, date) = tasks[id]
        if code is None:
            return {'error': 'task not found'}
        value1 = float(cbrf_connection.getValue(code, date).replace(',', "."))
        value2 = float(cbrf_connection.getValue(code).replace(',', "."))
        if value1 is None or value2 is None:
            raise web.notfound()

        return {'difference': str(value2 - value1)}

    @mimerender (
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def DELETE(self, id):
        id = int(id)
        if tasks.has_key(id):
            del tasks[id]
        else:
            raise web.notfound()
        return {'status': "deleted"}

    @mimerender (
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def POST(self, id):
        id = int(id)
        i = web.input()
        code = i.get("code", None)
        date = i.get("date", None)
        print code, date
        if code is None or date is None:
            raise web.badrequest()
            return {"error": "wrong parameters"}
        if tasks.has_key(id):
            tasks[id] = (code, date)
            status = "updated"
        else:
            raise web.notfound()
            status = "task not found"
        return {'status': status}

class Forecast:
    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def OPTIONS(self):
        web.header('Allow', 'GET')
        return {"GET": {"description": "Forecast for selected currency ",
                            "parameters": {"code": {"type": "string"}}},
                }

    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def GET(self):
        i = web.input()
        code = i.get("code")
        if code is None:
            raise web.notfound()
        if forecasts.has_key(code):
            return {"predicted value": forecasts[code]}
        else:
            queries.add(code)
            return {"status": "request is not ready"}

class Query:
    @mimerender (
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def OPTIONS(self):
        web.header('Allow', 'PUT, GET')
        return {"PUT": {"description": "Create task",
                        "parameters": {
                                "code": {"description": "currency code", "type": "string"},
                                "value": {"description": "predicted value of currency", "type": "string"}}},
                "GET": {"description": "get created queries"}
               }

    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def GET(self):
        if len(queries) == 0:
            return {"queries":"empty"}
        else:
            list_queries = list(queries)
            queries.clear()
            return {"queries": list_queries}

    @mimerender(
        not_acceptable_callback=lambda _, sup: (
            'text/plain',
            'Available Content Types: ' + ', '.join(sup)
        ),
        html=render_html,
        xml=render_xml,
        json=render_json,
    )
    def PUT(self):
        i = web.input()
        code = i.get("code", None)
        code = code.encode('ascii','ignore')
        value = i.get("value", None)
        if code is None or value is None:
            raise web.badrequest()
        forecasts[code] = value
        return {"status": "OK"}

if __name__ == "__main__":
    app.run()