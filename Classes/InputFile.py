class InputFile:
    def __init__(self, identifier: int, path: str, folder: str, name: str, percentage_limit: float, cells: list, total_detected_minutes: int,
                 content , stimulation_timeframe: int):
        self.id = identifier
        self.path = path
        self.folder = folder
        self.name = name
        self.percentage_limit = percentage_limit
        self.cells = cells
        self.total_detected_minutes = total_detected_minutes
        self.content = content
        self.stimulation_timeframe = stimulation_timeframe


