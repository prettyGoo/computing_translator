__author__ = 'Nikita'


def get_detected_value(file, base_position, offset, detect_with_split=False):
    file.seek(base_position)
    if not detect_with_split:
        return file.read(offset).lower()
    else:
        value = file.read(offset).lower()
        value = value.replace(' ', '')
        value = value.replace('\t', '')
        value = value.replace('\n', '')
        return value
