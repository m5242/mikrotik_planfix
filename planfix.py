import requests
import local_settings as settings

planfix_token = settings.planfix_token


def report_get_by_req_id(req_id):
    url = f"https://engineering.planfix.ru/rest/report/status/{str(req_id)}/"
    headers = {
        "Authorization": f"Bearer {planfix_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data["save"]["id"])
        return data["save"]["id"]
    else:
        print(f"Код: {response.status_code}")
        print(response.text)


def report_get_data_by_id(id):
    url = f"https://engineering.planfix.ru/rest/report/26000/save/{str(id)}/data?chunk=0"
    headers = {
        "Authorization": f"Bearer {planfix_token}",
        "Accept": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()


        commands = [
            row["items"][5]["text"]
            for row in data["data"]["rows"]
                if row["type"] == "Normal"
        ]
        return commands

    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)


def generate_report():
    try:
        generate_url = "https://engineering.planfix.ru/rest/report/26000/generate"
        headers = {
            "Authorization": f"Bearer {planfix_token}",
            "Accept": "application/json"
        }

        response = requests.post(generate_url, headers=headers)
        response.raise_for_status()

        generate_data = response.json()

        req_id = generate_data["requestId"]
        print(f"Отчёт успешно создан. ID запроса: {req_id}")
        return req_id

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при генерации отчёта: {str(e)}")
        return (False, None)

