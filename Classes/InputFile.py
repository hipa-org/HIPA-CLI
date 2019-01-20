class InputFile:
    def __init__(self, identifier, path, folder, name, percentage_limit, cells, total_detected_minutes,
                 content, stimulation_timeframe):
        self.id = identifier
        self.path = path
        self.folder = folder
        self.name = name
        self.percentage_limit = percentage_limit
        self.cells = cells
        self.total_detected_minutes = total_detected_minutes
        self.content = content
        self.stimulation_timeframe = stimulation_timeframe


