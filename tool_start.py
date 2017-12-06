# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 启动
# ------------------------------------------------------------------------------
import os, time, webbrowser

import wx
from wx.lib.pubsub import pub
from publish import Publish
import ui, env


class RunTool(ui.PublishTool):
    def __init__(self,parent):
        ui.PublishTool.__init__(self, parent)
        pub.subscribe(self.update_text_status, "update_text_status")
        pub.subscribe(self.update_btn_start, "update_btn_start")
        pub.subscribe(self.append_text_result, "append_text_result")
        self.is_programmer = False

    def update_text_status(self, msg):
        self.text_status.SetLabel(msg)

    def update_btn_start(self, enable):
        self.btn_start.Enable(enable)

    def append_text_result(self, msg):
        self.text_result.AppendText(time.strftime('%H:%M:%S') + ' ' + msg)

    def dir_changed( self, event):
        path = event.GetPath()
        self.is_programmer = False
        file_str = '您的身份已识别为：“策划汪”，以下是你要发布的文件，请逐个核对：\n'
        if not check_dir_empty(path):
            return
        # 遍历本地目录
        for f in os.listdir(path):
            if f == 'src':
                self.is_programmer = True
                break
            else:
                file_str += f + ' '
        if self.is_programmer:
            # 启用JDK切换
            self.jdk_static_text.Enable(True)
            self.jdk_picker.Enable(True)
            self.check_csv.Enable(True)
            file_str = get_pro_msg(path, None)
        else:
            # 禁用JDK切换
            self.jdk_static_text.Enable(False)
            self.jdk_picker.Enable(False)
            self.check_csv.Enable(False)

        self.text_files.SetValue(file_str)

    def jdk_changed(self, event):
        self.text_files.Clear()
        self.text_files.SetValue(get_pro_msg(self.dir_picker.GetPath(), event.GetPath()))

    def his_select( self, event ):
        webbrowser.open('https://git.ppgame.com/lijixue/sgcard-server-publish-tool/blob/master/CHANGELOG.md', new=0,
                        autoraise=True)

    def abt_select( self, event ):
        webbrowser.open('http://192.168.2.118/wordpress/2017/11/15/苍龙服务器发布工具gui版出炉啦', new=0, autoraise=True)

    def start(self, event):
        path = self.dir_picker.GetPath()
        # 未选择文件夹
        if path == '':
            wx.MessageBox('请选择要发布的文件夹', '错误', wx.ICON_ERROR)
            return
        if not check_dir_empty(path):
            return
        release = self.choi_relea.GetSelection()
        srv_type = self.choi_srv.GetSelection()
        release_name = self.choi_relea.GetString(release)
        srv_type_cn = self.choi_srv.GetString(srv_type)
        choice = wx.MessageBox('是否确定要发布到“' + release_name + '版' + srv_type_cn + '”', '确认',
                               wx.YES_NO | wx.ICON_EXCLAMATION)
        # 选择了取消
        if choice != wx.YES:
            return
        # 清空上次启动结果
        self.text_result.Clear()
        Publish(srv_type, release_name, self.choi_srv.GetCount(), self.dir_picker.GetPath(), self.is_programmer,
                self.jdk_picker.GetPath(), self.check_csv.IsChecked())


def check_dir_empty(path):
    # 判断本地参数是目录还是文件
    if not os.path.isdir(path):
        wx.MessageBox('选择的不是文件夹', '错误', wx.ICON_ERROR)
        return False
    if not os.listdir(path):
        wx.MessageBox('所选文件夹为空', '错误', wx.ICON_ERROR)
        return False
    return True


def get_pro_msg(proj_path, jdk_path):
    msg = '您的身份已识别为：“服务器大佬”\n'
    jdk_ver = env.check_java(jdk_path)
    if jdk_ver is not None:
        msg += '您的JDK版本是：' + jdk_ver + '，请确认\n'
        msg += '您选择的项目路径是：' + proj_path + '\n'
        msg += '请确认该项目所有文件已保存，确认完毕请点击“开始发布”'
    else:
        msg += '没有找到您的JDK，请指定JDK路径'
    return msg


if __name__ == "__main__":
    app = wx.App(False)
    frame = RunTool(None)
    frame.Show()
    # 开启程序
    app.MainLoop()