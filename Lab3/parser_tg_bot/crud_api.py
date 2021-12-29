import requests
import json

url = "http://127.0.0.1:8080/"


class CrudApi:
    @staticmethod
    def get_by_id(id: int):
        # print(id)
        response = requests.get(url + "get_by_id/" + str(id))
        # print(response)
        json_res = response.json()
        # print(json_res)
        return json_res

    @staticmethod
    def select_range(ids: [int]):
        # print(ids)
        response = requests.get(url + "select_by_ids", json={"ids": ids})
        # print(response)
        json_res = response.json()
        # print(json_res)
        return json_res

    @staticmethod
    def delete_range(ids: [int]):
        # print(ids)
        response = requests.post(url + "delete_by_id", json={"ids": ids})
        # print(response)
        if response.ok:
            json_res = {"status": "Oki"}
        else:
            json_res = {"status": "ERROR"}
        return json.dumps(json_res)

    # @staticmethod
    # def insert_one():
    #     if:
    #         json_res = {"status": "Oki"}
    #     else:
    #
    #     return json.dumps(json_res)

