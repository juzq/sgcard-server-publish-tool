# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 启动
# ------------------------------------------------------------------------------
import os
import time
import webbrowser

import wx
from pubsub import pub
from publish import Publish

import ui
import env


class RunTool(ui.PublishTool):
    def __init__(self, parent):
        ui.PublishTool.__init__(self, parent)
        check_multi_open()
        pub.subscribe(self.update_text_status, "update_text_status")
        pub.subscribe(self.update_btn_start, "update_btn_start")
        pub.subscribe(self.append_text_result, "append_text_result")
        self.is_programmer = False
        self.init_by_ini()

    def update_text_status(self, msg):
        self.text_status.SetLabel(msg)

    def update_btn_start(self, enable):
        self.btn_start.Enable(enable)

    def on_release_chosen(self, event):
        self.on_rel_srv_chosen()

    def on_srv_chosen(self, event):
        self.on_rel_srv_chosen()

    def on_rel_srv_chosen(self):
        release = self.choi_relea.GetSelection()
        path = env.paths[self.choi_relea.GetString(release)][self.choi_srv.GetSelection()]
        self.dir_picker.SetPath(path)
        if path != '':
            self.dir_changed(path)
        else:
            self.text_files.SetValue('')
            # 禁用JDK切换
            self.enable_jdk_csv(False)

    def append_text_result(self, msg):
        self.text_result.AppendText(time.strftime('%H:%M:%S') + ' ' + msg)

    def event_dir_changed(self, event):
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
            # 禁用发布
            wx.CallAfter(pub.sendMessage, "update_btn_start", enable=False)
            # 启用JDK切换
            self.enable_jdk_csv(True)
            maven_path = self.maven_picker.GetPath()
            if maven_path != '':
                file_str = get_pro_msg(path, maven_path)
            else:
                file_str = get_pro_msg(path, None)
        else:
            # 禁用JDK切换
            self.enable_jdk_csv(False)
            # 启用发布按钮
            wx.CallAfter(pub.sendMessage, "update_btn_start", enable=True)

        self.text_files.SetValue(file_str)
        # 保存已选择的发布文件夹
        if self.check_save_path.IsChecked():
            release = self.choi_relea.GetSelection()
            env.paths[self.choi_relea.GetString(release)][self.choi_srv.GetSelection()] = path

    def enable_jdk_csv(self, enable):
        self.jdk_static_text.Enable(enable)
        self.maven_picker.Enable(enable)
        self.check_csv.Enable(enable)

    def event_jdk_changed(self, event):
        self.jdk_changed(event.GetPath())

    def jdk_changed(self, path):
        self.text_files.Clear()
        # 禁用发布
        wx.CallAfter(pub.sendMessage, "update_btn_start", enable=False)
        self.text_files.SetValue(get_pro_msg(self.dir_picker.GetPath(), path))

    def his_select(self, event):
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

    def edit_info_select(self, event):
        set_info()

    def update_select(self, event):
        webbrowser.open('https://git.ppgame.com/lijixue/sgcard-server-publish-tool/tags', new=0, autoraise=True)

    def start(self, event):
        path = self.dir_picker.GetPath()
        # 未选择文件夹
        if path == '':
            wx.MessageBox('请选择要发布的文件夹', '错误', wx.ICON_ERROR)
            return
        if not check_dir_empty(path):
            return
        if env.env_user_name == '':
            if not set_info():
                return
        release = self.choi_relea.GetSelection()
        srv_type = self.choi_srv.GetSelection()
        release_name = self.choi_relea.GetString(release)
        srv_type_cn = self.choi_srv.GetString(srv_type)
        # 策划发布时，直到正确输入版本名称，或者选择取消
        if not self.is_programmer:
            answer = ''
            while answer != release_name:
                box = wx.TextEntryDialog(None, release_name + srv_type_cn + '\n' + path, '发布确认', '')
                # 点击了ok
                if box.ShowModal() == wx.ID_OK:
                    answer = box.GetValue()
                    if answer != release_name:
                        wx.MessageBox('请输入确认要发布的版本：内网/日文/韩文', '错误', wx.ICON_ERROR)
                else:
                    return
        # 清空上次启动结果
        self.text_result.Clear()
        Publish(srv_type, release_name, self.choi_srv.GetCount(), path, self.is_programmer,
                self.maven_picker.GetPath(), self.check_csv.IsChecked())
        # 保存操作记录
        if not os.path.exists(env.work_path):
            os.mkdir(env.work_path)
        file_obj = open(env.work_history_path, 'a+', encoding='utf8')
        try:
            file_obj.writelines(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + release_name + srv_type_cn + '\t' + path +
                                '\n')
        finally:
            file_obj.close()

    def tool_close(self, event):
        file_obj = open(env.work_config_path, 'w')
        try:
            file_obj.writelines(env.work_config_release + '=' + str(self.choi_relea.GetSelection()) + '\n')
            file_obj.writelines(env.work_config_srv_type + '=' + str(self.choi_srv.GetSelection()) + '\n')
            file_obj.writelines(env.work_config_maven_path + '=' + self.maven_picker.GetPath() + '\n')
            file_obj.writelines(env.work_config_upload_csv + '=' + str(self.check_csv.GetValue()) + '\n')
            file_obj.writelines(env.work_config_save_path + '=' + str(self.check_save_path.GetValue()) + '\n')
            file_obj.writelines(env.work_config_paths + '=' + str(env.paths) + '\n')
            file_obj.writelines(env.work_config_user_name + '=' + str(env.env_user_name) + '\n')
        finally:
            file_obj.close()
            wx.Exit()

    def check_new_release(self):
        count = self.choi_relea.GetCount()
        if len(env.paths) != count:
            for i in range(count):
                if env.paths[self.choi_relea.GetString(i)] is None:
                    paths = []
                    for _ in range(self.choi_srv.GetCount()):
                        paths.append("")
                    env.paths[self.choi_relea.GetString(i)] = paths

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
                    elif values[0] == env.work_config_maven_path:
                        path = values[1]
                        if path != '' and os.path.exists(path):
                            self.maven_picker.SetPath(path)
                            if self.is_programmer:
                                self.jdk_changed(path)
                    elif values[0] == env.work_config_upload_csv:
                        self.check_csv.SetValue(values[1] == 'True')
                    elif values[0] == env.work_config_save_path:
                        self.check_save_path.SetValue(values[1] == 'True')
                    elif values[0] == env.work_config_paths:
                        env.paths = eval(values[1])
                    elif values[0] == env.work_config_user_name:
                        env.env_user_name = values[1]
                    line = file_obj.readline()
                # 首次运行初始化保存路径
                if len(env.paths) == 0:
                    for release in range(self.choi_relea.GetCount()):
                        paths = []
                        for _ in range(self.choi_srv.GetCount()):
                            paths.append("")
                        env.paths[self.choi_relea.GetString(release)] = paths
                # 设置当前选择版本和服务器的路径
                self.on_rel_srv_chosen()
                # 检查是否有新的版本（兼容旧数据）
                self.check_new_release()
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


