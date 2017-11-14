# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 启动
# ------------------------------------------------------------------------------
import os

import wx
from wx.lib.pubsub import pub

from publish import Publish
import ui


class RunTool(ui.PublishTool):
    def __init__(self,parent):
        ui.PublishTool.__init__(self, parent)
        pub.subscribe(self.update_text_status, "update_text_status")
        pub.subscribe(self.update_btn_start, "update_btn_start")
        pub.subscribe(self.append_text_result, "append_text_result")

    def update_text_status(self, msg):
        self.text_status.SetLabel(msg)

    def update_btn_start(self, enable):
        self.btn_start.Enable(enable)

    def append_text_result(self, msg):
        self.text_result.AppendText(msg)

    def dir_changed( self, event ):
        path = event.GetPath()
        file_str = ''
        if not check_dir_empty(path):
            return
        # 遍历本地目录
        for f in os.listdir(path):
            if not os.path.isdir(f):
                file_str += f + ' '
        self.text_files.SetValue(file_str)

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
        choice = wx.MessageBox('确定要发布下列文件到“' + release_name + '版' + srv_type_cn + '”', '确认',
                               wx.YES_NO | wx.ICON_EXCLAMATION)
        # 选择了取消
        if choice != wx.YES:
            return
        # 清空上次启动结果
        self.text_result.Clear()
        Publish(srv_type, release_name, self.choi_srv.GetCount(), self.dir_picker.GetPath())


def check_dir_empty(path):
    # 判断本地参数是目录还是文件
    if not os.path.isdir(path):
        wx.MessageBox('选择的不是文件夹', '错误', wx.ICON_ERROR)
        return False
    if not os.listdir(path):
        wx.MessageBox('所选文件夹为空', '错误', wx.ICON_ERROR)
        return False
    return True


if __name__ == "__main__":
    app = wx.App(False)
    frame = RunTool(None)
    frame.Show(True)
    # 开启程序
    app.MainLoop()