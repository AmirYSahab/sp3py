'''
Created on Aug 17, 2020

@author: amir
'''
import os, gzip
import datetime
from utils.dtime import gnss_time
import io
import __codecs__
import pandas as pd
import threading
from time import sleep
import numpy as np
import sched, time
import matplotlib.pyplot as plt



from threading import Timer

class stream(object):
    def __init__(self):
        self._timer     = None
        self.is_running = False
        self.stop_running = False
        
        castinfo = __rinex__()
        url = castinfo.generate_url(leo = 'champ', date = (2002,2,1))
        castinfo.download(url=url)
        file_path = '{}/{}'.format(castinfo.download_path,url.split(sep='/')[-1])
        castinfo.unzip(file_path)
        castinfo.hatanaka2rinex(castinfo.hpath)
        castinfo.read(castinfo.path, return_raw=True)
        self.data = castinfo.data
        self.obsNum = len(castinfo.data['observations'])
        self.interval = castinfo.header['interval']
        #self.printit(self.j)
        self.cast(castinfo)
    
    def cast(self, castinfo):
        for data in castinfo.data['observations']:
            threading.Thread()
            print(np.shape(data))
            sleep(self.interval)
            return(data)
            
            
    def printit(self, j):
        if not self.stop_running:
            
            threading.Timer(0, self.printit).start()#self.interval
            self.stop_running = False
            output = {'flags' : self.data['flags'], 'prns': self.data['sv'], 'observations': self.data['observations'][self.j]}
            
            if j>self.obsNum: self.stop_running = True
            #print(self.data['observations'][j])
        else:
            return
            
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self.start)
            self._timer.start()
            print('blabla')
            #self.is_running = True
    def stop(self):
        self._timer.cancel()
        self.is_running = False

