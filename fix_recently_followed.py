from twitter_manager import *

friends_raw = t.friends.ids(user_id=2749655899)['ids']

targets = []
with open('../../sf_targets.csv','r') as in_file:
	for line in in_file:
		targets.append(int(line))

friends = friends_raw

print "Number of friends", len(friends)
print "Number of targets", len(targets)
print

for ta in targets:
	for i,f in enumerate(friends):
		if f == ta:
			del friends[i]

targets = list(set(targets) - set(friends_raw))

print "Number of friends not in targets", len(friends)
print "Number of targets not in friends", len(targets)
print "Total number of friends", len(friends) + len(targets)
print

frargets = friends + targets

with open('recently_followed.csv','w') as out_file:
	for i in frargets:
		print i,
		out_file.write(str(i) + '\n')
