import requests


class BoilerClient:
    """Client for interacting with the Boiler API.

    Args:
        base_url (str): Base URL of the boiler API. Defaults to 'http://localhost:8000'.
    """
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url.rstrip('/')

    def get_actual_temperature(self):
        """Retrieve the current actual temperature from the boiler.

        Returns:
            float: The current temperature in Celsius.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        response = requests.get(f"{self.base_url}/thermostat/actual")
        response.raise_for_status()
        return response.json()["actual_temperature"]

    def get_desired_temperature(self):
        """Retrieve the desired temperature setting from the boiler.

        Returns:
            float: The desired temperature in Celsius.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        response = requests.get(f"{self.base_url}/thermostat/desired")
        response.raise_for_status()
        return response.json()["desired_temperature"]

    def set_desired_temperature(self, temperature):
        """Set a new desired temperature for the boiler.

        Args:
            temperature (float): The desired temperature in Celsius.

        Returns:
            str: Success message from the API.

        Raises:
            requests.exceptions.RequestException: If the API request fails or temperature value is invalid.
        """
        response = requests.post(
            f"{self.base_url}/thermostat/desired",
            json={"desired_temperature": temperature}
        )
        response.raise_for_status()
        return response.json()["message"]

    def get_boiler_state(self):
        """Get the current operational state of the boiler.

        Returns:
            str: The boiler state, either 'heating' or 'not heating'.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        response = requests.get(f"{self.base_url}/boiler/state")
        response.raise_for_status()
        return response.json()["state"]

    def get_error_state(self):
        """Get the current error state of the boiler.

        Returns:
            dict: A dictionary containing:
                - code (int): The error code (0 means no error)
                - message (str): Description of the error

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        response = requests.get(f"{self.base_url}/boiler/error")
        response.raise_for_status()
        return {
            "code": response.json()["error_code"],
            "message": response.json()["error_message"]
        }


# Example usage:
if __name__ == "__main__":
    client = BoilerClient()
    try:
        print(f"Current temperature: {client.get_actual_temperature()}°C")
        print(f"Desired temperature: {client.get_desired_temperature()}°C")
        print(f"Boiler state: {client.get_boiler_state()}")
        print(f"Error state: {client.get_error_state()}")

        # Set a new desired temperature
        client.set_desired_temperature(23.0)
        print("Set new desired temperature to 23.0°C")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the boiler API: {e}")
