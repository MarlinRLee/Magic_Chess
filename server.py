import random
import socket
from _thread import *
import xml.etree.ElementTree as ET
  
class server:
    def __init__(self):
        self.currentId = 0
        self.todoque = []        
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = 'localhost'
        port = 5555
        #server_ip = socket.gethostbyname(server)

        #Card DB Stuff
        self.db = self.get_card_db("../text_magic_set.xml")
        self.librarys = {}
    
        try:
            self.soc.bind((server, port))
        except socket.error as e:
            print(str(e))

    def run(self):
        self.soc.listen(2)
        print("Waiting for a connection")
        while True:
            conn, addr = self.soc.accept()
            print("Connected to: ", addr)
            start_new_thread(self.threaded_client, (conn,))
            
    def threaded_client(self, conn):
        #Library stuff
        self.librarys[self.currentId] = []
        self.todoque.append([])
        
        conn.send(str.encode(str(self.currentId)))
        self.currentId += 1
        reply = ''
        while True:
            try:
                data = conn.recv(2048)
                reply = data.decode('utf-8')
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    arr = reply.split(":")
                    if arr[1] != "-1,-1": print("Recieved: " + reply)
                    id = int(arr[0])                 
            
                    message = arr[1].split(",")
                    match message[0]:
                        case "AddCard":
                            for i in range(message[1]):
                                self.librarys[self.currentId].append(message[2])
                        case "Shuffle":
                            random.shuffle(self.librarys[message[1]])
                        case "Draw":
                            if len(self.librarys[message[1]]) != 0:
                                name = self.librarys[message[1]].pop()
                                Cost, Type, Subtype, Text_Box = self.db[name]
                                reply = id + ":Draw," + name + "," + Cost + "," + Type + "," + Subtype + "," + Text_Box
                                self.addToDO(reply, -1)
                        case "Click":
                            self.addToDO(reply, id)
                        case "todo":
                            if len(self.todoque[id]) != 0:
                                conn.sendall(str.encode(self.todoque[id].pop(0)))
                    conn.sendall(str.encode(id + ":Noted"))
            except:
                break   
        print("Connection Closed")
        conn.close()
    
    def addToDO(self, mesg, skipID):
        for i in range(self.currentId):
            if i == skipID:
                continue
            self.todoque[i].append(mesg)
    
    def get_card_db(self, fileXML):
        save_map = {}
        tree = ET.parse(fileXML)
        root = tree.getroot()
        for magCard in root:
            Name, Cost, Type, Subtype, Text_Box = ("None", "None", "None", "None", "None")
            if(magCard.tag != "card"):
                continue
            for cardAttr in magCard:
                match cardAttr.tag:
                    case "name":
                        Name = cardAttr.text
                    case "cost":
                        Cost = cardAttr.text
                        if Cost is None:
                            Cost = ""
                    case "type":
                        Stype = cardAttr.find("supertype")
                        if Stype != None:
                            Type = Stype.text
                        
                        Ntype = cardAttr.find("subtype")
                        if Ntype != None and Ntype.text != None:
                            Subtype = Ntype.text
                    case "rules":
                        Text_Box = cardAttr.text
            save_map[Name] = (Cost, Type, Subtype, Text_Box)
        return save_map
            
            
if __name__ == '__main__':
    serv = server()
    serv.run()
    