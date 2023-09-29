import paramiko

from src.server.base import ServerBase
from src.server.interface import SshServerInterface
from src.shell.shell import Shell


class SshServer(ServerBase):
    def __init__(self, host_key_file, host_key_file_password=None):
        super(SshServer, self).__init__()
        self._host_key = paramiko.RSAKey.from_private_key_file(host_key_file, host_key_file_password)

    def connection_function(self, client):
        try:
            session = paramiko.Transport(client)
            session.add_server_key(self._host_key)

            server = SshServerInterface()
            try:
                session.start_server(server=server)
            except paramiko.SSHException:
                return

            channel = session.accept()
            stdio = channel.makefile('rwU')

            self.client_shell = Shell(stdio, stdio)
            self.client_shell.cmdloop()

            session.close()
        except:
            pass