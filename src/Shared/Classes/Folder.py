import time
from Shared.Services.Misc import Random


class Folder:
    def __init__(self, name=None, files=None):
        if name is None:
            self.name = Random.get_random_string(12)
        else:
            self.name = name

        self.created = time.time()

        if files is None:
            self.files = []
        else:
            self.files = files
