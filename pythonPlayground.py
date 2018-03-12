list = ('1:Hard drive recovery', '2:Hard drive copying', '3:RAID', '4:Hard Drive Formatting/Wiping', '5:ISO Creation', '6:Encryption', '7:Word processing', '8:Programming', '9:Resource monitor', '10:Browsers', '11:Torrenting', '12:Photo Editing', '13:Compression', '14:Remote Desktop', '15:Virtual Machines')

print('Here is the list of available options:')
for x in range(len(list)):
    print(list[x])

choice = input('What would you like help with today?:')
correctedchoice = int(choice) - int(1)

if int(choice) > len(list):
    print("No")
else:
    print(choice)



list = ['hello', 'hel', 'hi']

[print(i) for i in list]


for x in range(len(list)):
    print(list[x])
