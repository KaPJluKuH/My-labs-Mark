import requests
import json

url = "http://127.0.0.1:8080/"


class CrudApi:
    @staticmethod
    def get_by_id(id: int):
        response = requests.get(url + "get_by_id/" + str(id))
        json_res = response.json()
        return json_res

    @staticmethod
    def select_range(ids: [int]):
        response = requests.get(url + "select_by_ids", json={"ids": ids})
        json_res = response.json()
        return json_res

    @staticmethod
    def delete_range(ids: [int]):
        response = requests.post(url + "delete_by_id", json={"ids": ids})
        if response.ok:
            json_res = {"status": "Запись в таблице удалена."}
        else:
            json_res = {"status": "Невозможно удалить запись."}
        return json.dumps(json_res)

    @staticmethod
    def insert_row(users: [str]):
        cols = ["title", "date", "link", "src", "base64"]
        response = requests.post(url + "create", json={"columns": cols, "values": users})
        return response.status_code

    @staticmethod
    def update_row(id: int, cols: [str], vals: [str]):
        response = requests.post(url + "update", json={"columns": cols, "values": vals, "predicate": f"rowid = {id}", "download": True})
        return response.status_code
