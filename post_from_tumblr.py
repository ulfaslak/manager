from twitter_manager import *
from tumblr_manager import *

update = post_from_tumblr('thefitnessquotes')

t.statuses.update(status=update)