from flask import Flask, render_template

app = Flask(__name__)

menu = ["1", "2", "3"]


@app.route("/")
def index():
    return render_template('index.html', menu=menu)


if __name__ == "__main__":
    app.run()
