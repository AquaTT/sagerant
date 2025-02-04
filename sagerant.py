import requests

channel_ids = ["1177750783178047530", "1001199696146071755", "1102503770115543060"]

email = ""
password = ""

def login(email, password):
    data = {
        "gift_code_sku_id": "0",
        "login": email,
        "login_source": "null",
        "password": password,
        "undelete": "false"
    }

    r = requests.post("https://discord.com/api/v9/auth/login", json=data).json()
    
    return r

client = login(email=email, password=password)
access_token = client["token"]

headers = {
    "Authorization": access_token,
    "Content-Type": "application/json",
}

message_ids = []

initial_text = input("Text: ")
payload = {"content": initial_text, "tts": "false"}

for id in channel_ids:
    res1 = requests.post(f"https://discord.com/api/v9/channels/{id}/messages", headers=headers, json=payload)
    message_id = res1.json().get("id")
    if message_id:
        message_ids.append((id, message_id))
    print(res1, res1.text)

while True:
    command = input("Enter command (send/delete/exit): ").lower()
    
    if command == "send":
        text = input("Text: ")
        payload = {"content": text, "tts": "false"}

        for id in channel_ids:
            res1 = requests.post(f"https://discord.com/api/v9/channels/{id}/messages", headers=headers, json=payload)
            message_id = res1.json().get("id")
            if message_id:
                message_ids.append((id, message_id))
            print(res1, res1.text)
    
    elif command == "delete":
        if not message_ids:
            print("No messages to delete.")
        else:
            for id, message_id in message_ids:
                res2 = requests.delete(f"https://discord.com/api/v9/channels/{id}/messages/{message_id}", headers=headers)
                print(res2, res2.text)
            message_ids.clear()
    
    elif command == "exit":
        print("Exiting the program.")
        break
    
    else:
        print("Invalid command. Please enter 'send', 'delete', or 'exit'.")
