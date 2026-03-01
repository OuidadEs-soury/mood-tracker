from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from collections import Counter
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

FILE_NAME = "moods.txt"

MOODS = {
    "happy": "😊",
    "neutral": "😐",
    "sad": "😢",
    "angry": "😡"
}

def save_mood(mood):
    with open(FILE_NAME, "a") as f:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"{date}|{mood}\n")

def get_all_moods():
    if not os.path.exists(FILE_NAME):
        return []
    
    moods = []
    with open(FILE_NAME, "r") as f:
        for line in f.readlines():
            date, mood = line.strip().split("|")
            moods.append({"date": date, "mood": mood})
    return moods[::-1]  # newest first

def delete_mood(index):
    moods = get_all_moods()[::-1]  # original order
    if 0 <= index < len(moods):
        moods.pop(index)
        with open(FILE_NAME, "w") as f:
            for entry in moods:
                f.write(f"{entry['date']}|{entry['mood']}\n")

def get_stats():
    moods = get_all_moods()
    mood_names = [m["mood"] for m in moods]
    count = Counter(mood_names)
    total = len(moods)
    most_common = count.most_common(1)[0][0] if count else None
    return total, most_common

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "delete" in request.form:
            delete_index = int(request.form["delete"])
            delete_mood(delete_index)
            return redirect(url_for("home"))
        
        mood = request.form.get("mood")
        if mood:
            save_mood(mood)
            flash("Mood saved successfully!")
            return redirect(url_for("home"))

    moods = get_all_moods()
    total, most_common = get_stats()
    return render_template(
        "index.html",
        moods=moods,
        moods_dict=MOODS,
        total=total,
        most_common=most_common
    )

if __name__ == "__main__":
    app.run(debug=True)
    