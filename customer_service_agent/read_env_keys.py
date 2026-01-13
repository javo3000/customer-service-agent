with open(".env", "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            if "=" in line:
                key = line.split("=")[0]
                print(f"Key found in .env: {key}")

