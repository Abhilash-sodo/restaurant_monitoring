from flask import Flask, request, jsonify, send_file, render_template_string
import pandas as pd
import uuid
from database import engine
from sqlalchemy import text
import threading
import time

app = Flask(__name__)

# Store report status
reports = {}

def generate_report(report_id):
    # TODO: Implement report generation logic
    time.sleep(10)  # Simulate long-running task
    reports[report_id] = "Complete"

@app.route('/')
def home():
    html = '''
    <h1>Restaurant Monitoring System</h1>
    <h2>Available Endpoints:</h2>
    <ul>
        <li>POST /trigger_report - Triggers report generation</li>
        <li>GET /get_report?report_id=YOUR_REPORT_ID - Gets the status or result of a report</li>
    </ul>
    '''
    return render_template_string(html)

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    report_id = str(uuid.uuid4())
    reports[report_id] = "Running"
    
    # Start report generation in a separate thread
    threading.Thread(target=generate_report, args=(report_id,)).start()
    
    return jsonify({"report_id": report_id})

@app.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get('report_id')
    if report_id not in reports:
        return jsonify({"error": "Invalid report ID"}), 400
    
    status = reports[report_id]
    if status == "Running":
        return jsonify({"status": "Running"})
    elif status == "Complete":
        # TODO: Generate and return the CSV file
        return jsonify({"status": "Complete", "data": "CSV data here"})

if __name__ == '__main__':
    app.run(debug=True)