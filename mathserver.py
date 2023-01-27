from subprocess import PIPE,STDOUT,Popen
import socket as soc
from threading import Thread

class process_output(Thread):
    def __init__(self,p,c):
        Thread.__init__(self)
        self.p=p
        self.c=c

    def run(self) :
        while self.p.poll() is None:
          self.c.sendall(self.p.stdout.readline())
 
class mathprocess(Thread):
    def __init__(self,con):
        Thread.__init__(self)
        self.con=con
        
    def run(self):  
        p=Popen(['bc','-q'],stderr=STDOUT,stdin=PIPE,stdout=PIPE)
        outp=process_output(p,self.con)
        outp.start()
        while p.poll() is None: 
          inp =self.con.recv(1024)
          inp=inp.decode().strip()
          inp=inp+"\n"
          p.stdin.write(inp.encode())
          p.stdin.flush()

 
HOST =''
PORT=3377
s=soc.socket(soc.AF_INET,soc.SOCK_STREAM)
s.setsockopt(soc.SOL_SOCKET,soc.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen()
while True:
  con,adrs=s.accept()
  mprocess=mathprocess(con)
  mprocess.start()
  print("connection from {}:{}".format(adrs[0],adrs[1]))
