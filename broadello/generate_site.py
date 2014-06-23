from episodes import episodes
HEADER = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Live from the Broadello</title>
<link rel="stylesheet" href="../css/pure-min.css">
<link rel="stylesheet" href="../css/pure2.css">
</head>
<body>

<div class="content">

<h1>Live from the Broadello</h1>

<h3>What the hell is this?</h3>

We'll let the reviews do the talking:
<blockquote><em>"Like shamelessly listening to someone else's conversation in a cafe"</em></blockquote>
<blockquote><em>"Usually when I listen to podcasts, I get distracted and don't do my work. Your podcast is great - it's boring enough that I can keep working while listening to it!"</em></blockquote>
<strong>Follow us on Twitter</strong>: <a href="https://twitter.com/broadello">@broadello</a> for updates (usually Monday, Wednesday and Friday).<br/>
<strong>Grab the RSS feed</strong>: <a href="http://twitrss.me/twitter_user_to_rss/?user=broadello">here</a>.<br/>
<strong>Email us</strong> with Strong Opinions, a joke to share, or just something you want to get off your chest:  broadello at gmail dot com.<br/><br/>

<h3>Episode List</h3>\n"""

FOOTER = """</div>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-50792912-1', 'broadinstitute.org');
  ga('send', 'pageview');

var sc_project=9790764;
var sc_invisible=1;
var sc_security="63371cd3";
var scJsHost = (("https:" == document.location.protocol) ?
"https://secure." : "http://www.");
document.write("<sc"+"ript type='text/javascript' src='" +
scJsHost+
"statcounter.com/counter/counter.js'></"+"script>");
</script>
</body>
</html>"""


def render_episode_to_html(episode):
    episode_line = """<a href="{file_path}">{title}</a> {time}<br/>
{description}
<br/><br/>\n"""
    return episode_line.format(file_path=episode["path"], title=episode["title"],
                               time=episode["time"], description=episode["description"])


def render_html(output_file, episodes):
    with open(output_file, "w") as writer:
        writer.write(HEADER)
        for ep in episodes:
            writer.write(render_episode_to_html(ep))
        writer.write(FOOTER)


RSS_HEADER = """<?xml version="1.0" encoding="UTF-8"?>

<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">

<channel>

<itunes:explicit>

<title>Live from the Broadello</title>

<link>http://tinyurl.com/broadello</link>

<language>en-us</language>

<copyright>2014 Hussein and Louis</copyright>

<itunes:author>Hussein and Louis</itunes:author>

<itunes:summary>Two guys talking over lunch and each other.  Warning: Boats may be mentioned, but fear not listeners will be warned before boats are mentioned.  This is the home of guest Wednesdays.</itunes:summary>

<description>Two guys talking over lunch and each other.  Warning: Boats may be mentioned, but fear not listeners will be warned before boats are mentioned.  This is the home of guest Wednesdays.</description>

<itunes:owner>

<itunes:name>Broadello</itunes:name>

<itunes:email>broadello@gmail.com</itunes:email>

</itunes:owner>

<itunes:image href="http://example.com/podcasts/everything/AllAbout Everything.jpg" />"""



rss_footer="""</channel>

</rss>"""





render_html("test.html", episodes)