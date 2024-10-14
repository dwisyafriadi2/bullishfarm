import requests
import webbrowser
import time

# Define the common headers at the beginning
BASE_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",  # Ensure it's JSON
    "origin": "https://app.bullishfarm.app",
    "priority": "u=1, i",
    "referer": "https://app.bullishfarm.app/",
    "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}

def get_headers(token=None):
    """Returns the headers with an optional x-app-token."""
    headers = BASE_HEADERS.copy()  # Copy the base headers to avoid modification
    if token:
        headers["x-app-token"] = token  # Add the token if provided
    return headers

def read_init_data(file_path):
    """Reads the init-data from the specified file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

def authenticate(init_data):
    """Sends a POST request to authenticate using the given init-data."""
    url = "https://api.bullishfarm.app/auth/tg-mini-app"
    
    # Construct the payload
    payload = {
        "initData": init_data,  # initData contains the full URL-encoded string
        "tgPlatform": "tdesktop",
        "tgVersion": "7.10"
    }

    # Send the request
    response = requests.post(url, headers=get_headers(), json=payload)  # Use 'json' to send the payload as JSON
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error in request: {response.status_code} - {response.text}")
        return None

def fetch_task(token):
    """Fetches the task list using the provided token."""
    url = "https://api.bullishfarm.app/task/list"

    # Construct the payload for fetching tasks
    payload = {
        "lang": "id"
    }

    # Send the request with headers containing the token
    response = requests.post(url, headers=get_headers(token), json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching tasks: {response.status_code} - {response.text}")
        return None

def claim_task(token, task_id):
    """Claims the specified task using the provided task_id and token."""
    url = "https://api.bullishfarm.app/task/claim/ad"

    # Construct the payload for task claim
    payload = {
        "taskId": task_id
    }

    # Send the request with headers containing the token
    response = requests.post(url, headers=get_headers(token), json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error claiming task: {response.status_code} - {response.text}")
        return None

def claim_daily_reward(token):
    """Claims the daily reward using the provided token."""
    url = "https://api.bullishfarm.app/task/dailyrewards/claim"

    # No specific payload needed for daily reward claim
    payload = {}

    # Send the request with headers containing the token
    response = requests.post(url, headers=get_headers(token), json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error claiming daily reward: {response.status_code} - {response.text}")
        return None

def collect_box(token, energy, energy_left):
    """Automatically collects the box using the provided token and energy parameters."""
    url = "https://api.bullishfarm.app/zoo/box/collect"
    
    # Construct the payload for box collection
    payload = {
        "energy": energy,
        "energy_left": energy_left
    }

    # Send the request with headers containing the token
    response = requests.post(url, headers=get_headers(token), json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error collecting box: {response.status_code} - {response.text}")
        return None

def auto_tap_tap(token, energy, energy_left, animal_idx):
    """Performs the tap-tap action on an animal using the provided token."""
    url = "https://api.bullishfarm.app/zoo/animal/tap"

    # Construct the payload for the tap-tap action
    payload = {
        "energy": energy,
        "energy_left": energy_left,
        "animal_idx": animal_idx
    }

    # Send the request with headers containing the token
    response = requests.post(url, headers=get_headers(token), json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error performing tap-tap: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    # User options for enabling/disabling features
    enable_auto_claim_task = input("Enable Auto Claim Task (y/n): ").strip().lower() == 'y'
    enable_daily_checkin = input("Enable Daily Checkin (y/n): ").strip().lower() == 'y'
    enable_auto_collect_box = input("Enable Auto-Collect Box (y/n): ").strip().lower() == 'y'
    enable_auto_tap_tap = input("Enable Auto Tap-Tap (y/n): ").strip().lower() == 'y'

    # Read init_data from query.txt
    init_data = read_init_data("query.txt")
    
    # Authenticate with init_data
    auth_response = authenticate(init_data)
    if auth_response:
        print("Authentication successful:", auth_response)

        # Extract token from authentication response
        token = auth_response.get('token')

        # Fetch tasks using the token (if Auto Claim Task is enabled)
        if token and enable_auto_claim_task:
            task_response = fetch_task(token)
            if task_response:
                print("[Join Group](https://t.me/dasarpemulung)")
                print("Task list:", task_response)

                # Check if tasks exist in the 'items' list
                if "tasks" in task_response and "items" in task_response["tasks"] and len(task_response["tasks"]["items"]) > 0:
                    # Loop through all available tasks and claim them
                    for task in task_response["tasks"]["items"]:
                        task_id = task["id"]
                        task_title = task["title"]
                        task_url = task.get("url")
                        print("[Join Group](https://t.me/dasarpemulung)")
                        print(f"Attempting to claim task {task_id}: {task_title}")
                        
                        # Handle tasks with a URL (e.g., Twitter subscription)
                        if task_url:
                            print(f"Opening URL: {task_url}")
                            webbrowser.open(task_url)
                            print("Waiting for 15 seconds to simulate user interaction...")
                            time.sleep(15)  # Wait for 15 seconds

                        # Claim the task
                        claim_response = claim_task(token, task_id)
                        if claim_response:
                            print("[Join Group](https://t.me/dasarpemulung)")
                            print(f"Task {task_id} claimed successfully:", claim_response)
                        else:
                            print("[Join Group](https://t.me/dasarpemulung)")
                            print(f"Failed to claim task {task_id}.")
                else:
                    print("No tasks found.")
            else:
                print("Failed to fetch task list.")
        
        # Claim daily reward (if Daily Checkin is enabled)
        if enable_daily_checkin:
            print("Attempting to claim daily reward...")
            daily_reward_response = claim_daily_reward(token)
            if daily_reward_response:
                print("[Join Group](https://t.me/dasarpemulung)")
                print("Daily reward claimed successfully:", daily_reward_response)
            else:
                print("[Join Group](https://t.me/dasarpemulung)")
                print("Failed to claim daily reward.")

        # Auto-collect box (if Auto-Collect Box is enabled)
        if enable_auto_collect_box:
            print("Attempting to auto-collect the box...")
            energy = 100
            energy_left = 100  # Example values; adjust as needed
            box_response = collect_box(token, energy, energy_left)
            if box_response:
                print("[Join Group](https://t.me/dasarpemulung)")
                print("Box collected successfully:", box_response)
            else:
                print("[Join Group](https://t.me/dasarpemulung)")
                print("Failed to collect box.")

        # Auto Tap-Tap (if Auto Tap-Tap is enabled)
        if enable_auto_tap_tap:
            print("Attempting to perform Auto Tap-Tap...")
            energy = 100
            energy_left = 100
            animal_idx = 1  # Example animal index; adjust as needed
            tap_response = auto_tap_tap(token, energy, energy_left, animal_idx)
            if tap_response:
                print("[Join Group](https://t.me/dasarpemulung)")
                print("Tap-Tap performed successfully:", tap_response)
            else:
                print("[Join Group](https://t.me/dasarpemulung)")
                print("Failed to perform Tap-Tap.")
    else:
        print("Authentication failed.")
