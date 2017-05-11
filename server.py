from flask import Flask

#instance of app
app = Flask(__name__)

@app.route('/')
def render_index():
	return render_template('index.html')




if __name__ == "__main__":
	app.run(host = "0.0.0.0", debug = True)