import time
import local_settings as settings
from planfix import *
from mikrotik import *


def main():

    status_id_dp = settings.status_id_dp
    host_ip = settings.host_ip
    username = settings.username
    password = settings.password

    req_id = generate_report()
    time.sleep(10)

    status_id = report_get_by_req_id(req_id)
    time.sleep(1)

    commands = report_get_data_by_id(status_id)[0]
    list_id_of_task = report_get_data_by_id(status_id)[1]

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


if __name__ == "__main__":
    main()
