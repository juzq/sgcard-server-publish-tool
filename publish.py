# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 发布
# ------------------------------------------------------------------------------
import traceback
import os
import subprocess
import shutil
import time
import wx
import env
import sftp
from threading import Thread
from wx.lib.pubsub import pub


class Publish(Thread):
    def __init__(self, srv_type, release_name, choi_srv_size, dir_path, is_programmer, jdk_path, upload_csv):
        Thread.__init__(self)
        self.srv_type = srv_type
        self.release_name = release_name
        self.choi_srv_size = choi_srv_size
        self.dir_path = dir_path
        self.is_programmer = is_programmer
        self.jdk_path = jdk_path
        self.start()
        self.upload_csv = upload_csv

    def run(self):
        try:
            # 更新状态
            wx.CallAfter(pub.sendMessage, 'update_text_status', msg='正在发布')
            # 禁用发布按钮
            wx.CallAfter(pub.sendMessage, 'update_btn_start', enable=False)

            # 程序猿用，需要编译代码
            if self.is_programmer:
                build_code(self.jdk_path, self.dir_path)

            # 服务器信息
            server_info = env.server_info[self.release_name]
            # 服务器ID
            srv_index = 1
            # 列表服
            if self.srv_type == self.choi_srv_size - 1:
                srv_type_str = 'list'
                ip = server_info['fight_ip']
            # 战斗服
            elif self.srv_type == self.choi_srv_size - 2:
                srv_type_str = 'fight'
                ip = server_info['fight_ip']
            # 游戏服
            else:
                srv_type_str = 'game'
                ip = server_info['ip']
                # 服务器ID
                srv_index = self.srv_type + 1
            server_id = 'honor_' + srv_type_str + '_mixed_' + server_info['release_en'] + '_' + str(srv_index)

            # 关闭服务器
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在关闭服务器，请稍后...\n')
            ssh_res = sftp.ssh(ip, server_info['port'], server_info['username'], server_info['password'],
                               env.remote_root_path + 'scripts/stop_srv.sh ' + server_id)
            stop_sign = False
            for res in ssh_res:
                if 'success' in res or 'not open' in res:
                    stop_sign = True
            if stop_sign:
                wx.CallAfter(pub.sendMessage, "append_text_result", msg='关闭服务器成功\n')

            # 上传文件
            srv_path = env.remote_root_path + srv_type_str + 'Srv/' + server_id + '/'
            if self.is_programmer:
                upload_code(ip, server_info, self.dir_path, srv_path, srv_type_str, self.upload_csv)
            else:
                wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在上传配置表...\n')
                sftp.sftp_upload(ip, server_info['port'], server_info['username'], server_info['password'],
                                 self.dir_path + '/', srv_path + '/gameConfig/')
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='上传完毕\n')

            # 开启服务器
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在启动服务器，请稍后...\n')
            ssh_res = sftp.ssh(ip, server_info['port'], server_info['username'], server_info['password'],
                               env.remote_root_path + 'scripts/start_srv.sh ' + srv_type_str + ' ' + server_id)

            deal_result(ssh_res)
        except Exception as e:
            wx.CallAfter(pub.sendMessage, "update_text_status", msg="发布失败\n")
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='发布失败，原因：\n' + str(e))
            print(traceback.print_exc())
        finally:
            # 启用发布按钮
            wx.CallAfter(pub.sendMessage, "update_btn_start", enable=True)


def build_code(jdk_path, proj_path):
    wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在初始化操作环境...\n')
    full_tool_path = proj_path + env.tool_path
    # 删除文件夹
    if os.path.exists(full_tool_path):
        shutil.rmtree(full_tool_path)
        # 睡一下避免文件还在占用中
        time.sleep(1)
    # 新建文件夹
    os.mkdir(full_tool_path)
    os.mkdir(proj_path + env.build_path)
    os.mkdir(proj_path + env.tool_path + env.config_path)
    file_object = open(full_tool_path + '\\' + env.source_list_file, 'w')
    # 添加代码
    add_files(proj_path + env.source_path, file_object)
    file_object.close()
    # 编译文件夹
    wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在编译代码，请稍候...\n')
    compile_dir(full_tool_path, jdk_path, proj_path)
    # 打包
    wx.CallAfter(pub.sendMessage, "append_text_result", msg='编译完成，正在包起来...\n')
    package(jdk_path, proj_path)
    # 拷贝config
    upload_files = {
        '\\config\\app-bean.xml',
        '\\config\\app-db.xml',
        '\\config\\app.xml',
        '\\config\\app-cfg.xml',
        '\\config\\logSqlFactory.xml'
    }
    for file in upload_files:
        file_full_path = proj_path + file
        if os.path.exists(file_full_path):
            open(full_tool_path + file, "wb").write(open(file_full_path, "rb").read())


