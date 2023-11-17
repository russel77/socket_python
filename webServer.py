import json
from flask import Flask, render_template, request

app = Flask(__name__)

person = {}


def load_data():
    global person
    try:
        with open('output.json', 'r') as file:
            data = json.load(file)
            # Assuming the data in the file is a list of JSON strings
            person = {player_data['First name']: player_data for player_data in map(json.loads, data)}
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist


# Save the person dictionary to the output.json file
def save_data():
    with open('output.json', 'w') as file:
        json.dump(list(person.values()), file, indent=2)


# Initialize the person dictionary by loading existing data
load_data()


@app.route('/', methods=['GET', 'POST'])
def index():
    search_result = None
    load_data()
    if request.method == 'POST':

        search_name = request.form.get('search', '').strip()
        if search_name:
            search_result = search_player(search_name)

    return render_template('index.html', person=person, search_result=search_result)


def search_player(name):
    if name in person:
        return person[name]  # Return the dictionary for the specified player
    else:
        return f"Player not found"


def run_server():
    host = '0.0.0.0'  # Allow connections from any IP
    port = 7000
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    run_server()
