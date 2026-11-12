import os

print(os.path.realpath("/notizen"))
print(os.path.join("notizen","C:\\User"))
print(os.path.commonpath(["C:\\a\\notizen","C:\\a\\notizen\\unterodner"]))