def get_pro_msg(proj_path, maven_path):
    msg = '您的身份已识别为：“服务器大佬”'
    # jdk_ver = env.check_java(maven_path)
    if maven_path is not None:
        try:
            msg += env.check_maven(maven_path)
            # msg += '您的Maven路径是：' + maven_path + '，请确认\n'
            msg += '您选择的项目路径：' + proj_path + '\n'
            msg += '请确认所有文件已保存，确认完毕请点击“开始发布”'
            # 启用发布按钮
            wx.CallAfter(pub.sendMessage, "update_btn_start", enable=True)
        except FileNotFoundError:
            msg += '错误：选择的Maven路径不正确（只支持3.2.5版本）'
        except Exception as e:
            msg += e.args[0]
    else:
        msg += '提示：请选择Maven路径'
    return msg


# 检查多开
def check_multi_open():
    if not os.path.exists(env.work_path):
        os.mkdir(env.work_path)
    if os.path.exists(env.work_lock_path):
        try:
            os.remove(env.work_lock_path)
        except OSError as e:
            if e.errno == 13:
                wx.MessageBox('无法开启多个发布工具', '错误', wx.ICON_ERROR)
                wx.Exit()
    env.lock = os.open(env.work_lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)


def set_info():
    box=wx.TextEntryDialog(None, '请输入你的姓名全拼（例如：lijixue）', '信息补充（第一次运行时设置）', env.env_user_name)
    # 点击了ok
    if box.ShowModal() == wx.ID_OK:
        answer = box.GetValue()
        env.env_user_name = answer
        return True
    else:
        return False


if __name__ == "__main__":
    app = wx.App(False)
    frame = RunTool(None)
    frame.Show()
    # 开启程序
    app.MainLoop()
