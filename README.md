# ISU_FTPS_Tool
A script to copy files from a local directory to an FTP or FTPS server, with configuration from an ini file.

Possible configurations in the ini file (with exxample):

[ServerConf]
server: ftp.example.com
port: 21
user: U
pass: 1234

;Set connection to SFTP instead of FTP (possible values: 0 - FTP  or 1 - SFTP)
secure_conn: 0 
 
[FileConf]
target_dir: /Remote/Something
copy_dir: /Users/Desktop/test
