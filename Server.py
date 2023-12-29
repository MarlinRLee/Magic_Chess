import random
import socket
import threading
from time import sleep
import xml.etree.ElementTree as ET

class Server:
    def __init__(self):
        self.free_id = 0
        self.todo_queue = [[], []]
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.settimeout(10)
        server = '0.0.0.0'
        port = 5555
        server_ip = socket.gethostbyname(server)
        print("Server IP: " + server_ip)

        # Card DB
        self.db = self.get_card_db("../text_magic_set.xml")
        self.libraries = {}

        try:
            self.soc.bind((server, port))
        except socket.error as e:
            print(str(e))

    def run(self):
        self.soc.listen(2)
        while True:
            try:
                print("Waiting for a connection")
                conn, addr = self.soc.accept()
                print("Connected to: ", addr)
                threading.Thread(target=self.threaded_client, args=(conn,)).start()
            except socket.timeout:
                print("no clients found")
                sleep(1)
            
    def threaded_client(self, conn):
        client_id = self.free_id
        self.libraries[client_id] = []
        self.todo_queue[client_id] = []
        
        conn.send(str.encode(str(client_id)))
        self.free_id = (self.free_id + 1) % 2

        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break

                reply = data.decode('utf-8')
                arr = reply.split("::")
                client_id = int(arr[0])                 
            
                self.handle_message(client_id, arr[1], conn)
            except Exception as e:
                print(f"An error occurred: {e}")
                break   

        print("Connection Closed")
        conn.close()

    def handle_message(self, client_id, unsplit_message, conn):
        message = unsplit_message.split(",,,")
        confirmation_needed = False
        match message[0]:
            case "AddCard":
                self.handle_add_card(client_id, message)
                confirmation_needed = True
            case "Shuffle":
                random.shuffle(self.libraries[client_id])
                confirmation_needed = True
            case "Draw":
                self.handle_draw(client_id, conn)
            case "Click":
                self.add_to_do(f"{client_id}::{unsplit_message}", client_id)
                confirmation_needed = True
            case "todo":
                confirmation_needed = self.handle_todo(client_id, conn)

        if confirmation_needed:
            conn.sendall(str.encode(str(client_id) + "::Noted"))

                


    def handle_add_card(self, client_id, message):
        for i in range(int(message[1])):
            self.libraries[client_id].append(message[2].strip())

    def handle_draw(self, client_id, conn):
        if self.libraries[client_id]:
            name = self.libraries[client_id].pop()
            Cost, Type, Subtype, Text_Box = self.db[name]
            reply = f"{client_id}::Draw,,,{name},,,{Cost},,,{Type},,,{Subtype},,,{Text_Box}"
            self.add_to_do(reply, -1)
            conn.sendall(str.encode(reply))

    def handle_todo(self, client_id, conn):
        if self.todo_queue[client_id]:
            ret = self.todo_queue[client_id].pop(0)
            conn.sendall(str.encode(ret))
            return False
        return True
        

    def add_to_do(self, mesg, skip_id):
        for i in range(2):
            if i == skip_id:
                continue
            self.todo_queue[i].append(mesg)
    
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
    serv = Server()
    serv.run()
