from src.server.server import SshServer
import sys

if __name__ == '__main__':
    my_shell = SshServer(sys.argv[1])
    my_shell.start(port=int(sys.argv[2]))
