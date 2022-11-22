from os.path import sep as sep
with open("main.py", "r", encoding="utf-8") as f:
  code = f.read().split("\n")
for i in code:
    if i.split(" ")[0] == "import":
        with open("imports.txt", "a", encoding="utf-8") as file:
            file.write(i)
    life i.split(" ")[0] == "from":
        
    else:
        break