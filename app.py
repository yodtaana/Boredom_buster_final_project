from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)


activities = [
    "Take a walk outside",
    "Read a book",
    "Listen to music",
    "Meditate",
    "Do some yoga",
    "Bake cookies",
    "Draw a picture",
    "Watch a movie",
    "Call a friend",
]

def bored(input_activity):
    matching_activities = [activity for activity in activities if input_activity.lower() in activity.lower()]
    if matching_activities:
        return random.choice(matching_activities)
    else:
        return random.choice(activities)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    participants = request.form['participants']
    price_range = tuple(float(x) for x in request.form['price'].split(','))

    response = requests.get("https://www.boredapi.com/api/activity",
                            params={"participants": participants, "price": price_range})
    data = response.json()

    if 'activity' in data:
        activity = data['activity']
        return render_template('results.html', activity=activity)
    else:
        suggestions = []
        for i in range(3):
            response = requests.get("https://www.boredapi.com/api/activity")
            data = response.json()
            suggestions.append(data['activity'])
        return render_template('results.html', suggestions=suggestions)

@app.route('/results')
def results():
    activity = request.args.get('activity')
    suggestion_count = int(request.args.get('suggestion_count'))


    activity = bored(activity)


    if not activity:
        suggestions = random.choices(activities, k=suggestion_count)
    else:
        suggestions = random.choices(activities, k=suggestion_count - 1)

    return render_template('results.html', activity=activity, suggestions=suggestions)


if __name__ == '__main__':
    app.run(debug=True)

