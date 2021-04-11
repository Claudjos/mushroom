from json import dumps


class Storage:
	"""
	TODO:
		- add memory clean up policy
	"""
	def __init__(self):
		self.collections = {}

	def set(self, collection: str, key: str, value: dict):
		self.collections[collection][key] = value
		print("SET", collection, key, value, flush=False)

	def get(self, collection: str, key: str) -> dict:
		print("GET", collection, key, flush=False)
		return self.collections.get(collection, {}).get(key, {})

	def get_handler(self, collection: str):
		self.collections.setdefault(collection, {})
		return StorageHandler(self, collection)

	def handle_request(self, request: bytes) -> bytes:
		collection, key = request.decode().split(";")
		value = self.get(collection, key.strip())
		return dumps(value).encode()


class StorageHandler:

	def __init__(self, storage: Storage, collection: str):
		self.storage = storage
		self.collection = collection

	def save(self, key: str, value: dict):
		return self.storage.set(self.collection, key, value)


class Collector:

	def __init__(self, storage: Storage):
		self.storage = storage

	def save(self, source_ip: str, source_port: int, value: dict):
		self.storage.save(
			self.make_key(source_ip, source_port),
			value
		)

	@classmethod
	def make_key(cls, source_ip: str, source_port: int):
		return f"{source_ip}:{source_port}"

	def process(self, source_ip: str, data: bytes):
		pass
