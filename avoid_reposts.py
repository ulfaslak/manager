import base64
from urllib import urlopen


def image_handler(url):
	img = urlopen(url).read()
	return img


## UPDATED
def get_existing_hashkeys():
	"""
		Returns an array of existing image hashes
	"""
	try:
		with open('existinghashes.csv', 'r') as in_file:
			hashes = []
			for line in in_file:
				hashes.append(int(line))
	except:
		hashes = []

	return hashes


## UPDATED
def image_hashkey(image):
	"""
		Returns the image hashkey.
	"""
	# Relevant if image is stored in local file.
	#with open(image) as shittypic:
	#	string = base64.b64encode(shittypic.read())

	hashkey = hash(image)

	return hashkey


## UPDATES
def store_hashkey(image):
	"""
		Storing the image hash in the hashfile.
	"""
	hashkeys		= get_existing_hashkeys()
	hashkey 		= image_hashkey(image)

	hashkeys.append(hashkey)

	with open('existinghashes.csv', 'w') as out_file:
		for key in hashkeys:
			out_file.write(str(key) + "\n")


def is_unique(image):
	"""
		Returns True if image is unique (not a repost), False otherwise.
	"""
	hashkeys		= get_existing_hashkeys()
	hashkey 		= image_hashkey(image)

	print "Hashkey:", hashkey
	print
	print "Hashkeys:", hashkeys

	if not hashkey in hashkeys or hashkey == 0:
		return True
	else:
		return False

