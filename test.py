import requests
import json

# Define your GraphQL query
query = """
query MyQuery {
  getAllUsers {
    email
    fullName
    id
    username
  }
}
"""

# URL of your GraphQL server
url = "http://localhost:8888/graphql"

# Prepare the headers for the request
headers = {
    "Content-Type": "application/json"
}

# Prepare the payload for the POST request
json_data = {
    "query": query
}

# Send the request to the server
response = requests.post(url, json=json_data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    print(json.dumps(response.json(), indent=4))
else:
    print("Query failed to run by returning code of {}. {}".format(response.status_code, query))
