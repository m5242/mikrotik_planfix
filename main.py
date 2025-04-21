import time

import schedule

from mikrotik import *
from planfix import *

status_id_dp = settings.status_id_dp
host_ip = settings.host_ip
username = settings.username
password = settings.password
granting_access_report_id = settings.granting_access_report_id
terminating_access_report_id = settings.terminating_access_report_id
status_id_fin = settings.status_id_fin


def granting_access():
    try:
        print(f"Запуск granting_access в {time.strftime('%Y-%m-%d %H:%M:%S')}")
        req_id = generate_report(granting_access_report_id)
        time.sleep(10)

        status_id = report_get_by_req_id(req_id)
        time.sleep(1)

        commands = report_get_data_by_id(status_id, granting_access_report_id)[0]
        list_id_of_task = report_get_data_by_id(status_id, granting_access_report_id)[1]

        time.sleep(1)
        command_final = "\n".join(commands)

        ssh = connect_via_ssh(host_ip, username, password)
        if ssh:
            output = execute_command(ssh, command_final)
            if output is not None:
                print("response from router: ")
                print(output.strip() if output else "")
            ssh.close()
        else:
            print("Не удалось подключиться")

        time.sleep(1)
        for ids in list_id_of_task:
            print(ids)
            status_changing(ids, status_id_dp)
        print("Скрипт granting_access отработал.\n\n")
    except Exception as e:
        print(f"Ошибка при выполнении скрипта: {e}\n\n")


def terminating_access():
    try:
        print(f"Запуск terminating_access в {time.strftime('%Y-%m-%d %H:%M:%S')}")
        req_id = generate_report(terminating_access_report_id)
        time.sleep(10)

        status_id = report_get_by_req_id(req_id)
        time.sleep(1)

        commands = report_get_data_by_id_for_term(status_id, terminating_access_report_id)[0]
        list_id_of_task = report_get_data_by_id_for_term(status_id, terminating_access_report_id)[1]

        time.sleep(1)
        command_final = "\n".join(commands)

        ssh = connect_via_ssh(host_ip, username, password)
        if ssh:
            output = execute_command(ssh, command_final)
            if output is not None:
                print("response from router: ")
                print(output.strip() if output else "")
            ssh.close()
        else:
            print("Не удалось подключиться")

        time.sleep(1)
        for ids in list_id_of_task:
            print(ids)
            status_changing(ids, status_id_fin)
        print("Скрипт terminating_access отработал.\n\n")
    except Exception as e:
        print(f"Ошибка при выполнении скрипта: {e}\n\n")


schedule.every(1).hours.do(granting_access)
schedule.every(24).hours.do(terminating_access)


granting_access()
time.sleep(11*60)
terminating_access()


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(15)
