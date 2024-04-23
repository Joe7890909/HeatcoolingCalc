
from flask import *
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

# Use relative path for devices.json for better portability
devices_file_path = 'devices.json'

def read_devices():
    """Reads the devices from the JSON file."""
    with open(devices_file_path, 'r') as file:
        return json.load(file)

def write_devices(devices):
    """Writes the devices to the JSON file."""
    with open(devices_file_path, 'w') as file:
        json.dump(devices, file, indent=4)

@app.route('/devices', methods=['GET', 'PUT'])
def devices():
    if request.method == 'GET':
        # Return the list of devices
        return jsonify(list(read_devices().keys()))
    elif request.method == 'PUT':
        # Update the devices file
        new_device = request.json
        devices = read_devices()
        devices[new_device['name']] = {
            'power_watts': new_device['power_watts'],
            'btu_per_hour': new_device['btu_per_hour']
        }
        write_devices(devices)
        return jsonify({'message': 'Device added'}), 201

def calculate_total_power_and_btu(selections):
    total_watts = 0
    total_btu = 0
    devices = read_devices()
    for device, quantity in selections.items():
        if device in devices:
            x = int(devices[device]['power_watts'])
            y = int(devices[device]['btu_per_hour'])
            total_watts += x * quantity
            total_btu += y * quantity
    return total_watts, total_btu

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    selections = data['selections']
    total_watts, total_btu = calculate_total_power_and_btu(selections)
    return jsonify({'Total power consumption (Watts)': total_watts, 'Total BTU per hour': total_btu})

@app.route("/import",methods = ["GET"])
def index():
    return render_template("import.html",)
@app.route("/" ,methods = ["GET"])
def index1():
    return render_template("Powerfrontend.html",)


if __name__ == '__main__':
    app.run(debug=True)
