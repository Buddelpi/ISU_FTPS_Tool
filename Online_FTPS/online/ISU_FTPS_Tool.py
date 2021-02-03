'''
Created on Oct 5, 2019

@author: delpi
'''

from ftplib import FTP, FTP_TLS
import os
import ConfigParser
import argparse
import logging
import sys

########### DEFAULT CONF ####################################

########### MODIFY ########################
 
USER = 'external'
PASS = 'Titkos123'
 
########### MODIFY IF YOU WANT ############
 
SERVER = 'server.hunskate.hu'
PORT = 21
BINARY_STORE = True # if False then line store (not valid for binary files (videos, music, photos...))
TARGET_DIR = '/mukorcsolya/2019_2020/Tesztverseny/eredmenyek/' 
COPY_DIR = '/Users/delpi/Desktop/test'
SECURE_CONN = '1'

########### DO NOT MODIFY #################

LOG_FILE = 'ISU_FTPS_tool.log'

#############################################################
 
logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', filename=LOG_FILE, level=logging.INFO) 
Config = ConfigParser.ConfigParser() 
parser = argparse.ArgumentParser()
parser.add_argument('-p', type=str, default='', help="Defines the postfix, when a different ini file is used")

try:
    args = parser.parse_args()
except:
    logging.error('Wrong argument. Usage: a) No argument, thus default ini is used; b) -p [Postfix], where Postfix can be a string (eg.: -p spec --> program will use ISU_FTPS_tool_conf_spec.ini)')
    sys.exit()
 
def print_line(result):
    print(result)
 
def connect_ftps():
    #Connect to the server
    print("Step 1")
    if SECURE_CONN == '1':
        ftps = FTP_TLS(SERVER)
    else:
        ftps = FTP(SERVER)
    print("Step 2")
    ftps.set_debuglevel(2)
    print("Step 3")
    ftps.set_pasv(False)
    print("Step 4")
    ftps.connect(port=PORT, timeout=80)
    print("Step 5")
    ftps.login(USER, PASS)
    print("Step 6")
    ftps.cwd(TARGET_DIR)
    print("Step 7")
    ftps.set_pasv(True)
    print("Step 8")
    ftps.prot_p()
    #ftps.ccc()
    return ftps

 
def upload_file(ftp_connetion, upload_file_path):
 
    #Open the file
    try:
        upload_file = open(upload_file_path, 'r')
        
        #get the name
        path_split = upload_file_path.split('/')
        final_file_name = path_split[len(path_split)-1]
    
        #transfer the file
        print("Trying to store a file")
        if BINARY_STORE:
            ftp_connetion.storbinary('STOR '+ final_file_name, upload_file,blocksize=8192)
        else:
            #ftp_connetion.storlines('STOR ' + final_file_name, upload_file, print_line)
            ftp_connetion.storlines('STOR '+ final_file_name, upload_file)
            
        logging.info('Upload finished for file: '+ final_file_name + 'to server' + SERVER )
        
    except IOError as e:
        print (e.strerror)
        logging.error('Problem uploading file: '+ final_file_name + '.')
 
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                logging.warn("Wrong input in config file: %s" % option)
        except:
            logging.warn("Problem with config file: %s!" % option)
            dict1[option] = None
    return dict1

def readConfiguration():
    global USER
    global PASS
    global SERVER
    global PORT
    global TARGET_DIR
    global COPY_DIR
    global SECURE_CONN
    
    conf = "ISU_FTPS_tool_conf"
    
    if args.p != '':
        conf = conf + '_' + args.p + '.ini'
    else:
        conf = conf + '.ini'
    
    print(conf)
    
    try:
        if Config.read(conf) == []:
            logging.warn("Problem reading config file, default values will be used!")
            print("Default values instead on ini")
        else:
            USER = ConfigSectionMap("ServerConf")['user']
            PASS = ConfigSectionMap("ServerConf")['pass']
            SERVER = ConfigSectionMap("ServerConf")['server']
            PORT = ConfigSectionMap("ServerConf")['port']
            SECURE_CONN = ConfigSectionMap("ServerConf")['secure_conn']
            TARGET_DIR = ConfigSectionMap("FileConf")['target_dir'] 
            COPY_DIR = ConfigSectionMap("FileConf")['copy_dir']
    except:
        logging.warn("Problem reading config file, default values will be used!")
        print("Default values instead on ini")
    
    
    
    

def main():
    
    #Take all the files and upload all
    readConfiguration()
    
    connSuccesful = False
    
    try:
        print("Try to connect to server")
        ftps_conn = connect_ftps()
        print("Connected")
        logging.info('Connection Succesful to server: '+ SERVER)
        connSuccesful = True
    except:
        logging.error('Problem connecting to server: '+ SERVER)
    
    if connSuccesful:  
        
        try:  
            for name in os.listdir(COPY_DIR):
                full_path = COPY_DIR + '/' + name
                upload_file(ftps_conn, full_path)
        
        except:
            logging.error('Problem reaching file in copy directory. Maybe copy path is wrong.')
            
        ftps_conn.close()


if __name__ == '__main__':
    main()
    

