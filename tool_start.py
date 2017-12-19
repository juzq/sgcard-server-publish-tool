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
        self.init_by_ini()

    def update_text_status(self, msg):
        self.text_status.SetLabel(msg)

    def update_btn_start(self, enable):
        self.btn_start.Enable(enable)

    def append_text_result(self, msg):
        self.text_result.AppendText(time.strftime('%H:%M:%S') + ' ' + msg)

    def event_dir_changed( self, event):
        path = event.GetPath()
        self.dir_changed(path)

    def dir_changed(self, path):
        self.is_programmer = False
        file_str = '您的身份已识别为：“小小策划”\n以下是你要发布的文件，请逐个核对，核对完毕后请点击“开始发布”\n'
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
            jdk_path = self.jdk_picker.GetPath()
            if jdk_path != '':
                file_str = get_pro_msg(path, jdk_path)
            else:
                file_str = get_pro_msg(path, None)
        else:
            # 禁用JDK切换
            self.jdk_static_text.Enable(False)
            self.jdk_picker.Enable(False)
            self.check_csv.Enable(False)

        self.text_files.SetValue(file_str)

    def event_jdk_changed(self, event):
        self.jdk_changed(event.GetPath())

    def jdk_changed(self, path):
        self.text_files.Clear()
        self.text_files.SetValue(get_pro_msg(self.dir_picker.GetPath(), path))

    def his_select( self, event ):
        self.text_result.Clear()
        if os.path.exists(env.work_history_path):
            file_obj = open(env.work_history_path, 'r', encoding='utf8')
            try:
                line = file_obj.readline()
                while line:
                    self.text_result.AppendText(line)
                    line = file_obj.readline()
            finally:
                file_obj.close()
        else:
            self.text_result.SetValue('没有发布历史')

    def update_select( self, event ):
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
        Publish(srv_type, release_name, self.choi_srv.GetCount(), path, self.is_programmer,
                self.jdk_picker.GetPath(), self.check_csv.IsChecked())
        # 保存操作记录
        if not os.path.exists(env.work_path):
            os.mkdir(env.work_path)
        file_obj = open(env.work_history_path, 'a+', encoding= 'utf8')
        try:
            file_obj.writelines(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + release_name + srv_type_cn + '\t' + path +
                                '\n')
        finally:
            file_obj.close()

    def tool_close(self, event):
        if self.dir_picker.GetPath() != '':
            if not os.path.exists(env.work_path):
                os.mkdir(env.work_path)
            file_obj = open(env.work_config_path, 'w')
            try:
                    file_obj.writelines(env.work_config_release + '=' + str(self.choi_relea.GetSelection()) + '\n')
                    file_obj.writelines(env.work_config_srv_type + '=' + str(self.choi_srv.GetSelection()) + '\n')
                    file_obj.writelines(env.work_config_dir_path + '=' + self.dir_picker.GetPath() + '\n')
                    file_obj.writelines(env.work_config_jdk_path + '=' + self.jdk_picker.GetPath() + '\n')
                    file_obj.writelines(env.work_config_upload_csv + '=' + str(self.check_csv.GetValue()) + '\n')
            finally:
                file_obj.close()
                wx.Exit()
        else:
            wx.Exit()

    def init_by_ini(self):
        if os.path.exists(env.work_config_path):
            file_obj = open(env.work_config_path, 'r')
            try:
                line = file_obj.readline()
                while line:
                    values = line.replace('\n', '').split('=')
                    if values[0] == env.work_config_release:
                        self.choi_relea.SetSelection(int(values[1]))
                    elif values[0] == env.work_config_srv_type:
                        self.choi_srv.SetSelection(int(values[1]))
                    elif values[0] == env.work_config_dir_path:
                        path = values[1]
                        if path == '' or not os.path.exists(path):
                            path = os.path.expanduser('~')
                        self.dir_picker.SetPath(path)
                        self.dir_changed(path)
                    elif values[0] == env.work_config_jdk_path:
                        path = values[1]
                        if path != '' and os.path.exists(path):
                            self.jdk_picker.SetPath(path)
                            if self.is_programmer:
                                self.jdk_changed(path)
                    elif values[0] == env.work_config_upload_csv:
                        self.check_csv.SetValue(values[1] == 'True')
                    line = file_obj.readline()
            finally:
                file_obj.close()


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
        msg += '您选择的项目路径：' + proj_path + '\n'
        msg += '请确认所有文件已保存，确认完毕请点击“开始发布”'
    else:
        msg += '没有找到您的JDK，请重新选择JDK路径'
    return msg


if __name__ == "__main__":
    app = wx.App(False)
    frame = RunTool(None)
    frame.Show()
    # 开启程序
    app.MainLoop()