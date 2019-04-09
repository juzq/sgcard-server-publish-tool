# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 发布
# ------------------------------------------------------------------------------
import subprocess
import traceback
from threading import Thread

import wx
from pubsub import pub

import env
import sftp


class Publish(Thread):
    def __init__(self, srv_type, release_name, choi_srv_size, dir_path, is_programmer, maven_path, upload_csv):
        Thread.__init__(self)
        self.srv_type = srv_type
        self.release_name = release_name
        self.choi_srv_size = choi_srv_size
        self.dir_path = dir_path
        self.is_programmer = is_programmer
        self.maven_path = maven_path
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
                build_code(self.maven_path, self.dir_path)

            # 服务器信息
            server_info = env.server_info[self.release_name]
            # 服务器ID
            srv_index = 1
            ip = server_info['ip']
            # 列表服
            if self.srv_type == self.choi_srv_size - 1:
                srv_type_str = 'list'
            # 战斗服
            elif self.srv_type == self.choi_srv_size - 2:
                srv_type_str = 'fight'
            # 游戏服
            else:
                srv_type_str = 'game'
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
            sftp.ssh(ip, server_info['port'], server_info['username'], server_info['password'],
                     'screen -dmS ' + server_id + ' sh ' + srv_path + 'start.sh ' + env.env_user_name + ';screen -ls')
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='已提交启动服务器请求，请关注邮件通知。')
            # 更新状态
            wx.CallAfter(pub.sendMessage, "update_text_status", msg="发布完成\n")
        except Exception as e:
            wx.CallAfter(pub.sendMessage, "update_text_status", msg="发布失败\n")
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='发布失败，原因：\n' + str(e))
            print(traceback.print_exc())
        finally:
            # 启用发布按钮
            wx.CallAfter(pub.sendMessage, "update_btn_start", enable=True)


def build_code(maven_path, proj_path):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # clean
    wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在清理编译目录...\n')
    cmd = maven_path + '\\bin\\mvn.bat -f "' + proj_path + '"' + ' clean > ' + env.work_config_log_file
    # print(cmd)
    ps = subprocess.Popen(cmd, startupinfo=si)
    ps.wait()
    # package
    wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在编译打包，请稍候...\n')
    cmd = maven_path + '\\bin\\mvn.bat -f "' + proj_path + '"' + ' package >> ' + env.work_config_log_file
    ps = subprocess.Popen(cmd, startupinfo=si)
    ps.wait()
    # 打包
    wx.CallAfter(pub.sendMessage, "append_text_result", msg='编译打包完成，已在本工具目录生成日志:' +
                                                            env.work_config_log_file + '\n')


def upload_code(ip, server_info, dir_path, srv_path, srv_type_str, upload_csv):
    # 公共文件
    upload_files = {
        'target/': [srv_type_str + '-' + server_info['release_en'] + '.jar'],
        'config/': ['app-bean.xml', 'applicationContext-core.xml', 'applicationContext-taskPool.xml']
    }

    # 游戏服
    if srv_type_str == 'game':
        upload_files.update({'config/languageres/': ['language.properties', 'text_jp.properties', 'text_kr.properties',
                                                     'text_zh_cs.properties']})
        config = upload_files['config/']
        config.append('app-cfg.xml')
        config.append('app-db.xml')
        config.append('applicationContext-activeMq-receive-gs.xml')
        config.append('applicationContext-activeMq-send-gs.xml')
        config.append('app.xml')
        config.append('dispatchEvent-gs-receive.properties')
        config.append('dispatchEvent-gs-send.properties')
        config.append('logSqlFactory.xml')
        # 日文没有这个
        # config.append('repair-bean.xml')
        config.append('text.properties')
        config.append('SystemNotice.properties')
    elif srv_type_str == 'fight':
        config = upload_files['config/']
        config.append('applicationContext-activeMq-receive-ws.xml')
        config.append('applicationContext-activeMq-send-ws.xml')
        config.append('applicationContext_FightServer.xml')
        config.append('dispatchEvent-ws-receive.properties')
    elif srv_type_str == 'list':
        config = upload_files['config/']
        config.append('app-db.xml')
        config.append('applicationContext-activeMq-receive.xml')
        config.append('applicationContext-activeMq-send.xml')
        config.append('applicationContext-biz.xml')
        config.append('applicationContext-http.xml')
        config.append('applicationContext-mysql.xml')
        config.append('dispatchEvent-receive.properties')
        config.append('dispatchEvent-send.properties')
        config.append('logSqlFactory.xml')

    for directory, files in upload_files.items():
        for file in files:
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在上传' + directory + file + '\n')
            remote_dir = ''
            if 'jar' not in file:
                remote_dir = directory
            sftp.sftp_upload(ip, server_info['port'], server_info['username'], server_info['password'],
                             dir_path + '/' + directory + file, srv_path + remote_dir)

    # 上传配置表
    if upload_csv:
        wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在上传配置表...\n')
        sftp.sftp_upload(ip, server_info['port'], server_info['username'], server_info['password'],
                         dir_path + '/gameConfig/', srv_path + '/gameConfig/')
