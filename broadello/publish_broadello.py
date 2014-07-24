from jinja2 import Environment, FileSystemLoader
import os
import email
from bs4 import BeautifulSoup
from copy import deepcopy
import pytumblr
import yaml
import datetime
from ftplib import FTP

url="http://broadello.jellycast.com/pod/"
path="/home/unix/hussein/broadello/ftp/"
#url="http://broadinstitute.org/~hussein/broadello/"
#path="/home/unix/hussein/public_html/broadello/"

#transfer any episodes we're missing over to jellycast
import jellycreds
ftp = FTP("broadello.jellycast.com", jellycreds.user, jellycreds.password)
ftp.cwd("pod")
fnames = ftp.nlst()

dirpath, dirnames, filenames = os.walk(path).next()
for missing in [ f for f in filenames if f not in fnames ]:
	with open( os.path.join(dirpath, missing), 'r' ) as missingfile:
		ftp.storbinary(	"STOR " + missing, missingfile )

#render things! 
env = Environment(loader=FileSystemLoader('templates'))
import episodes

#rss
with open(path+"rss.xml", "w") as out:
	template = env.get_template("rss.template.html")
	eplist = deepcopy(episodes.episodes)
	for ep in eplist:
		ep["url"] = url + ep["path"]
		ep["size"] = os.path.getsize(path + ep["path"])
		ctime = ep["fake_ctime"] if "fake_ctime" in ep else os.path.getctime(path + ep["path"])
		ep["date"] = email.Utils.formatdate(ctime)
		ep["description"] = BeautifulSoup(ep["description"]).get_text()

	out.writelines( template.render( episodes=eplist))

#ftp the rss feed over too
with open(path+"rss.xml", 'r') as rss:
	ftp.storlines("STOR rss.xml", rss )
ftp.quit()

#construct a tumblr client	
def get_client():
		yaml_path = os.path.expanduser('~') + '/.tumblr'
		yaml_file = open(yaml_path, "r")
		tokens = yaml.safe_load(yaml_file)
		yaml_file.close()

		client = pytumblr.TumblrRestClient(tokens['consumer_key'],
										tokens['consumer_secret'],
										tokens['oauth_token'],
										tokens['oauth_token_secret'] )
		return client

#post a single episode to tumblr
def tumbl_post(tumbl, ep):
	template = env.get_template("tumblr.template.html")
	t = ep["fake_ctime"] if "fake_ctime" in ep else os.path.getctime(path + ep["path"])
	ep["date"] = datetime.datetime.strftime(datetime.datetime.fromtimestamp(t), "%Y-%m-%d %H:%M:%S GMT")
	ep["url"] = url + ep["path"]
	tumbl.create_text(	"broadello",
				state = "published",
				date = ep["date"],
				title = ep['title'],
				format = "html",
				body = template.render( ep = ep ) )

#delta between the titles we have in episodes.py and tumblr; upload any missing posts
tumbl = get_client()
titles = [x['title'] for x in tumbl.posts('broadello')['posts']]
eplist = reversed(deepcopy(episodes.episodes))
for ep in eplist:
	if ep["title"] not in titles:
		tumbl_post( tumbl, ep )
