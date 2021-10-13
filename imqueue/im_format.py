from enum import Enum
import cv2

class ImFormat(Enum):
    PNG = 0,
    JPG = 1,

def formatToString(format: ImFormat) -> str:
    if format == ImFormat.PNG:
        return '.png'
    elif format == ImFormat.JPG:
        return '.jpg'
    raise Exception('Unknown format in formatToString().')

def formatToCVFormat(format: ImFormat):
    if format == ImFormat.PNG:
        return [cv2.IMWRITE_PNG_COMPRESSION, 0]
    elif format == ImFormat.JPG:
        return [cv2.IMWRITE_JPEG_QUALITY, 100]
    raise Exception('Unknown format in formatToCVFormat().')