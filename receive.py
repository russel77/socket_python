import json
import socket


def add_to_json_array(data, filename='output.json'):
    try:
        # Try to open the existing JSON file
        with open(filename, 'r') as file:
            # Load the existing JSON array
            json_array = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty JSON array
        json_array = []

    # Add the new data to the JSON array
    json_array.append(data)

    # Write the updated JSON array back to the file
    with open(filename, 'w') as file:
        json.dump(json_array, file, indent=2)


def main():
    host = socket.gethostbyname(socket.gethostname())  # Server IP
    port = 5000  # Port on the server

    s = socket.socket()  # Create a new socket

    try:
        s.connect((host, port))  # Connect to the server
        print("Connected to the server.")
        print("You are ready to receive data.")

        while True:
            data = s.recv(4096).decode('utf-8')

            # Check if data is not empty
            if not data:
                break  # Exit the loop when no data
                # Attempt to load JSON data
            try:
                player_data = json.loads(data)
                if player_data is not None:
                    # Check if the required keys are present in the received JSON
                    if all(key in player_data for key in ["First name", "Last name", "Age", "Scored Try"]):
                        add_to_json_array(data)
                    else:
                        print("Received data does not have all required keys:", player_data)

            except json.JSONDecodeError:
                print("Error decoding JSON data:", data)


    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        s.close()  # Close the socket connection when done
        # add_to_json_array(data)
        #
        #     player_data = json.loads(data)
        #     print("Received data:", player_data)
        #
        #     if not data:
        #         break  # Exit the loop when no more data is received

    # except Exception as e:
    #     print(f"Error: {e}")
    #
    # finally:
    #     s.close()  # Close the socket connection
    #     print("Connection closed. Thanks for your participation.")


if __name__ == "__main__":
    main()
