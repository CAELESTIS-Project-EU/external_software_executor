from flask import jsonify
import requests
import json

def run_addpath(dir):
    RHINO_LISTENER_URL = "http://localhost:4000"
    data_dict= {'software': 'addpath', 'parameters': {'dir': dir}}
    data = json.dumps(data_dict)
    # Send a notification to the Rhino listener
    response = requests.post(RHINO_LISTENER_URL, json=data)
        
    # Check response from Rhino
    if response.status_code == 200:
        return jsonify({'status': 'success', 'message': 'Notification sent to Rhino'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to notify Rhino'}), 500