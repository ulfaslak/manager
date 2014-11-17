import numpy
from PIL import Image
import requests
from StringIO import StringIO

def existing_image_ids():
	"""
		Returns an array of existing image hashes
	"""
	try:
		with open('existing_image_ids.csv', 'r') as in_file:
			image_ids = []
			for line in in_file:
				image_ids.append(int(line))
	except:
		image_ids = []

	return image_ids


## UPDATED
def new_image_id(url):
	"""
		Returns the image id.
	"""
	response = requests.get(url)
	img = Image.open(StringIO(response.content))

	image_id = []
	for i, pixel in enumerate(numpy.asarray(img).ravel()):
		if i % 10 == 0:
			image_id.append(str(pixel))
		elif i > 100:
			break

	image_id = int(''.join(image_id))
	return image_id


## UPDATES
def store_image_id(url):
	"""
		Storing the image hash in the hashfile.
	"""
	image_ids		= existing_image_ids()
	image_id 		= new_image_id(url)

	image_ids.append(image_id)

	with open('existing_image_ids.csv', 'w') as out_file:
		for key in image_ids:
			out_file.write(str(key) + "\n")

def is_unique(url):
	"""
		Returns True if image is unique (not a repost), False otherwise.
	"""

	image_ids		= existing_image_ids()
	image_id 		= new_image_id(url)

	if not image_id in image_ids:
		store_image_id(url)
		return True
	else:
		return False
