from mine_user_info import write_featureset
from os import listdir
from os.path import isfile, join
from time import sleep
import sys


already_mined = [ int(f) for f in listdir('features_assholes')[1:] ]

assholes = []
with open('assholes.csv', 'r') as infile:
    for line in infile:
        assholes.append(int(line))


assholes = list(set(assholes) - set(already_mined))


for wait, userid in enumerate(assholes):
	if wait == 3:
		sys.exit()

	featureset = write_featureset(userid)

	with open('features_assholes/%d' % userid, 'w') as outfile:
		outfile.write(str(featureset))

	print "\n--> Wrote:\t%s\n-->to\t\t%s" % (str(featureset), userid)