class __rinex__:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.download_path = '{}/{}'.format(self.script_path,'downloads')
        self.check_path(self.download_path)
        self.file_name = ''
        self.data_dict = {'rinex':{}}
    
    def check_path(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
            
    def file_exits(self, path):
        return os.path.exists(path)
        
    def download(self,url, email):
        #### reference : https://cddis.nasa.gov/Data_and_Derived_Products/CDDIS_Archive_Access.html

        self.file_name = url.split(sep='/')[-1]
        file_path = '{}/{}'.format(self.download_path,self.file_name)
        if not self.file_exits(file_path):
            #wget --ftp-user anonymous --ftp-password {} ftps://gdc.cddis.eosdis.nasa.gov/doris/data/cs2/2017/cs2rx17001.001.Z
            cmd_init = 'wget --ftp-user anonymous --ftp-password {}'.format(email)
            command = '{} {} -P {}'.format(cmd_init, url, self.download_path)
            os.system(command)

    def unzip(self,path):
        if path.split(sep='.')[-1] == 'Z':
            name = path.split(sep = '/')[-1].split(sep='.')[:-1]
            cmd = 'uncompress -k {}'.format(path)
            self.hpath = path[:-2]
            if not self.file_exits(self.hpath):
                os.system(cmd)
            else:
                print('File {} is already uncompressed         \n Continuing to convert hatanaka to rinex ...'.format(path.split(sep = '/')[-1]))
    
    def generate_url(self, leo = str, date=datetime):
        #ftps://gdc.cddis.eosdis.nasa.gov/doris/data/cs2/2017/cs2rx17001.001.Z
        #date = (2010,01,01)
        if leo == 'champ':
            base_url = 'ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/satellite/champ'
            t = gnss_time(date)
            doy = t.doy()
            return '{0}/{1}/{2:03d}/cham{2:03d}0.{3}d.Z'.format(base_url,date[0], doy,str(date[0])[-2:])
    
    def hatanaka2rinex(self):
        
        cmd = '{}/RNXCMP/bin/CRX2RNX {}'.format(self.script_path,self.hpath)
        self.path = '{}{}'.format(self.hpath[:-1],'o')
        if not self.file_exits(self.path):
            os.system(cmd)
        else:
            print(' Hatanaka file {} is already converted to rinex         \n Continuing to read the rinex file ...'.format(self.hpath.split('/')[-1]))
        
    def read(self,path, return_type = 'tensor'):
        with open(path,'r') as rinex_:
            rinex = rinex_.readlines()
            rinex_.close()
            if return_type == 'xDataFrame':
                self.data = __codecs__.read_rinex(rinex, return_type = return_type).observations
            elif return_type == 'raw':
                self.data, self.header = __codecs__.read_rinex(rinex, return_type = return_type).observations
            elif return_type == 'tensor':
                self.data = __codecs__.read_rinex(rinex, return_type = return_type)
            print('Rinex file is piled into data submodule')
            #a = pd.DataFrame(observations.body)

class __sp3__:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.download_path = '{}/{}'.format(self.script_path,'downloads')
        self.check_path(self.download_path)
        self.file_name = ''
        self.data_dict = {'sp3':{}}
        
    def check_path(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
    
    def file_exits(self, path):
        return os.path.exists(path)
    
    def download(self,url, email):
        #### reference :         
        # problem in download
        self.file_name = url.split(sep='/')[-1]
        file_path = '{}/{}'.format(self.download_path,self.file_name)
        if not self.file_exits(file_path):
            # Now grab the page or pages we care about.
            cmd_init = 'wget --ftp-user anonymous --ftp-password {}'.format(email)
            command = '{} {} -P {}'.format(cmd_init, url, self.download_path)
            os.system(command)
    
    def unzip(self,path):
        if path.split(sep='.')[-1] == 'Z':
            name = path.split(sep = '/')[-1].split(sep='.')[:-1]
            cmd = 'uncompress -k {}'.format(path)
            self.path = path[:-2]
            if not self.file_exits(self.path):
                os.system(cmd)
            else:
                print('File {} is already uncompressed ...'.format(path.split(sep = '/')[-1]))

    def generate_url(self, system = str, date=datetime, source = 'gfz'):
        #date = (2010,01,01)
        
        t = gnss_time(date)
        gpsWeek = t.time.gpsWeek
        gps_weekDaya = t.time.weekDay
        
        if system == 'gps':
            base_url = 'ftps://gdc.cddis.eosdis.nasa.gov/gnss/products'
            
            return '{0}/{1:04d}/{2}{3:04d}{4}.sp3.Z'.format(base_url,gpsWeek,'gfz',gpsWeek,gps_weekDaya)
        elif system =='glonass':
            base_url = 'ftps://gdc.cddis.eosdis.nasa.gov/glonass/products'
            
            return '{0}/{1:04d}/{2}{3:04d}{4}.sp3.Z'.format(base_url,gpsWeek,'igx',gpsWeek,gps_weekDaya)
        
    def read(self,path, return_type = False):
        with open(path,'r') as sp3_:
            sp3 = sp3_.readlines()
            sp3_.close()
            
            
            if return_type == 'raw':
                data = __codecs__.read_sp3(sp3, return_raw = return_type).observations
            elif return_type == 'xDataFrame':
                data, self.header = __codecs__.read_sp3(sp3, return_type = return_type).observations
            elif return_type == 'tensor':
                data = __codecs__.read_sp3(sp3, return_type = return_type).data
                
            print('Rinex file is piled into data submodule')
            #a = pd.DataFrame(observations.body)
            return data
class DO():
    def __init__(self, human_command):
        expected_commands = ['url', 'download', 'unzip', 'convert', 'read', 'raw']
        self.modules = ['generate_url', 'download', 'unzip', 'hatanaka2rinex', 'read', 'raw']
         
        self.module_list = [module for cmd, module in zip(expected_commands, self.modules) if human_command.find(cmd) != -1]

        self.execute(human_command)

    def execute(self, command, systems = ['champ', 'GOCE', 'GRACE']):
        # call the class
        rinex = __rinex__()
        if self.module_list[0] == self.modules[0]:
            date = '({})'.format(command.split('(')[1].split(')')[0])
            leo = [leo for leo in systems if command.find(leo) != -1][0]
            url = rinex.generate_url(leo = leo, date = eval(date))
            rinex.download(url=url)
            file_path = '{}/{}'.format(rinex.download_path,url.split(sep='/')[-1])
            rinex.unzip(file_path)
            rinex.hatanaka2rinex(rinex.hpath)
            if 'raw' in self.module_list:
                rinex.read(rinex.path, return_raw=True)
            else:
                rinex.read(rinex.path)
        else:
            if 'download' in self.module_list:
                url = command.split('"')[1]    
                rinex.download(url = url) 
                file_path = '{}/{}'.format(rinex.download_path,url.split(sep='/')[-1])
                rinex.unzip(file_path)
                rinex.hatanaka2rinex(rinex.hpath)
                if 'raw' in self.module_list:
                    rinex.read(rinex.path, return_raw=True)
                else:
                    rinex.read(rinex.path)
            else:
                file_path = command.split('"')[1] 
                if 'unzip' in self.module_list:
                    rinex.unzip(file_path)
                    rinex.hatanaka2rinex(rinex.hpath)
                    if 'raw' in self.module_list:
                            rinex.read(rinex.path, return_raw=True)
                    else:
                        rinex.read(rinex.path)
                else:
                    if 'hatanaka2rinex' in self.module_list: 
                        rinex.hatanaka2rinex(file_path)
                        if 'raw' in self.module_list:
                            rinex.read(rinex.path, return_raw=True)
                        else:
                            rinex.read(rinex.path)
                    else:
                        if 'raw' in self.module_list:
                            rinex.read(rinex.path, return_raw=True)
                        else:
                            rinex.read(file_path)
        self.data = rinex.data
                             
if __name__ == '__main__':
    #type: 'HumanLevel'
    type = 'rinex'
#     type = 'sp3'
    email ='e189904@metu.edu.tr' #input('give me your email adress registered to https://cddis.nasa.gov/Data_and_Derived_Products/CDDIS_Archive_Access.html')
    if type == 'HumanLevel_rinex':
        
        # you can call the modules in two ways:
        # method 1:
        # possible commands
        
        keywords = ['url', 'download', 'unzip', 'convert', 'read']
        command0 = 'generate url of champ for date (2002,2,1) & download rinex & unzip it & convert hatanaka to rinex & read it'
        command1 = 'download rinex from url " x " & unzip it & convert hatanaka to rinex & read it'
        command2 = 'unzip from " x " & convert hatanaka to rinex & read it'
        command3 = 'convert hatanaka to rinex from " x " & read it'
        command4 = 'read rinex from path " x "'
        
        chip = DO(human_command = command0)
        
        print('x')
    if type == 'rinex':
        rinex = __rinex__()
        # method 2:
        url = rinex.generate_url(leo = 'champ', date = (2002,2,1))
        rinex.download(url=url, email = email)
        file_path = '{}/{}'.format(rinex.download_path,url.split(sep='/')[-1])
        rinex.unzip(file_path)
        rinex.hatanaka2rinex()
        rinex.read(rinex.path)
        rinex.data
    if type == 'sp3':
        gps_sp3 = __sp3__()
        gpsurl = gps_sp3.generate_url('gps', date = (2002,2,1))
        gps_sp3.download(gpsurl, email=email)
        file_path = '{}/{}'.format(gps_sp3.download_path,gpsurl.split(sep='/')[-1])
        gps_sp3.unzip(file_path)
        gps_sp3.read(gps_sp3.path, return_type='tensor')
        
        
        glonass_sp3 = __sp3__()
        glonassurl = glonass_sp3.generate_url('glonass', date = (2002,2,1))
        glonass_sp3.download(glonassurl, email=email)
        file_path = '{}/{}'.format(glonass_sp3.download_path,glonassurl.split(sep='/')[-1])
        glonass_sp3.unzip(file_path)
        glonass_sp3.read(glonass_sp3.path, return_type='tensor')
        
        '''
        for sat in glonass_sp3.data['rows']:
            fig, axs = plt.subplots(4, 1)
            for o in range(len(glonass_sp3.data['columns'])):
                axs[o].plot(glonass_sp3.data['tensor'][sat,o,:],'.') 
        plt.show()
        '''
        
    
'''
#     castinfo = __rinex__()
#     url = castinfo.generate_url(leo = 'champ', date = (2002,2,1))
#     castinfo.download(url=url)
#     file_path = '{}/{}'.format(castinfo.download_path,url.split(sep='/')[-1])
#     castinfo.unzip(file_path)
#     castinfo.hatanaka2rinex(castinfo.hpath)
#     castinfo.read(castinfo.path, return_raw=True)
    def hello(input):
        print('hey {}'.format(input))
        #j+=1
    j = 0
    print("starting...")
    rt = stream() # it auto-starts, no need of rt.start()
#     try:
#         print('hey')
#         #sleep(6) # your long-running job goes here...
#     finally:
#         rt.stop() # better in a try/finally block to make sure the program ends!
'''
