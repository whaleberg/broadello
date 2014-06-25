from jinja2 import Environment, PackageLoader
import os

env = Environment(loader=PackageLoader('broadello', 'templates'))


import episodes


#app = Flask(__name__)


#if __name__ == '__main__':
#    app.run()

with open("test.html","w") as out:
    template = env.get_template("index.template.html")
    out.writelines( template.render( episodes=episodes.episodes))

url="http://www.broadinstitute.org/~hussein/broadello/"
path="/home/unix/hussein/public_html/broadello/"

with open("rss.html", "w") as out:
    template = env.get_template("rss.template.html")
    for ep in episodes.episodes:
        ep["url"] = url + ep["path"]
        ep["size"] = os.path.getsize(path + ep["path"])

    print episodes.episodes

    out.writelines( template.render( episodes=episodes.episodes))