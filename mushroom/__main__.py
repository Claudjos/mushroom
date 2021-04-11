from . import COLLECTION_TCP_SYN, SOCKET_PATH
from .core import *
from .tcp import *
from os import unlink
from select import select
import socket
import sys


if __name__ == "__main__":

	if len(sys.argv) < 2:
		print("Too few parameters", flush=True)
		exit(1)

	# Parse target ports
	SYN_PORTS = list(map(lambda x: int(x), sys.argv[1].split(",")))
	print("Collecting SYN data for ports: {}".format(", ".join(map(lambda x: str(x), SYN_PORTS))))

	# Initialize storage and collectors
	storage = Storage()
	collectors = [
		SynCollector(storage.get_handler(COLLECTION_TCP_SYN), SYN_PORTS),
	]

	# Raw socket to sniff traffic
	rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
	rawsocket.setblocking(0)

	# UDP UNIX socket to retrieve data
	server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	server.setblocking(0)
	server.bind(SOCKET_PATH)

	try:

		while True:

			rl, wl, xl = select([rawsocket, server],[],[])

			if rawsocket in rl:
				data, source = rawsocket.recvfrom(65565)
				for collector in collectors:
					collector.process(source[0], data)

			if server in rl:
				try:
					data, addr = server.recvfrom(1024)
					server.sendto(storage.handle_request(data), addr)
				except Exception as e:
					print(e, flush=False)

	except KeyboardInterrupt as e:
		pass
	except Exception as e:
		print(e, flush=True)
	finally:
		unlink(SOCKET_PATH)
