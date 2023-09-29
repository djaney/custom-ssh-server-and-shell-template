from src.server.server import SshServer


if __name__ == '__main__':
    my_shell = SshServer("<home>/.ssh/id_rsa")
    my_shell.start(port=2222)
