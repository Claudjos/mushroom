from . import SOCKET_PATH, COLLECTION_TCP_SYN
from json import loads
from uuid import uuid4
from os import unlink
import socket


class Client:

	def __init__(self):
		self.sock_name = "/tmp/{}.sock".format(uuid4())
		self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.sock.bind(self.sock_name)

	def get_syn_data(self, ip: str, port: int) -> dict:
		"""
		TODO
			- set timeout
		"""
		self.sock.sendto(
			"{};{}:{}".format(
				COLLECTION_TCP_SYN,
				ip,
				str(port)
			).encode(),
			SOCKET_PATH
		)
		return loads(self.sock.recv(1024).decode())

	def __del__(self):
		unlink(self.sock_name)
