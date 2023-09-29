import paramiko

from src.server.base import ServerBase
from src.server.interface import SshServerInterface
from src.shell.shell import Shell
import logging


class SshServer(ServerBase):
    def __init__(self, host_key_file, host_key_file_password=None):
        super(SshServer, self).__init__()
        self._host_key = paramiko.RSAKey.from_private_key_file(host_key_file, host_key_file_password)
        self._session_map = {}

    @staticmethod
    def _get_session_id(addr):
        return "{}-{}".format(*addr)

    def add_session(self, addr, client, session, server_interface, client_shell):
        self._session_map[self._get_session_id(addr)] = {
            'cl': client,
            'se': session,
            'in': server_interface,
            'sh': client_shell,
        }

    def get_session(self, addr):
        key = self._get_session_id(addr)
        if key in self._session_map:
            return self._session_map[self._get_session_id(addr)]
        else:
            raise KeyError(f"{addr} does not exist in record")

    def remove_session(self, addr):
        key = self._get_session_id(addr)
        if key in self._session_map:
            del self._session_map[key]

    def connection_function(self, client, addr):
        logger = logging.getLogger()
        logger.info(f"{client} {addr} connected")
        try:
            session = paramiko.Transport(client)
            session.add_server_key(self._host_key)
            server_interface = SshServerInterface()
            try:
                session.start_server(server=server_interface)

            except paramiko.SSHException:
                return

            channel = session.accept()
            stdio = channel.makefile('rwU')

            client_shell = Shell(stdio, stdio)

            self.add_session(addr, client, session, server_interface, client_shell)

            client_shell.cmdloop()

            session.close()
        except Exception as e:
            raise e
        finally:
            self.remove_session(addr)
            logger.info(f"{addr} disconnected")
