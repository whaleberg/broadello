from jinja2 import Environment, FileSystemLoader
import os
import email
from bs4 import BeautifulSoup

env = Environment(loader=FileSystemLoader('templates'))

import episodes

url="http://www.broadinstitute.org/~hussein/broadello/"
path="/home/unix/hussein/public_html/broadello/"

with open(path+"index.html","w") as out:
    template = env.get_template("index.template.html")
    out.writelines( template.render(episodes=episodes.episodes) )

with open(path+"rss.xml", "w") as out:
    template = env.get_template("rss.template.html")
    for ep in episodes.episodes:
        ep["url"] = url + ep["path"]
        ep["size"] = os.path.getsize(path + ep["path"])
        ep["date"] = email.Utils.formatdate(os.path.getctime(path + ep["path"]))[:-3] + "500"
        ep["description"] = BeautifulSoup(ep["description"]).get_text()

    print episodes.episodes

    out.writelines( template.render( episodes=episodes.episodes))
