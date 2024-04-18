# Define the device data
from flask import *
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)
current_directory = os.getcwd()
os.chdir(current_directory)
with open(r'C:\Powerandcoolingcalc\devices.json', 'r') as file:
    devices = json.load(file)

def calculate_total_power_and_btu(selections):
    total_watts = 0
    total_btu = 0
    for device, quantity in selections.items():
        if device in devices:
            total_watts += devices[device]['power_watts'] * quantity
            total_btu += devices[device]['btu_per_hour'] * quantity
    return total_watts, total_btu

# Endpoint to process device selections
@app.route('/calculate', methods=['POST'])
def calculate_total_power_and_btu():
    data = request.get_json()
    selections = data['selections']
    total_watts = 0
    total_btu = 0
    for device, quantity in selections.items():
        if device in devices:
            total_watts += devices[device]['power_watts'] * quantity
            total_btu += devices[device]['btu_per_hour'] * quantity
    response = {
        "Total power consumption (Watts)": total_watts,
        "Total BTU per hour": total_btu
    }
    return jsonify(response), 200
@app.route('/devices', methods=['GET'])
def get_devices():
    try:
        with open(r'C:\Powerandcoolingcalc\devices.json', 'r') as file:
            devices = json.load(file)
        return jsonify(list(devices.keys())), 200
    except Exception as e:
        return jsonify({"error": "Unable to fetch devices", "details": str(e)}), 500


@app.route('/', methods=['GET'])
def DisplayWebpage():
    return render_template(r'Powerfrontend.html')
    




# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)