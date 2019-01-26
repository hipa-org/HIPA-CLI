from Classes.InputFile import InputFile


def calculate_minutes(file: InputFile):
    file.total_detected_minutes = len(file.cells[0].timeframes) * 3.9 / 60
