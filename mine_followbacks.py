from mine_user_info import write_featureset
from os import listdir
from os.path import isfile, join
from time import sleep
import sys


already_mined = [ int(f) for f in listdir('features_followbacks') ]

followbacks = []
with open('followbacks.csv', 'r') as infile:
    for line in infile:
        followbacks.append(int(line))


followbacks = list(set(followbacks) - set(already_mined))


for wait, userid in enumerate(followbacks):
	if wait == 3:
		sys.exit()

	featureset = write_featureset(userid)

	with open('features_followbacks/%d' % userid, 'w') as outfile:
		outfile.write(str(featureset))

	print "\n--> Wrote:\t%s\n-->to\t\t%s" % (str(featureset), userid)
