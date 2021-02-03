# ISU_FTPS_Tool
A script to copy files from a local directory to an FTP or SFTP server, with configuration from an ini file.

Possible configurations in the ini file (with example):

* Server Configuration
  * server: ftp.example.com
  * port: 21
  * user: U
  * pass: 1234
  * secure_conn: 0 (0 - FTP, 1 - SFTP)
 
* File Path Configuration
  * target_dir: /Remote/Something
  * copy_dir: /Users/Desktop/test
  
The program uses ISU_FTPS_Tool_conf.ini as default, but it can be changed with a command line argument as follows:
  - ISU_FTPS_Tool.py -p spec --> The program will add 'spec' as a postfix and will search for ISU_FTPS_Tool_conf_spec.ini
 
