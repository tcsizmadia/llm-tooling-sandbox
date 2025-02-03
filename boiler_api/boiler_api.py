from flask import Flask, request
import threading
import time

app = Flask(__name__)

# Constants
TEMPERATURE_UPDATE_INTERVAL = 5  # seconds

# Simulated state
actual_temperature = 21.5
desired_temperature = 22.0
is_heating = False
error_code = 0
error_messages = {
    0: "No error",
    1: "Low pressure",
    2: "Sensor fault",
    3: "Ignition failure",
}

# Temperature adjustment thread control
temperature_thread = None
should_run = False


def adjust_temperature():
    global actual_temperature, is_heating, should_run

    while should_run:
        if abs(desired_temperature - actual_temperature) < 0.1:
            is_heating = False
            actual_temperature = desired_temperature
        else:
            is_heating = True
            if actual_temperature < desired_temperature:
                actual_temperature = round(actual_temperature + 0.1, 1)
            else:
                actual_temperature = round(actual_temperature - 0.1, 1)
        time.sleep(TEMPERATURE_UPDATE_INTERVAL)


@app.route("/thermostat/actual")
def get_actual_temperature():
    return {"actual_temperature": actual_temperature}, 200


@app.route("/thermostat/desired", methods=["GET"])
def get_desired_temperature():
    return {"desired_temperature": desired_temperature}, 200


@app.route("/thermostat/desired", methods=["POST"])
def set_desired_temperature():
    global desired_temperature, temperature_thread, should_run
    data = request.get_json()

    if not data or "desired_temperature" not in data:
        return {"error": "Missing desired_temperature"}, 400

    try:
        desired_temperature = float(data["desired_temperature"])

        # Start temperature adjustment thread if not already running
        if temperature_thread is None or not temperature_thread.is_alive():
            should_run = True
            temperature_thread = threading.Thread(target=adjust_temperature)
            temperature_thread.start()

        return {"message": "Desired temperature set successfully"}, 200
    except ValueError:
        return {"error": "Invalid temperature value"}, 400


@app.route("/boiler/state")
def get_boiler_state():
    state = "heating" if is_heating else "not heating"
    return {"state": state}, 200


@app.route("/boiler/error")
def get_error_state():
    return {
        "error_code": error_code,
        "error_message": error_messages.get(error_code, "Unknown error"),
    }, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
