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


        headers = data['data']['rows'][0]['items']
        column_index = next(index for index, item in enumerate(headers) if item['text'] == 'Номер задачи')

        task_numbers = []
        for row in data['data']['rows'][1:]:
            if row['type'] == 'Normal':
                task_numbers.append(row['items'][column_index]['text'])

        commands = [
            row["items"][5]["text"]
            for row in data["data"]["rows"]
                if row["type"] == "Normal"
        ]
        return commands, task_numbers
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


def status_changing(task_id, status_id):
    url = f"https://engineering.planfix.ru/rest/task/{task_id}"

    headers = {
        "Authorization": f"Bearer {planfix_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {"silent": "false"}

    payload = {
        "status": {
            "id": status_id
        }
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            params=params,
            json=payload
        )
        response.raise_for_status()
        print(response.json())
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Ошибка выполнения запроса: {e}")
        return None
