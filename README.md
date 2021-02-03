# ISU_FTPS_Tool
A script to copy files from a local directory to an FTP or FTPS server, with configuration from an ini file.

Possible configurations in the ini file (with exxample):

* Server Configuration
  * server: ftp.example.com
  * port: 21
  * user: U
  * pass: 1234
  * secure_conn: 0 
 
* File Path Configuration
  * target_dir: /Remote/Something
  * copy_dir: /Users/Desktop/test
