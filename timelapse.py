from time import sleep
import threading
from os import listdir
from os.path import isfile, join
from shutil import copyfile
from subprocess import Popen, PIPE

DIR = 'static/timelapse/'


class Timelapse(object):

    def __init__(self, logger):
        self.logger = logger
        self.thread = threading.Thread(target = self.take_pics)
        self.thread.setDaemon(True)
        self.thread.start()


    def is_image(self, path):
        return isfile(path) and path.split('.')[-1] == 'jpg' 

    def take_pics(self):
        while True:

            now_image = 'static/now.jpg'


            if isfile(now_image):
                images = [f for f in listdir(DIR) if self.is_image(join(DIR,f))]
                try:
                    next_index = max([int(i.split('-')[0]) for i in images]) + 1
                except:
                    next_index = 0

                copyfile(now_image, DIR + '%s-image.jpg' % next_index)


            process = Popen(['fswebcam', '-r', '1024x768', '-d', '/dev/video0', '--save', now_image], stdout=PIPE)
            stdout, stderr = process.communicate()

            sleep(60)
