from . import SOCKET_PATH, COLLECTION_TCP_SYN
from json import loads
from uuid import uuid4
from os import unlink
from select import select
import socket


class Client:

	def __init__(self):
		self.sock_name = "/tmp/{}.sock".format(uuid4())
		self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		self.sock.bind(self.sock_name)

	def get_syn_data(self, ip: str, port: int) -> dict:
		"""
		RAISES
			FileNotFoundError: if server UNIX socket does not exists.
		"""
		self.sock.sendto(
			"{};{}:{}".format(
				COLLECTION_TCP_SYN,
				ip,
				str(port)
			).encode(),
			SOCKET_PATH
		)
		# Wait one second for the response
		rl, wl, xl = select([self.sock],[],[], 1)
		if rl == []:
			return None
		else:
			return loads(self.sock.recv(1024).decode())

	def __del__(self):
		unlink(self.sock_name)
