# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/6/27
# Description: sftp下载上传
# ------------------------------------------------------------------------------

import os
import paramiko


def ssh(host, port, username, password, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    # stdin, stdout, stderr = chan.send(cmd)
    result = stdout.readlines()
    ssh.close()
    return result


def download(host,port,username,password,local,remote):
    sf = paramiko.Transport((host, port))
    sf.connect(username = username,password = password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    if os.path.isdir(local):#判断本地参数是目录还是文件
        for f in sftp.listdir(remote):#遍历远程目录
            print(f)
            sftp.get(os.path.join(remote+f),os.path.join(local+f))#下载目录中文件
    else:
        sftp.get(remote,local)#下载文件
    sf.close()


def sftp_upload(host, port, username, password, local, remote):
    sf = paramiko.Transport((host, port))
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    # 判断本地参数是目录还是文件
    if os.path.isdir(local):
        # 遍历本地目录
        for f in os.listdir(local):
            # 上传目录中的文件
            sftp.put(os.path.join(local+f), os.path.join(remote+f))
    else:
        # 上传文件
        sftp.put(local, remote)
    sf.close()