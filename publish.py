# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 发布
# ------------------------------------------------------------------------------
import traceback
from threading import Thread

import wx
from wx.lib.pubsub import pub
import env
import sftp


class Publish(Thread):
    def __init__(self, srv_type, release_name, choi_srv_size, dir_path):
        Thread.__init__(self)
        self.srv_type = srv_type
        self.release_name = release_name
        self.choi_srv_size = choi_srv_size
        self.dir_path = dir_path
        self.start()

    def run(self):
        try:
            # 更新状态
            wx.CallAfter(pub.sendMessage, 'update_text_status', msg='正在发布')
            # 禁用发布按钮
            wx.CallAfter(pub.sendMessage, 'update_btn_start', enable=False)

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
                               env.root_path + 'scripts/stop_srv.sh ' + server_id)
            stop_sign = False
            for res in ssh_res:
                if 'success' in res or 'not open' in res:
                    stop_sign = True
            if stop_sign:
                wx.CallAfter(pub.sendMessage, "append_text_result", msg='关闭服务器成功\n')

            # 上传文件
            remote_path = env.root_path + srv_type_str + 'Srv/' + server_id + '/gameConfig/'
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在上传文件...\n')
            sftp.sftp_upload(ip, server_info['port'], server_info['username'], server_info['password'], self.dir_path
                             + '/', remote_path)
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='上传完毕\n')

            # 开启服务器
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='正在启动服务器，请稍后...\n')
            ssh_res = sftp.ssh(ip, server_info['port'], server_info['username'], server_info['password'],
                               env.root_path + 'scripts/start_srv.sh ' + srv_type_str + ' ' + server_id)
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
        except Exception as e:
            wx.CallAfter(pub.sendMessage, "update_text_status", msg="发布失败\n")
            wx.CallAfter(pub.sendMessage, "append_text_result", msg='发布失败，原因：\n' + str(e))
            print(traceback.print_exc())
        finally:
            # 启用发布按钮
            wx.CallAfter(pub.sendMessage, "update_btn_start", enable=True)