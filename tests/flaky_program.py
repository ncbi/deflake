f = open("counter", "w+")
contents =  f.read()
print contents
if contents == "":
    f.write("1")
else:
    f.write(str(int(contents) + 1))
f.close()
