import socket
import re
import time
import operator
import pyautogui as pag

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = "...."
BOT = "GMBot"
CHANNEL = "gmchatplayschess"
OWNER = "gmchatplayschess"
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" + "NICK " + BOT + "\n" + "JOIN #" + CHANNEL + "\n").encode())

moveDic = {}

def joinchat():
    loading = True
    while loading:
        readbuffer_join = irc.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        for line in readbuffer_join.split("\n")[0:1]:
            print(line)
            loading = loadingComplete(line)

def loadingComplete(line):
    print("TEST:" ,":End of /NAMES list" in line)
    if ":End of /NAMES list" in line:
        print("bot has joined " + CHANNEL + "'s Channel!")
        sendMessage(irc, "chat room joined!")
        return False
    else:
        print("not joined")
        return True

def sendMessage(irc, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    irc.send((messageTemp + "\n").encode())


def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user


def getMessage(line):
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    
    return message
#joinchat()

#console - check if it was a server message
def console(line):
    if "PRIVMSG" in line:
        return False
    else:
        return True


def checkValid(line):
    return re.match(r'[a-h][1-8][a-h][1-8]', line)
    

def updateDict(line):
    if line not in moveDic:
        moveDic[line] = 1
    else:
        moveDic[line] += 1

def chooseMove():
    global moveDic
    try:
        move = max(moveDic.items(), key=operator.itemgetter(1))[0]
    except:
        move = "error"
    moveDic = {}
    return move


def takePrint():
    


def makeMove(move):
    startCoordX = 200
    startCoordY = 400
    interval = 50
    print(move)
    values = [ord(move[0]) - 96, int(move[1]), ord(move[2]) - 96, int(move[3])]
    print(values)
    #move[0] = ord(move[0]) - 96
    #move[2] = ord(move[0]) - 96
    pag.moveTo(startCoordX + (interval * (values[0]-1)), startCoordY + (interval * (values[1]-1)), 1)
    pag.click()
    pag.moveTo(startCoordX + (interval * (values[2]-1)), startCoordY + (interval * (values[3]-1)), 1)
    pag.click()


def newGame():
    pag.moveTo(200,300)
    pag.click()

while True:
    sendMessage(irc, "/me Start voting")
    t_end = time.time() + 20
    while time.time() < t_end:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and console(line):
                rp = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(rp)
                print(rp)
                continue
            else:
                print("user:", getUser(line), "  message:", getMessage(line))
                if checkValid(getMessage(line)) or (getMessage(line) == "newgame"):
                    updateDict(getMessage(line))
                    
                else:
                    print("invalid move")
    
    sendMessage(irc, "/me End voting")
    print(moveDic)
    move = chooseMove()
    print("Move chosen:", move)
    if move == "newgame":
        newGame()
    elif move == "error":
        continue
    else:
        makeMove(move)
    
    time.sleep(5)


        


#sendMessage(irc, "hello everyone")
