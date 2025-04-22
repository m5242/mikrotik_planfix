import requests
import config as settings

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
        print(f"Statuscode: {response.status_code}")
        print(response.text)


def report_get_data_by_id(id, rep_id):
    url = f"https://engineering.planfix.ru/rest/report/{str(rep_id)}/save/{str(id)}/data?chunk=0"
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
        print(f"Error: {response.status_code}")
        print(response.text)


def generate_report(rep_id):
    try:
        generate_url = f"https://engineering.planfix.ru/rest/report/{str(rep_id)}/generate"
        headers = {
            "Authorization": f"Bearer {planfix_token}",
            "Accept": "application/json"
        }

        response = requests.post(generate_url, headers=headers)
        response.raise_for_status()

        generate_data = response.json()

        req_id = generate_data["requestId"]
        print(f"Report created successfully. Request ID: {req_id}")
        return req_id

    except requests.exceptions.RequestException as e:
        print(f"Generation report error: {str(e)}")
        return False, None


def report_get_data_by_id_for_term(id, rep_id):
    url = f"https://engineering.planfix.ru/rest/report/{str(rep_id)}/save/{str(id)}/data?chunk=0"
    headers = {
        "Authorization": f"Bearer {planfix_token}",
        "Accept": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        headers = data['data']['rows'][0]['items']

        task_number_index = next(index for index, item in enumerate(headers) if item['text'] == 'Номер задачи')
        command_index = next(
            index for index, item in enumerate(headers) if item['text'] == 'Команда для маршрутизатора')

        task_numbers = []
        commands = []
        for row in data['data']['rows'][1:]:
            if row['type'] == 'Normal':
                task_numbers.append(row['items'][task_number_index]['text'])
                commands.append(row['items'][command_index]['text'])

        return commands, task_numbers
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None, None


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
        print(f"Executing task failed: {e}")
        return None
