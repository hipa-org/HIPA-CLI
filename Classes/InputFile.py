class InputFile:
    def __init__(self, id, path, folder, name, percentage_limit, cells, cell_count, row_count, total_detected_minutes, content, stimulation_timeframe):
        self.id = id
        self.path = path
        self.folder = folder
        self.name = name
        self.percentage_limit = percentage_limit
        self.cells = cells
        self.cell_count = cell_count
        self.row_count = row_count
        self.total_detected_minutes = total_detected_minutes
        self.content = content
        self.stimulation_timeframe = stimulation_timeframe


