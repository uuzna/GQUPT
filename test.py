with open("APIkeys.txt", "r") as file:
    api_key = file.readline().strip()
print(api_key)