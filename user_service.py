import zmq
import os
import json
import time  # Import time for delay

# Path to user database file
USER_DB_FILE = "user_profiles.json"

# Initialize ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")  # Port for the user microservice

# Load or create the user database
if not os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, 'w') as db:
        json.dump({"users": []}, db)  # Initialize with an empty user list

def load_users():
    """Load the user database from file."""
    with open(USER_DB_FILE, 'r') as db:
        return json.load(db)

def save_users(data):
    """Save the user database to file."""
    with open(USER_DB_FILE, 'w') as db:
        json.dump(data, db, indent=4)

def add_user(username):
    """Add a new user to the database."""
    data = load_users()
    if username in data["users"]:
        return f"User '{username}' already exists."
    data["users"].append(username)
    save_users(data)
    return f"User '{username}' created successfully."

def check_user(username):
    """Check if a user exists in the database."""
    data = load_users()
    if username in data["users"]:
        return f"User '{username}' exists."
    return f"User '{username}' not found."

def list_users():
    """Return a list of all users."""
    data = load_users()
    return f"Registered users: {', '.join(data['users']) if data['users'] else 'No users found.'}"

# Main service loop
print("User Microservice running on port 5556...")
while True:
    # Receive a JSON request from the client
    print("\nWaiting for a request...")
    request = socket.recv_json()
    command = request.get("command")
    username = request.get("username")

    # Simulate processing delay
    print("Processing request...")
    time.sleep(2)  # 2-second delay to simulate work being done

    if command == "add_user":
        response = add_user(username)

    elif command == "check_user":
        response = check_user(username)

    elif command == "list_users":
        response = list_users()

    else:
        response = "Invalid command."

    # Simulate response generation delay
    print("Generating response...")
    time.sleep(1)  # 1-second delay for response preparation

    # Send the response back to the client
    print("Sending response...")
    socket.send_string(response)
