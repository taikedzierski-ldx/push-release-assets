all_users = {
    # Using a Personal API Token (preferred method)
    "user1" : ["adg789786adfg7896adfg7896adfg"],

    # Using credentials (deprecated, also non-secure)
    "user2" : ["user-two", "th3Passw0rd"]
}

def getUser(username):
    return all_users[username]
