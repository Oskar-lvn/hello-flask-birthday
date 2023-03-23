from flask import Flask, request, jsonify
from datetime import datetime

"""
The in-memory dictionary is sufficient for the purpose of this POC, however, for production, 
depending on the requirements, it is recommended to use a persistent DB/storage for the data.
For example, Cloud SQL (see suggested architecture).
"""

app = Flask(__name__)
users = {}

@app.route('/')
def hello_world():
    return "Hello World!"

# API endpoint for adding/updating user's name and date of birth
@app.route('/hello/<username>', methods=['PUT'])
def add_user(username):
    # Verify that the username contains only letters
    if not username.isalpha():
        return 'Username must contain only letters', 400
    
    # Parse the date of birth from request JSON
    dob_str = request.json.get('dateOfBirth')
    # Verify that the request containes a dateOfBirth 
    if not dob_str:
        return 'Missing date of birth', 400
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    except ValueError:
        return 'Invalid date format. Please use YYYY-MM-DD.', 400
    
    # Check if the date of birth is in the past
    if dob >= datetime.now().date():
        return 'Invalid date of birth', 400
    
    # Add/update the user in the dictionary with its dateofbirth value
    users[username] = dob
    
    # Return success status
    return '', 204

# API endpoint for retrieving user's birthday message
@app.route('/hello/<username>', methods=['GET'])
def hello_user(username):
    # Verify that the username contains only letters
    if not username.isalpha():
        return 'Username must contain only letters', 400
    
    # Check if user exists in the dictionary
    if username not in users:
        return 'User not found', 404
    
    # Calculate days to user's next birthday
    dob = users[username]
    today = datetime.now().date()
    days_to_birthday = (datetime(today.year, dob.month, dob.day).date() - today).days % 365
    
    # Return birthday message in JSON format
    if days_to_birthday == 0:
        message = f'Hello, {username}! Happy birthday!'
    else:
        message = f'Hello, {username}! Your birthday is in {days_to_birthday} day(s)'
    return jsonify(message=message)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)