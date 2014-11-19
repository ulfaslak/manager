# -*- coding: UTF-8 -*-


#---Imports---#

from twitter_manager import *

import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from re import split

#---Script---#

def get_ALICE_response(message):
	"""
		Pipes a message to ALICE and gets a response.
	"""
	d = webdriver.PhantomJS()
	d.get('http://sheepridge.pandorabots.com/pandora/talk?botid=b69b8d517e345aba&skin=custom_input')

	# Pipe to ALICE
	while True:
		try:
			text_field = d.find_element_by_xpath("/html/body/form/p/input[1]")
			break
		except:
			sleep(1)

	while True:
		try:
			text_field.send_keys(message)
			break
		except:
			sleep(1)

	while True:
		try:
			text_field.send_keys(Keys.ENTER)
			break
		except:
			sleep(1)

	# Retrieve response from ALICE
	while True:
		try:
			ALICE_response = d.find_element_by_xpath("/html/body").text
			break
		except:
			sleep(1)

	ALICE_response_list = ALICE_response.split('\n')

	for line in ALICE_response_list:
		if 'A.L.I.C.E.:' in line:
			ALICE_response = line[12:]
			break

	return ALICE_response


def get_CHOMSKY_response(message):
	"""
		Pipes a message to CHOMSKY and gets a response.
	"""

	d = webdriver.PhantomJS()
	d.get('http://demo.vhost.pandorabots.com/pandora/talk?botid=b0dafd24ee35a477')

	# Pipe to ALICE
	while True:
		try:
			text_field = d.find_element_by_xpath('/html/body/center/table/tbody/tr/td[4]/form/input')
			break
		except:
			sleep(1)
                        print "Sleep get text_field"

	while True:
		try:
			text_field.send_keys(message)
			break
		except:
			sleep(1)
                        print "Sleep send message to text_field"

	while True:
		try:
			d.find_element_by_xpath('/html/body/center/table/tbody/tr/td[4]/form/font/input').click()
                        #text_field.send_keys(Keys.ENTER)
			break
		except:
			sleep(1)
                        print "Sleep click submit"

	# Retrieve response from ALICE
	while True:
		try:
			CHOMSKY_response = d.find_element_by_xpath("/html/body/center/table/tbody/tr/td[4]/form/font/font/font").text
			break
		except:
			sleep(1)
                        print "Sleep get response"

	CHOMSKY_response = CHOMSKY_response.split('\n')[2]
	CHOMSKY_response_list = CHOMSKY_response.split()
	
	if 'Chomsky' in CHOMSKY_response:
		for index, word in enumerate(CHOMSKY_response_list):
			if 'Chomsky' in word:
				 CHOMSKY_response_list[index] = 'Emilia'
        
        censure = ['robot', 'chatbot', 'computer', 'com']
        for element in censure:
                if element in CHOMSKY_response:
                        print "Bad answer caught: ", CHOMSKY_response
                        sys.exit()


        CHOMSKY_shortened_response = []
        for word in CHOMSKY_response_list:
                CHOMSKY_shortened_response.append(word)
                if '.' in word or '!' in word or '?' in word:
                        break       

	CHOMSKY_shortened_response = ' '.join(CHOMSKY_shortened_response)

	return CHOMSKY_shortened_response


def is_valid(text):
	"""
		Asserts that the message isn't spam.
	"""

	bag_of_spam_words = """http unfollow validate click facebook google pintrest
	blog FB @ .com .ly website dotcom outu .me email address send #
        RT""".split()

	for word in bag_of_spam_words:
		if word in text:
			spam = word
			return {'true': False, 'spam': spam}

	return {'true': True, 'spam': ""}


def get_latest_unread():
	"""
		Returns the text of the latest message from a stored since_id and 
		stores that ones since_id in a file.
	"""

	with open('message_since_id.csv','r') as in_file:
		since_id = int(in_file.read())

	# JSON hvor 0 er nyest.
	latest_message = t.direct_messages(since_id=since_id, count=1)

	if len(latest_message) == 0:
		print "No new messages."
		sys.exit()

	with open('message_since_id.csv','w') as out_file:
		since_id_new = int(latest_message[0]['id'])
		out_file.write(str(since_id_new))

	return {
	'message': latest_message[0]['text'], 
	'user_id': latest_message[0]['sender']['id'], 
	'screen_name': latest_message[0]['sender']['screen_name'],
	'message_id': since_id_new,
	}


def respond_user():
	"""
		Uses get_latest_unread and get_ALICE_response to post a reply to the
		user.
	"""

	latest_unread 	= get_latest_unread()
	message  		= latest_unread['message']
	user_id  		= latest_unread['user_id']
	screen_name		= latest_unread['screen_name']
	message_id 		= latest_unread['message_id']
	
	if is_valid(message)['true']:
		response = get_CHOMSKY_response(message)
		try:
			t.direct_messages.new(text=response, user_id=user_id)
			try:
                                print "Responded '%s' to message '%s'." % (response,message)
                        except:
                                print "Unicode Error in message but responding '%s' anyway" % response
		except:
			t.friendships.destroy(user_id=user_id)
			remove_user_from_current_friends(user_id)
			t.direct_messages.destroy(id=message_id)

			try:
                                print "Exception found, unfollowing user '%s' and deleting message '%s'." % (screen_name, message)
                        except:
                                print "Unicode Error in message but deleting and unfollowing anyway."
	else:
		t.friendships.destroy(user_id=user_id)
		remove_user_from_current_friends(user_id)
		t.direct_messages.destroy(id=message_id)
                try:
		        print """Tweet filter caught spam '%s' in message '%s'. Unfollowing user '%s and deleting message.""" % (is_valid(message)['spam'], message, screen_name)
                except:
                        print "Unicode messed up, but I'm still deleting the message and unfollowing the user."



# Run script
sleep(randrange(599))
respond_user()
