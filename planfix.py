import requests


def test_api():
    url = "https://engineering.planfix.ru/rest/report/26000/save/5388/data?chunk=0"
    # url = "https://engineering.planfix.ru/rest/report/26000/generate"
    # url = "https://engineering.planfix.ru/rest/report/26000/generate"
    headers = {
        "Authorization": "Bearer 92887b05010d215da04742e2031491fd",
        "Accept": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        header_row = next(row for row in data["data"]["rows"] if row["type"] == "Header")
        column_index = next(
            index for index, item in enumerate(header_row["items"])
            if item["text"] == "Команда для маршрутизатора"
        )

        commands = []
        for row in data["data"]["rows"]:
            if row["type"] != "Header":
                command = row["items"][column_index]["text"]
                commands.append(command)
                print(command)

    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)