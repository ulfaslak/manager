import pytumblr
#import sys
from twitter_manager import *
from location_coordinates import *
#import sys
#from bs4 import BeautifulSoup
#import urllib2
#from lxml import html
#import requests

tu = pytumblr.TumblrRestClient(
	'1e6SLA3EPSA6buqX7yeDYEMr0pACheY6d0SwSkGgvYjS4Gu5Tm',
	'dPX00RMbuosaxDSyWDs7RwELDoIT06C0FfQZtxbBZxWaCkotbd',
)

hashtag_bag = """#fitness #lifestyle #nutrition #motivation #fitfam #healthy #wellness 
#fitblr #fitnessmotivation #life #inspiration #workoutmotivation #training #fitspo #fit
#fitspiration #workhard #trainhard #inshape #endurance #healthyliving #eatclean
"""

hashtag_list = hashtag_bag.split()

def scrape_tum_pic_urls(user):
	"""
		Scraping: 'thefitnessquotes', 'healthy-life-style-forever', 'visionsthroughmyeyes'
		'beliveinyourselffrv' 'tru1tru' 'fitness-quotes'
	"""

	print "Scraping %s" % user


	try:
		with open('image_urls.csv', 'r') as in_file:
			image_urls = in_file.read().split(',')

	except IOError:
		print "No existing record of images. Making new record."
		image_urls = []
	

	for _page in range(2,500):

		print "Scraping page %d" % _page

		url 		= 'http://%s.tumblr.com/page/%d' % (user, _page)
		response 	= urllib2.urlopen(url)
		html 		= response.read()
		soup 		= BeautifulSoup(html)

		scraped_ims	= [ link.get('src') for link in soup.find_all('img') ]
		cleaned_ims = filter(lambda x: x[-3:] == 'jpg', scraped_ims)

		if len(cleaned_ims) == 0:
			print "Found no more images on page %d. Exitting." % _page
			break


		for link in cleaned_ims:
			print link
			image_urls.append(link)

	
	image_urls = list(set(image_urls))

	with open('image_urls.csv', 'w') as out_file:
		for url in image_urls:
			if url != image_urls[-1]:
				out_file.write(url + ',')
			else:
				out_file.write(url)



def post_from_stored_images():
	
	shuffle(hashtag_list)
	hashtags = hashtag_list[:randrange(2,5)]
	title = '#dailymotivation ' + ' '.join(hashtags)

	with open('image_urls.csv', 'r') as in_file:
		image_urls = in_file.read().split(',')

	url = image_urls[-1]

	with open('image_urls.csv', 'w') as out_file:
		for url in image_urls:
			if url == image_urls[-2]:
				out_file.write(url)
			elif url == image_urls[-1]:
				break
			else:
				out_file.write(url + ',')

	print "url: ", url


	img = urlopen(url).read()

	params = {
			'status': title, 
			'media[]': img, 
			'lat':str(location_coordinates()[0]), 
			'long':str(location_coordinates()[1])}

	t.statuses.update_with_media(**params)