# 添加源码到编译清单
def add_files(source_dir, file_object):
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)
        if os.path.isfile(source_file) and '.java' in source_file:
            file_object.writelines(source_file + '\n')
        if os.path.isdir(source_file):
            add_files(source_file, file_object)


# 编译目录
def compile_dir(full_tool_path, jdk_path, proj_path):
    if jdk_path == '':
        javac = 'javac'
    else:
        javac = '"' + jdk_path + '\\bin\\javac"'
    cmd = javac + ' -encoding utf-8 -sourcepath "' + full_tool_path + env.source_path + '"' + ' -Djava.ext.dirs="' + \
        proj_path + '\\lib" "@' + full_tool_path + '\\' + env.source_list_file + '" -d "' + proj_path + env.build_path \
        + '"'
    # print(cmd)
    ps = subprocess.Popen(cmd)
    ps.wait()

    # 苍龙源码中包含有坑爹的xml，无法编译，只能拷贝过来：src\com\xd100\lzll\db\sqlmap
    full_copy_source_path = proj_path + env.source_path + env.copy_source_path
    if os.path.exists(full_copy_source_path):
        copy_files(full_copy_source_path, proj_path + env.build_path + env.copy_source_path)


# 拷贝文件
def copy_files(source_dir, target_dir):
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)
        target_file = os.path.join(target_dir, file)
        if os.path.isfile(source_file):
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            if not os.path.exists(target_file) or (os.path.exists(target_file)
                                                   and (os.path.getsize(target_file) != os.path.getsize(source_file))):
                open(target_file, "wb").write(open(source_file, "rb").read())
        if os.path.isdir(source_file):
            copy_files(source_file, target_file)


# 打包
def package(jdk_path, proj_path):
    if jdk_path == '':
        jar = 'jar'
    else:
        jar = '"' + jdk_path + '\\bin\\jar"'
    cmd = jar + ' cfM "' + proj_path + env.package_path + '" -C "' + proj_path + env.build_path + '" .'
    # print(cmd)
    ps = subprocess.Popen(cmd)
    ps.wait()
    wx.CallAfter(pub.sendMessage, "append_text_result", msg='包得很成功，位置：\n' + proj_path + env.package_path + '\n')


def upload_code(ip, server_info, dir_path, srv_path, srv_type_str, upload_csv):
    upload_files = {
        'bin.zip': '',
        'config\\app-bean.xml': 'config/',
    }

    # 游戏服和列表服上传app-db
    if srv_type_str != 'fight':
        upload_files.update({'config\\app-db.xml': 'config/'})
    # 游戏服
    if srv_type_str == 'game':
        upload_files.update({'config\\app.xml': 'config/'})
        upload_files.update({'config\\app-cfg.xml': 'config/'})
        upload_files.update({'config\\logSqlFactory.xml': 'config/'})

    for file in upload_files.keys():
        wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在上传' + file + '\n')
        sftp.sftp_upload(ip, server_info['port'], server_info['username'], server_info['password'],
                         dir_path + env.tool_path + '\\' + file, srv_path + upload_files[file])

    # 上传配置表
    if upload_csv:
        wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在上传配置表...\n')
        sftp.sftp_upload(ip, server_info['port'], server_info['username'], server_info['password'],
                         dir_path + '/gameConfig/', srv_path + '/gameConfig/')


def deal_result(ssh_res):
    show_error = False
    cfg_err = False
    for res in ssh_res:
        if '配置表错误' in res:
            cfg_err = True
            wx.CallAfter(pub.sendMessage, "append_text_result", msg=res)
        elif not cfg_err and 'Exception' in res:
            if not show_error:
                wx.CallAfter(pub.sendMessage, "append_text_result", msg='服务器启动失败，请拷贝以下错误给程序：\n')
                show_error = True
            wx.CallAfter(pub.sendMessage, "append_text_result", msg=res)
        elif 'GameServer Started' in res or 'fightServer startup' in res or '启动完毕' in res:
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='服务器已启动\n')
            break
        elif not cfg_err and show_error:
            wx.CallAfter(pub.sendMessage, "append_text_result", msg=res)
    # 更新状态
    wx.CallAfter(pub.sendMessage, "update_text_status", msg="发布完成\n")
    # 发布结果
    if not cfg_err and not show_error:
        wx.CallAfter(pub.sendMessage, "append_text_result", msg='发布成功\n')
    else:
        wx.CallAfter(pub.sendMessage, "append_text_result", msg='发布失败\n')
