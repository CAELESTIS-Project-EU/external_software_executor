from flask import Flask, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

#AVILABLE_SOFTWARE_JSON="config/available_software.json"

RHINO_LISTENER_URL = "http://localhost:4000"  # Replace PORT with the actual port number

# def load_software():
#     with open(AVILABLE_SOFTWARE_JSON, 'r') as file:
#         return json.load(file)

@app.route('/run', methods=['POST'])
def run_command():
    try:
        # Get the command from the request
        data = request.get_json()
        # Send a notification to the Rhino listener
        response = requests.post(RHINO_LISTENER_URL, json=data)
        
        # Check response from Rhino
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'Notification sent to Rhino'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to notify Rhino'}), 500

    except Exception as e:
        message = f"Error: {type(e).__name__} - {str(e)}"
        return jsonify({'status': 'error', 'message': message}), 500



if __name__ == '__main__':
    app.run(debug=True)

