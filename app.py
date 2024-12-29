from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# File to store daily water data and records
data_file = "daily_water_data.json"
records_file = "water_records.json"

# Load existing water data or initialize empty
if os.path.exists(data_file):
    with open(data_file, "r") as file:
        water_data = json.load(file)
else:
    water_data = {}

# Load records for weekly summary
if os.path.exists(records_file):
    with open(records_file, "r") as file:
        water_records = json.load(file)
else:
    water_records = {}

def save_data():
    """Save water data to the daily data file."""
    with open(data_file, "w") as file:
        json.dump(water_data, file, indent=4)

@app.route('/')
def index():
    """Welcome Page."""
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_water_intake():
    """Log water intake for the day."""
    date_today = str(datetime.today().date())
    intake = float(request.form['intake'])

    if intake < 1.5:
        return f"Oops! You need at least 1.5L of water daily. Please drink more."

    water_data[date_today] = intake
    save_data()
    return f"Great! You've hydrated yourself with {intake:.2f} liters today."

@app.route('/weekly_summary')
def weekly_summary():
    """Displays weekly summary."""
    total_intake = 0
    days_logged = 0

    for date, intake in water_data.items():
        total_intake += intake
        days_logged += 1

    weekly_average = total_intake / days_logged if days_logged > 0 else 0

    return render_template('summary.html', total_intake=total_intake, weekly_average=weekly_average)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

