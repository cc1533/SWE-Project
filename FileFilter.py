# the purpose of this is to extract the words that were extracted as keywords using mallet
# from a file that is is the same format as the lined columns. this makes it easier to see
# which keywords from the output_state file belong to which line and subsequently which date
# and enhancement or bug type

stopf = open("en.txt", "r")
opfile = open("TOPICINPUT.lined", "r")

new = opfile.read().lower()

stops = stopf.readlines()
for line in range(len(stops)):
    stops[line] = stops[line].split()[0]

for word in stops:
    while (" "+word+" " in new):
        new = new.replace(" "+word+" ", " ")
    while ("\n"+word+" " in new):
        new = new.replace("\n"+word+" ", "\n")
    while (" "+word+"\n" in new):
        new = new.replace(" "+word+"\n", "\n")
    while ("\n"+word+"\n" in new):
        new = new.replace("\n"+word+"\n", "\n\n")

while (". " in new):
    new = new.replace(". ", " ")
while ("'" in new):
    new = new.replace("'", "")
while ("," in new):
    new = new.replace(",", "")
while (": " in new):
    new = new.replace(": ", " ")
for x in ['1','2','3','4','5','6','7','8','9','0', '(', ')']:
    while (x in new):
        new = new.replace(x, "")

newfile = open("FILTERED.txt", "w")
newfile.write(new)
newfile.close()

opfile.close()
stopf.close()
