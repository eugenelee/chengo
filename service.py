import tornado.ioloop
import tornado.web
import subprocess
from subprocess import Popen, PIPE

class MainHandler(tornado.web.RequestHandler):
    def get(self):
#        self.write(execfile("chengo.py chen.txt"))
        output = Popen(['python', 'chengo.py', 'chen.txt'], stdout=PIPE).communicate()[0]
        self.write(output)
#        self.write(subprocess.call("python chengo.py chen.txt", shell=True))
#import subprocess

#subprocess.call("test1.py", shell=True)


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
