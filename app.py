from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from collections import Counter
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

FILE_NAME = "moods.txt"

MOODS = {
    "happy": {"emoji": "😊", "score": 4},
    "neutral": {"emoji": "😐", "score": 3},
    "sad": {"emoji": "😢", "score": 2},
    "angry": {"emoji": "😡", "score": 1}
}


def save_mood(mood, note):
    with open(FILE_NAME, "a") as f:
        date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"{date}|{timestamp}|{mood}|{note}\n")


def get_all_moods():
    if not os.path.exists(FILE_NAME):
        return []

    moods = []
    with open(FILE_NAME, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if "|" in line:
                parts = line.split("|")
                if len(parts) == 4:
                    date, timestamp, mood, note = parts
                    moods.append({
                        "date": date,
                        "timestamp": timestamp,
                        "mood": mood,
                        "note": note
                    })
    return moods[::-1]


def get_stats(moods):
    mood_names = [m["mood"] for m in moods]
    count = Counter(mood_names)
    total = len(moods)
    most_common = count.most_common(1)[0][0] if count else None
    return total, most_common


def calculate_streak(moods):
    if not moods:
        return 0

    unique_days = sorted({m["date"] for m in moods}, reverse=True)
    streak = 0
    today = datetime.now().date()

    for i, day in enumerate(unique_days):
        expected_day = today - timedelta(days=i)
        if day == expected_day.strftime("%Y-%m-%d"):
            streak += 1
        else:
            break

    return streak


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        mood = request.form.get("mood")
        note = request.form.get("note")

        if mood:
            save_mood(mood, note)
            flash("Mood saved successfully!")
            return redirect(url_for("home"))

    moods = get_all_moods()
    total, most_common = get_stats(moods)
    streak = calculate_streak(moods)

    return render_template(
        "index.html",
        moods=moods,
        moods_dict=MOODS,
        total=total,
        most_common=most_common,
        streak=streak
    )


if __name__ == "__main__":
    app.run(debug=True)