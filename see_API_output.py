import requests
import json

API_ENDPOINT = "https://math.he.net/mathbot"

data = { "q" : "$7x^{4} + 4x^{4} + 1x^{6} + 9x^{10} + 2x^{5}$" }

response = requests.post(url = API_ENDPOINT, data = data)

json_object = response.json()["data"]["solved"]

# check whether the question was parsed correctly,
# if the list is empty it fails
if not json_object:
    print("Mathbot is unable to parse the question asked.")

else:
    # extracts the solver name from the API_ENDPOINT
    print("\nSolver type: ", response.json()["data"]["parsed"]["tree"][0], "\n")
    print("HTML Solution: \n", response.json()["data"]["solved"]["answer"]["result"]["html_solution"])
    # now check for the special tag that marks the answers
    # figure out the syntax of the span tags, and figureout how to handle dom selection in python
    # make sure to cross check with robert's script

print(json.dumps(response.json(), indent=1))
