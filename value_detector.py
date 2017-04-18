__author__ = 'Nikita'


def get_detected_value(file, base_position, offset):
    file.seek(base_position)
    return file.read(offset).lower()