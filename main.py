import modules.parser as p
import modules.models as m

PATHTOBLOCK = './sampleblock'

print("start")
a = p.Parser()
with open(PATHTOBLOCK, 'r') as content_file:
    CONTENT = content_file.read()
    a.parse(CONTENT)

print("done")
print("#######")
print("#######")

