import requests
import json

url = "http://127.0.0.1:8080/"


class CrudApi:
    @staticmethod
    def select_range(ids: [int]):
        print(ids)
        response = requests.get(url + "select_by_ids", json={"ids": ids})
        print(response)
        json_res = response.json()
        return json_res

    @staticmethod
    def delete_range(ids: [int]):
        print(ids)
        response = requests.post(url + "delete_by_id", json={"ids": ids})
        print(response)
        if response.ok:
            json_res = {"status": "Oki"}
        else:
            json_res = {"status": "ERROR"}
        return json.dumps(json_res)
