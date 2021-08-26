import cv2
from io import BytesIO
from PIL import Image
import requests

class ImageHandler(object):

	def read_image(image_path):
		image = Image.open(requests.get(image_path, stream = True).raw)
		return image