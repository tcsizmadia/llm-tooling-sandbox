import ollama
from boiler_api.boiler_client import BoilerClient


SYSTEM_PROMPT = """
You are an AI assistant for a smart boiler system. 
Your task is to interact with the boiler using the Boiler API. 
Do your best to help the user with their boiler-related queries. 
If the user feels cold, they might want to increase the desired temperature. If you don't know the temperature, you can ask the boiler for it.
If the user feels hot, they might want to decrease the desired temperature.
Do not make up information. If you don't know something, ask the boiler for the information. If there is no function for that, tell the user you can't help with that.
Restrict your responses to the boiler system only, deny any general information requests. 
Proceed with the command:
"""


def get_available_functions(client: BoilerClient) -> dict:
    available_functions = {
        "get_actual_temperature": client.get_actual_temperature,
        "get_desired_temperature": client.get_desired_temperature,
        "set_desired_temperature": client.set_desired_temperature,
        "get_boiler_state": client.get_boiler_state,
        "get_error_state": client.get_error_state,
    }

    return available_functions


def get_model_response(prompt, client: BoilerClient, model="mistral-nemo") -> str:
    """Get response from Ollama API.

    Args:
        prompt (str): User input prompt
        model (str): Name of the model to use

    Returns:
        str: Model's response text
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    first_response = ollama.chat(
        model=model,
        messages=messages,
        tools=[
            client.get_actual_temperature,
            client.get_boiler_state,
            client.get_desired_temperature,
            client.set_desired_temperature,
            client.get_error_state,
        ],
    )

    if first_response.message.tool_calls:
        output = ""
        for tool in first_response.message.tool_calls or []:
            function_to_call = get_available_functions(client).get(tool.function.name)
            if function_to_call == client.get_actual_temperature:
                output += f"\nActual temperature: {function_to_call()}°C"
            elif function_to_call == client.get_desired_temperature:
                output += f"\nDesired temperature: {function_to_call()}°C"
            elif function_to_call == client.get_boiler_state:
                output += f"\nBoiler state: {function_to_call()}"
            elif function_to_call == client.get_error_state:
                error_state = function_to_call()
                output += f"\nError code: {error_state['code']}\nError message: {error_state['message']}"
            elif function_to_call == client.set_desired_temperature:
                output += f"\n{function_to_call(**tool.function.arguments)}"

        messages.append(first_response.message)
        messages.append({"role": "tool", "content": output, "tool": tool.function.name})
        final_response = ollama.chat(model=model, messages=messages)
        response_content = final_response.message.content
    else:
        response_content = first_response.message.content

    return response_content


def main():
    print("Boiler Chat Agent (using mistral-nemo)\n")
    print("Type 'bye' to exit\n")

    client = BoilerClient()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "bye":
            print("\nGoodbye!")
            break

        if user_input:
            print("\nAgent: ", end="")
            response = get_model_response(user_input, client)
            print(response)
            print()  # Empty line for better readability


if __name__ == "__main__":
    main()
