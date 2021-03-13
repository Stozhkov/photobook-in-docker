import io
import random

from PIL import Image


def generate_photo_file(file_name):
    """
    Generate picture for test.
    :param file_name:
    :return Image object:
    """
    file = io.BytesIO()
    image = Image.new('RGBA', size=(600, 400), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = file_name
    file.seek(0)
    return file


def generate_file_name() -> str:
    """
    Generate file name for test.
    :return file name:
    """
    file_name = ''

    for i in range(5):
        file_name += random.choice("wertyupasdfghkzxcvbnm")

    return file_name + '.png'
