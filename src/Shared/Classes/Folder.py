import time
from Shared.Services.Misc import Random


class Folder:
    def __init__(self):
        self.name = Random.get_random_string(12)
        self.created = time.time()
        self.files = []
