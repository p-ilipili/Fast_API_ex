import requests
import subprocess
print("\n\n------------------------ NEW TEST ------------------------")
print("\n\nTest sans authentification:")
subprocess.run(['curl', 'http://127.0.0.1:8000/mcq?nb_qst=5&q_type=Test%20de%20positionnement&q_category=BDD'])

print("\n\nTest avec authentification erronee:")
subprocess.run(['curl', '-u', 'alice:lalaland', 'http://127.0.0.1:8000/mcq?nb_qst=5&q_type=Test%20de%20positionnement&q_category=BDD'])

print("\n\nTest avec authentification correcte, 1 categorie:")
res = subprocess.run(['curl', '-u', 'alice:wonderland', 'http://127.0.0.1:8000/mcq?nb_qst=5&q_type=Test%20de%20positionnement&q_category=BDD'])
print(res.stdout)

print("\n\nTest avec authentification correcte, type et categorie ne correspondent pas:")
subprocess.run(['curl', '-u', 'alice:wonderland', 'http://127.0.0.1:8000/mcq?nb_qst=5&q_type=Test%20de%20positionnement&q_category=Classification'])

print("\n\nTest avec authentification correcte, nb de questions incorrect:")
subprocess.run(['curl', '-u', 'alice:wonderland', 'http://127.0.0.1:8000/mcq?nb_qst=7&q_type=Test%20de%20positionnement&q_category=BDD'])

print("\n\nTest avec authentification correcte, 2 categories:")
res2 = subprocess.run(
    [
        'curl', '-X', 'GET', '-u', 'alice:wonderland',
        'http://127.0.0.1:8000/mcq?nb_qst=5&q_type=Test%20de%20positionnement&q_category=BDD,Docker'
    ]
)
print(res2.stdout)
#------------------------------------------ ADD QUESTION TEST 1 -----------------------------------------------#

print("\n\nTest of the add question function with incorrect authentication:")
# using the base64 encoded token instead of -u admin:4dm1N
url = 'http://localhost:8000/add-question'
payload = {
    "question": "What is the capital of France?",
    "subject": "Geography",
    "use": "General Knowledge",
    "correct": ["A", "B"],
    "responseA": "Paris",
    "responseB": "London",
    "responseC": "Berlin"
}

# Define the headers with the Authorization token
hders = {
    'Authorization': f'Basic {'YW1111111111tMU4='}',
    'Content-Type': 'application/json'
}

# Send the POST request with headers
response = requests.post(url, json=payload, headers=hders)

# Print the response
if response.ok:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)


#------------------------------------------ ADD QUESTION TEST 2 -----------------------------------------------#
print("\n\nTest of the add question function with a normal user : alice:wonderland:")
# Define the URL and the payload
url = 'http://localhost:8000/add-question'
payload = {
    "question": "What is the capital of France?",
    "subject": "Geography",
    "use": "General Knowledge",
    "correct": ["A", "B"],
    "responseA": "Paris",
    "responseB": "London",
    "responseC": "Berlin"
}

# Define the credentials for Basic Authentication
username = 'alice'
password = 'wonderland'

# Define the headers
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request with Basic Authentication
response = requests.post(url, json=payload, headers=headers, auth=(username, password))

# Print the response
if response.ok:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)


#------------------------------------------ ADD QUESTION TEST 3 -----------------------------------------------#

print("\n\nTest of the add question function with correct authentication:")
# using the base64 encoded token instead of -u admin:4dm1N
url = 'http://localhost:8000/add-question'
payload = {
    "question": "What is the capital of France?",
    "subject": "Geography",
    "use": "General Knowledge",
    "correct": ["A", "B"],
    "responseA": "Paris",
    "responseB": "London",
    "responseC": "Berlin"
}

# Define the headers with the Authorization token
hders = {
    'Authorization': f'Basic {'YWRtaW46NGRtMU4='}',
    'Content-Type': 'application/json'
}

# Send the POST request with headers
response = requests.post(url, json=payload, headers=hders)

# Print the response
if response.ok:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)

#----------------------------------------------------------------------------------------------------------------#

print("\n\n------------------------ END OF TEST ------------------------")