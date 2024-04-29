from flask import Blueprint, request, jsonify
import subprocess
import json

import importlib

from app import AVILABLE_SOFTWARE_JSON, auth

api = Blueprint('api', __name__)

def load_software():
    with open(AVILABLE_SOFTWARE_JSON, 'r') as file:
        return json.load(file)

def run_command(command):
    # Run the command using subprocess
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Check if the command executed successfully
    if process.returncode == 0:
        response = {'status': 'success', 'output': output.decode('utf-8')}
    else:
        response = {'status': 'failure', 'output': error.decode('utf-8')}
    return response

def resolve_params(args, params):
    for i in range(len(args)):
        value = args[i]
        if isinstance(value, str) and value[0] == '{' and value[-1] == '}':
                variable_name = value[1:-1]
                args[i] = params[variable_name]



def run_function(full_func_name, args, params):
        mod_name, func_name = full_func_name.rsplit('.',1)
        module = importlib.import_module(mod_name)
        resolve_params(args, params)
        func = getattr(module, func_name)
        return func(*args)


@api.route('/run', methods=['POST'])
@auth.login_required
def run():
    try:
        # Get the command from the request
        data = request.get_json()
        print(str(data))
        available_software = load_software()
        software = data['software']
        params = data['parameters']
        s_type = available_software[software]['type']
        if s_type == "command":
            response = run_command(available_software[software]['command'].format(**params))
        elif s_type == "function":
            response = run_function(available_software[software]['function'], 
                         available_software[software]['args'], params)
        else :
            raise Exception("Type of software " + software + "not supported (" + type + ")" )
        return jsonify(response), 200
    except KeyError as e:
        message = f"'software' or 'parameters' not found: {str(e)}"
        return jsonify({'status': 'error', 'message': message}), 500
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        message = f"Error: {type(e).__name__} - {str(e)}"
        return jsonify({'status': 'error', 'message': message}), 500
