from threading import Thread
import darknet
import sys
import producer
import recorder
import receiver as recv
from multiprocessing import Process

def getProgram(user):
  progdict = {}
  def testprog(prog, sour, dest, action, args, data):
    print('testproc:',data)
  progdict['testprog'] = testprog

  def talker(prog, sour, dest, action, args, data): 
    producer.response(prog, dest, sour, 'response', (), 'connected')

    rcdr = recorder.recoder()
    rcdrthr = Process(target=rcdr.recoder, args=(dest, sour, user,), daemon=True)
    rcdrthr.start()
  
    receiver = recv.receiver()
    receiver.play(dest, sour, 'pi', )  
    #rcdrthr.terminate()
    #rcdrthr.join()
    print('...........................')
    return 
  progdict['talker'] = talker

  def monitorhome(prog, sour, dest, action, args, data):
    detectP = Process(target=darknet.getObject, args=(prog, sour, dest, 'response', str(args), str(data), './tmp.jpeg',), daemon=True)
    detectP.start()
    #detectP.join()
    
  progdict['monitorhome'] = monitorhome
  
  def icebox(prog, sour, dest, action, args, data):
    print('ice')
    detectP = Process(target=darknet.getObject, args=(prog, sour, dest, 'response', str(args), str(data), './frut3.jpg',), daemon=True)
    detectP.start()
    #detectP.join()
    '''import subprocess as sub
    p = sub.Popen(['python', './darknet.py', prog, sour, dest, action, str(args), str(data), './frut3.jpg' ],stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()'''
  progdict['icebox'] = icebox
  
  return progdict
