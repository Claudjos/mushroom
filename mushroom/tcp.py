from .core import Collector, Storage


class SynCollector(Collector):

	def __init__(self, storage, targets: list):
		super().__init__(storage)
		self.targets = targets

	def process(self, source_ip: str, data: bytes):
		if data[33] == 2:
			dest_port = (data[22] << 8) + data[23]
			if dest_port in self.targets:
				self.save(
					source_ip, 
					(data[20] << 8 ) + data[21], 
					{
						"ttl": int(data[8]),
						"synsize": int((data[2] << 8) + data[3]),
						"winsize": int((data[34] << 8 ) + data[35])
					}
				)
