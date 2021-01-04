'''
Created on Jan 4, 2021

@author: amir
'''
from rinexReader import __sp3__ 
import datetime

if __name__ == '__main__':
    year = input('year />:')#2002
    month = input('month />:')
    day = input('day />:')
    n_days = int(input('number of days you need to download />:'))
    email = input('Input the registered email to ftps://gdc.cddis.eosdis.nasa.gov/ />:')
    # read rinex
    dtime = datetime.datetime.strptime('{}-{}-{}'.format(year,month,day),"%Y-%m-%d")
    gps_sp3 = __sp3__()
    glonass_sp3 = __sp3__()
    
    gps_sp3Data = [None]*n_days
    glonass_sp3Data = [None]*n_days
    
    for day_ in range(n_days):
            d = dtime + datetime.timedelta(days = day_)
            
            # read sp3 for gps
            gpsurl = gps_sp3.generate_url('gps', date = (d.year,d.month,d.day))
            
            gps_sp3.download(gpsurl, email=email)
            
            file_path = '{}/{}'.format(gps_sp3.download_path,gpsurl.split(sep='/')[-1])
            
            gps_sp3.unzip(file_path)
            
            gps_sp3Data[day_] = gps_sp3.read(gps_sp3.path, return_type='tensor')
            
            # read sp3 for glonass
            glonass_sp3 = __sp3__()
            
            glonassurl = glonass_sp3.generate_url('glonass', date = (d.year,d.month,d.day))
            
            glonass_sp3.download(glonassurl, email=email)
            
            file_path = '{}/{}'.format(glonass_sp3.download_path,glonassurl.split(sep='/')[-1])
            
            glonass_sp3.unzip(file_path)
            
            glonass_sp3Data[day_] = glonass_sp3.read(glonass_sp3.path, return_type='tensor')
            
    print('gps_sp3 data is downloaded and read in rnxData for {} day/s'.format(len(gps_sp3Data)))
    print('glonass_sp3 data is downloaded and read in rnxData for {} day/s'.format(len(glonass_sp3Data)))
    print('gps_sp3Data[day_].observations has keys: {}'.format(gps_sp3Data[day_].keys()))
    print('glonass_sp3Data[day_].observations has keys: {}'.format(glonass_sp3Data[day_].keys()))
    print('gps_sp3Data[day_].observations["help"]:{}'.format(gps_sp3Data[day_]['help']))
    print('glonass_sp3Data[day_].observations["help"]:{}'.format(glonass_sp3Data[day_]['help']))
            
            
            
            
            
            
            