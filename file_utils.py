import io

import pyheif
from PIL import Image


def convert_image_from_heic_to_jpeg(bytesIo):
    i = pyheif.read_heif(bytesIo)

    # Convert to other file format like jpeg
    s = io.BytesIO()
    pi = Image.frombytes(
        mode=i.mode, size=i.size, data=i.data)

    pi.save(s, format="jpeg")

    return s
