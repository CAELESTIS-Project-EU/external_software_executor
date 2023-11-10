from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

AVILABLE_SOFTWARE_JSON="config/available_software.json"

def load_software():
    with open(AVILABLE_SOFTWARE_JSON, 'r') as file:
        return json.load(file)

@app.route('/run', methods=['POST'])
def run_command():
    try:
        # Get the command from the request
        data = request.get_json()
        available_software = load_software()
        software = data['software']
        params = data['parameters']
        command = available_software[software].format(**params)
        # Run the command using subprocess
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        # Check if the command executed successfully
        if process.returncode == 0:
            response = {'status': 'success', 'output': output.decode('utf-8')}
        else:
            response = {'status': 'failure', 'output': error.decode('utf-8')}
        return jsonify(response), 200
    except KeyError as e:
        message = f"'software' or 'parameters' not found: {str(e)}"
        return jsonify({'status': 'error', 'message': message}), 500
    
    except Exception as e:
        message = f"Error: {type(e).__name__} - {str(e)}"
        return jsonify({'status': 'error', 'message': message}), 500


if __name__ == '__main__':
    app.run(debug=True)

