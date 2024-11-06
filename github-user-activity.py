import json
import urllib.error
import urllib.request


# Github API endpoint
APP_URL = "https://api.github.com/users/{}/events"


def fetch_github_activity(username):
    try:
        # Request data from Github API
        with urllib.request.urlopen(APP_URL.format(username.lower())) as response:
            if response.status == 200:
                data = json.loads(response.read())
                return data
            else:
                print(f"Error: Unable to fetch data (status code {response.status})")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def parse_activity(data):
    # Parsse and display each event in a readable format
    activities = []
    for event in data:
        event_type = event["type"]
        repo_name = event["repo"]["name"]

        # Create readable message base on event type
        if event_type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            activities.append(f"Pushed {commit_count} commit(s) to {repo_name}")
    return activities


def display_activity(activities):
    # Display parsed activities or handle no activities found
    if activities:
        for activity in activities:
            print(activity)
    else:
        print("No recent activity found.")


def main():
    # Prompt the user for the Github username
    username = input("Enter the GitHub username: ")

    data = fetch_github_activity(username)

    if data:
        activities = parse_activity(data)
        display_activity(activities)


if __name__ == "__main__":
    main()
