import paramiko


def connect_via_ssh(host_ip, username, password, port=22):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_ip, port=port, username=username, password=password)
        return ssh
    except Exception as e:
        print(f"Cannot connect to router: {e}")
        return None


def execute_command(ssh, command):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print(f"Error: {error}")
        return output
    except Exception as e:
        print(f"Error while program executed: {e}")
        return None
