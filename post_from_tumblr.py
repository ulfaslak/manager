from twitter_manager import *
from tumblr_manager import *

print "Script: post_from_tumblr.py"

sleep(randrange(1500))

blog_bag = """thefitnessquotes healthy-life-style-forever visionsthroughmyeyes
beliveinyourselffrv tru1tru fitness-quotes"""

blog_list = blog_bag.split()
shuffle(blog_list)

det = randrange(2)

if det == 1:
    post_from_tumblr(blog_list[0])
