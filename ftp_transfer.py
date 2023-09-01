import ftplib
import os


def plain_ftp(docpath, server='192.168.1.50'):
    ftp = ftplib.FTP(server)
    ftp.login('anonymous', 'xxx@xxx.xxx')
    ftp.cwd('/public/')
    ftp.storbinary(
        'STOR ' + os.path.basename(docpath),
        open(docpath, 'rb'),
        1024
    )
    ftp.quit()
