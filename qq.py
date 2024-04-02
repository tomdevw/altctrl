def generate_names():
    base_name = "cxwalt"
    names = [f"{base_name}{i:02}" for i in range(41)]
    return names

# Test the function
names_list = generate_names()
for name in names_list:
    print(name)
