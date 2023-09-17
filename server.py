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
                    arr = reply.split("::")
                    if arr[1] != "todo": print("Recieved: " + reply)
                    id = int(arr[0])                 
            
                    message = arr[1].split(",,,")
                    match message[0]:
                        case "AddCard":
                            for i in range(int(message[1])):
                                self.librarys[id].append(message[2].strip())

                        case "Shuffle":
                            random.shuffle(self.librarys[id])
                        case "Draw":
                            if len(self.librarys[id]) != 0:
                                name = self.librarys[id].pop()
                                Cost, Type, Subtype, Text_Box = self.db[name]
                                print(id)
                                print(name)
                                reply = str(id) + "::Draw,,," + name + ",,," + Cost + ",,," + Type + ",,," + Subtype + ",,," + Text_Box
                                print("3")
                                self.addToDO(reply, -1)
                                print(self.todoque)
                        case "Click":
                            self.addToDO(reply, id)
                        case "todo":
                            if len(self.todoque[id]) != 0:
                                print("todo work exists")
                                ret = self.todoque[id].pop(0)
                                print("Sent: " + ret)
                                conn.sendall(str.encode(ret))
                                continue
                    conn.sendall(str.encode(str(id)+ "::Noted"))
            except:
                break   
        print("Connection Closed")
        print(self.todoque)
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
    