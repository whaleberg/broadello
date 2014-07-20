from jinja2 import Environment, FileSystemLoader
import os
import email
from bs4 import BeautifulSoup
from copy import deepcopy
import pytumblr
import yaml
import datetime

env = Environment(loader=FileSystemLoader('templates'))

import episodes

url="http://broadello.jellycast.com/pod/"
path="/home/unix/hussein/public_html/broadello/"

with open(path+"rss.xml", "w") as out:
	template = env.get_template("rss.template.html")
	eplist = deepcopy(episodes.episodes)
	for ep in eplist:
		ep["url"] = url + ep["path"]
		ep["size"] = os.path.getsize(path + ep["path"])
		ep["date"] = email.Utils.formatdate(os.path.getctime(path + ep["path"]))
		ep["description"] = BeautifulSoup(ep["description"]).get_text()

	out.writelines( template.render( episodes=episodes.episodes))

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

def tumbl_post(tumbl, ep):
	template = env.get_template("tumblr.template.html")
	t = os.path.getctime(path + ep["path"])
	ep["date"] = datetime.datetime.strftime(datetime.datetime.fromtimestamp(t), "%Y-%m-%d %H:%M:%S GMT")
	ep["url"] = url + ep["path"]
	tumbl.create_text(	"broadello",
				state = "published",
				date = ep["date"],
				title = ep['title'],
				format = "html",
				body = template.render( ep = ep ) )

tumbl = get_client()
titles = [x['title'] for x in tumbl.posts('broadello')['posts']]
eplist = reversed(deepcopy(episodes.episodes))
for ep in eplist:
	if ep["title"] not in titles:
		tumbl_post( tumbl, ep )
