from flask import Flask
from threading import Thread

app = Flask('Budi Bot')#apparently you could name it with anything

@app.route('/')
def home():
  #  Moderately distracting stuff ~anno2003
    return "<marquee>\
		<h1 style=\"background:linear-gradient(to left, violet, indigo, blue, green, yellow, orange, red);\">\
			<i>I'm still standing ...</i> <p><a href=\"https://Budi-Bot-3.priacantiq.repl.co/about\">klik</a></p>\
		</h1></marquee>\
		<iframe src=\"https://giphy.com/embed/Bap9PFewF20es\" width=\"480\" height=\"480\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/lizard-Bap9PFewF20es\">via GIPHY</a></p>"

@app.route('/about')
def about():
	return """
	<h1>Budi Bot 3</h1>
	<h2>Brought to you by <i>PriaCantiq</i> and frens</h2>
	<hr>
	"""
@app.route('/do/not/try/to/find/the/easter/Egg')
def egg():
	return """
	<h1>Conrats </h1>
	<p> you habe vound ze semi seckrit pej</p>
	<p> i'll think of a reward later</p>
	<hr>
	<marquee direction=\"down\" behaviour=\"alternate\"><IMG SRC=\"https://cdn.discordapp.com/attachments/708711084349063251/915110901852565535/fuck_pepe.gif\" ></marquee>
	<br>
	<marquee direction=\"up\" behaviour=\"alternate\"><IMG SRC=\"https://cdn.discordapp.com/attachments/708711084349063251/915112017004728360/OIP.lVMXeRolgmZhtfjGYYxVPAHaGU.jpg\"></marquee>
	<br>
	<marquee direction=\"left\" behaviour=\"alternate\"><img src=\"https://cdn.discordapp.com/attachments/708711084349063251/915111770228662302/ryuko_pepe.jpg\"></marquee>
	<br>
	<marquee direction=\"right\" behaviour=\"alternate\" scrollamount=\"75\"><img src=\"https://cdn.discordapp.com/attachments/708711084349063251/915110377975582750/sonic_pepe.gif\"></marquee>
	"""
def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()