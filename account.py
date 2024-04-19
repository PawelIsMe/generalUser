import json
import re

# Creates an account
def createAccount(fname, lname, user, password, ipaddr):
    f = "accounts.json"

    new_data = {
        "first_name": fname, # First name
        "last_name": lname,  # Last name
        "username": user,    # Username
        "password": password,# Password
        "ipaddr": ipaddr,    # IP address
        "islogged": 1,       # Tells if the user is logged in
        "id": 0              # ID - doesn't work :c
    }

    # Read json file
    with open(f, "r") as file:
        data = json.load(file)

        # Update json object
        data.append(new_data)

    # Write json file
    with open(f, "w") as file:
        json.dump(data, file, indent=5)


# Checks if the account is created under the user's ip address
def haveAnAccount(ipaddr):
    with open('accounts.json') as json_file:
        json_data = json.load(json_file)

    # ipaddr searching
    for item in json_data:
        if item.get("ipaddr") == ipaddr:
            return True
    return False

# Checks if the account exists
def doesExist(user):
    with open('accounts.json') as json_file:
        json_data = json.load(json_file)

    # username searching
    for item in json_data:
        if item.get("username") == user:
            return True
    return False


# Simple check password and login in accounts.json
def checkLogin(username, password):
    f = open("accounts.json", "r")
    data = json.loads(f.read())

    for cos in data:
        if cos.get('username') == username and cos.get('password') == password:
            return True
    return False

# Activates login in accounts.json (changes islogged: 0 -> islogged: 1)
def activateLogin(user):
    changeData(user, "islogged", 1)

# Logs out the user in accounts.json (changes islogged: 1 -> islogged: 0)
def logout(user):
    changeData(user, "islogged", 0)

# Checks if the user is logged in
def isLogged(user):
    if readData(user, "islogged") == 1:
        return True
    return False

# Changes data in accounts.json
def changeData(user, it, new):
    with open('accounts.json') as json_file:
        json_data = json.load(json_file)

    for item in json_data:
        if item.get("username") == user:
            item[it] = new
        newData = json.dumps(json_data, indent=5)


    with open('accounts.json', 'w') as f:
        f.write(newData)
    f.close()

# Returns data in accounts.json
def readData(user, it):
    with open('accounts.json') as json_file:
        json_data = json.load(json_file)

    for item in json_data:
        if item.get("username") == user:
            return item[it]

# Returns username and password for a given IP address
def checkIpAddr(ipaddr):
    with open('accounts.json') as json_file:
        json_data = json.load(json_file)

    for item in json_data:
        if item.get("ipaddr") == ipaddr and item['islogged'] == 1:
            return item['username'], item['password']

# =============== CHAT HISTORY ===============
# Save message in chat history (conversation.txt)
def saveMessage(user, msg):
    with open('conversation.txt', 'r') as f:
        last_line = f.readlines()[-1]
        f.close()

    x = re.search(r"value=\"(.*?)\"", last_line)
    last_user = x.group(1)
    if last_user == user:
      div_msg = f"<div class=\"message\" value=\"{user}\">{msg}</div>\n"
    else:
      div_msg = f"<p class=\"nick\">{user}</p><div class=\"message\" value=\"{user}\">{msg}</div>\n"

    with open("conversation.txt", "a") as myfile:
        myfile.write(div_msg)
        myfile.close()

# Returns chat history (conversation.txt) to function chat() in main.py
def readChatHistory():
    with open('conversation.txt', 'r') as f:
        chat_history = f.read()
    return chat_history