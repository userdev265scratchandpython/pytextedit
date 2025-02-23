import hashlib, random, os
HasMadeKey = False
while not HasMadeKey:
    usern = os.getlogin()
    if len(usern) >= 9:
        print("c1")
        uname = usern
    elif len(usern) == 8:
        print("c2")
        safe = random.randint(0, 9)
        uname = f"{safe}{usern}"
    elif len(usern) == 7:
        print("c3")
        safe = random.randint(10, 99)
        uname = f"{safe}{usern}"
    elif len(usern) == 6:
        print("c4")
        safe = random.randint(100, 999)
        uname = f"{safe}{usern}"
    elif len(usern) == 5:
        print("c5")
        safe = random.randint(1000, 9999)
        uname = f"{safe}{usern}"
    elif len(usern) == 4:
        print("c6")
        safe = random.randint(10000, 99999)
        uname = f"{safe}{usern}"
    elif len(usern) == 3:
        print("c7")
        safe = random.randint(100000, 999999)
        uname = f"{safe}{usern}"
    elif len(usern) == 2:
        print("c8")
        safe = random.randint(1000000, 9999999)
        uname = f"{safe}{usern}"
    elif len(usern) == 1:
        print("c9")
        safe = random.randint(10000000, 99999999)
        uname = f"{safe}{usern}"
    else:
        print("no username")
        safe = random.randint(100000000, 999999999)
        uname = f"{safe}"
    cryptlevela = hashlib.sha256(uname.encode('utf-8')).hexdigest()
    lookina = random.randint(0, 9)
    lookinb = random.randint(0, 9)
    passwd = ""
    while not len(passwd) == 18:
        passwd = input("generation password (can be anything 18 characters long) :")
        if len(passwd) > 18:
            print("too long, encryption cannot proceed until it is 18 long.")
        elif len(passwd) < 18:
            print("too short, encryption cannot proceed until it is 18 long.")
    maina = cryptlevela[lookinb]
    mainb = uname[lookina]
    cur = f"{maina}{mainb}{passwd}"
    cur = f"{cur}{lookina}{cur}{lookinb}{cur}{lookina}{cur}{lookinb}{cur}{lookina}{cur}{lookinb}{cur}{lookina}{cur}{lookinb}{cur}{lookina}{cur}{lookinb}"
    endval = hashlib.sha256(cur.encode('utf-8')).hexdigest()
    try:
        endfile = open(f"{endval}.txt", "x")
        endfile.close()
    except:
        HasMadeKey = False
    else:
        HasMadeKey = True
print(endval)
print("please press any key after copying your key")
os.system("pause > nul")
