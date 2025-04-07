import paramiko
import local_settings as settings


def connect_via_ssh(host_ip, username, password, port=22):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_ip, port=port, username=username, password=password)
        return ssh
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None


def execute_command(ssh, command):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print(f"Ошибка: {error}")
        return output
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")
        return None


def main():
    host_ip = settings.host_ip
    username = settings.username
    password = settings.password
    command = input("type command: ")

    ssh = connect_via_ssh(host_ip, username, password)
    if ssh:
        output = execute_command(ssh, command)
        if output is not None:
            print("response: ")
            print(output.strip() if output else "")
        ssh.close()
    else:
        print("Не удалось подключиться")


if __name__ == "__main__":
    main()
