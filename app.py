from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "moods.txt"


def save_mood(mood):
    with open(FILE_NAME, "a") as f:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"{date} - {mood}\n")


def get_last_mood():
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
            if lines:
                return lines[-1]
    except FileNotFoundError:
        return None
    return None


def get_all_moods():
    try:
        with open(FILE_NAME, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        mood = request.form["mood"]
        save_mood(mood)

    last_mood = get_last_mood()
    return render_template("index.html", last_mood=last_mood)


@app.route("/history")
def history():
    moods = get_all_moods()
    moods.reverse()
    return render_template("history.html", moods=moods)


if __name__ == "__main__":
    app.run(debug=True)