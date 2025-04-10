import local_settings as settings
from planfix import *
from mikrotik import *


def main():
    test_api()
    # host_ip = settings.host_ip
    # username = settings.username
    # password = settings.password
    # planfix_token = settings.planfix_token
    # planfix_username = settings.planfix_username
    # command = input("type command: ")
    #
    # ssh = connect_via_ssh(host_ip, username, password)
    # if ssh:
    #     output = execute_command(ssh, command)
    #     if output is not None:
    #         print("response: ")
    #         print(output.strip() if output else "")
    #     ssh.close()
    # else:
    #     print("Не удалось подключиться")


if __name__ == "__main__":
    main()
