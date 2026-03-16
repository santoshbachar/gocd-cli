from gocd_cli.commands.pipeline import List, Check, Unpause
from gocd import Server

# Config – change if needed
HOST = "http://localhost:8153"
USER = "admin"
PASS = "badger"
PIPELINE = "up42"


server = Server(HOST, USER, PASS)
# cmd = List(server).run()

cmd = Check(server, "up42", 1).run()

# cmd = Unpause(server, PIPELINE).run()
