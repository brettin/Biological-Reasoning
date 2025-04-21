import requests
import urllib.parse
import json

# Define your search and filter parameters
start_date = '2023-01-01'     # Start of date range (YYYY-MM-DD)
end_date = '2023-12-31'       # End of date range (YYYY-MM-DD)
cursor = 0                  # Starting index for records
limit = 10                  # Maximum number of records to return
search_query = "genomic surveillance"  # Your search string

# URL encode the search term
encoded_query = urllib.parse.quote(search_query)

# Construct the URL.
# Note: This example assumes the API supports a "query" parameter.
# Some endpoints might use "q", "search", etc.
url = (
    f"https://api.biorxiv.org/details/biorxiv/"
    f"{start_date}/{end_date}/{cursor}/{limit}"
    f"?query={encoded_query}"
)

# Print the URL for debugging purposes
print("Requesting URL:", url)

# Make the HTTP GET request to the API
response = requests.get(url)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()  # Parse JSON response
    # Display the output in a nicely formatted JSON string
    print("Response JSON:")
    print(json.dumps(data, indent=2))
else:
    print(f"Error: Received response code {response.status_code}")
