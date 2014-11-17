from twitter_manager import *
import requests as rq

targets = rq.get(
	'http://ec2-54-77-226-94.eu-west-1.compute.amazonaws.com/static/targets').text

targets = targets.split('\n')[:-1]
targets = [ int(n) for n in targets ]
targets.append(1853338002)

try:
	with open('sf_targets.csv', 'r') as in_file:
		used_targets = in_file.read().split('\n')[:-1]
		used_targets = [ int(n) for n in used_targets ]
except IOError:
	with open('sf_targets.csv', 'w') as dummy:
		used_targets = []

new_targets = list(set(targets) - set(used_targets))

for i in new_targets:
	try:
		t.friendships.create(user_id=i, follow=True)
	except TwitterHTTPError:
		print "User %d accept pending" % i
	print "Followed", i

with open('sf_targets.csv', 'w') as out_file:
	for i in targets:
		out_file.write(str(i) + '\n')
