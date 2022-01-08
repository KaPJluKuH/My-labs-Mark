from bottle import route, run, template, get, post, request
import json

from DbContextSingle import SingleContext

context = SingleContext("parserDb.db")


@get("/get_by_id/<id>")
def get_by_id(id):
    res = context.get_instance().Select("article_data_images", f"rowid = {id}")
    return json.dumps(res)


@get("/select_by_ids")
def select_by_id():
    ids = request.json['ids']
    predicate = "1=1" if len(ids) == 0 else f"rowid in ({','.join(ids)})"
    # print(predicate)
    return json.dumps(context.get_instance().Select("article_data_images", predicate))


@post("/delete_by_id")
def delete_by_id():
    ids = request.json['ids']
    context.get_instance().Delete("article_data_images", f'rowid in ({",".join(ids)})')


@post("/truncate")
def truncate():
    table_name = request.json['table_name']
    context.get_instance().Delete(table_name)


@post("/create")
def create_row():
    download = "download" in request.params and request.params['download'] == "true"
    pars = request.json
    cols = pars['columns']
    vals = pars['values']
    context.get_instance().Insert("article_data_images", cols, vals, download)


@post("/update")
def update_row():
    download = "download" in request.params and request.params['download'] == "true"
    cols = request.json['columns']
    vals = request.json['values']
    predicate = request.json['predicate']
    context.get_instance().Update("article_data_images", cols, vals, predicate, download)


# Как по другому создавать таблицу из клиента?
# Может редактирование схемы не должно быть в этом интерфейсе?
def create_table():
    table_name = "article_data_images"
    columns = (('title', 'TEXT', ('NOT NULL',)),
                ('date', 'TEXT', ('NOT NULL',)),
                ('link', 'TEXT', ('PRIMARY KEY', 'NOT NULL')),
                ('src', 'TEXT', ('NOT NULL',)),
                ('base64', 'BLOB', ('NOT NULL',)))
    context.get_instance().CreateTable(table_name, columns)

try:
    create_table()
    run()
except:
    context.get_instance().Disconnect()
