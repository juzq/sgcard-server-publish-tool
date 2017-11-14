# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class PublishTool
###########################################################################

class PublishTool ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"苍龙服务器发布工具", pos = wx.DefaultPosition, size = wx.Size( 551,417 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self.menu_bar = wx.MenuBar( 0 )
		self.menu_chio = wx.Menu()
		self.menu_item_hist = wx.MenuItem( self.menu_chio, wx.ID_ANY, u"更新历史(H)", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_chio.AppendItem( self.menu_item_hist )
		
		self.menu_bar.Append( self.menu_chio, u"选项(S)" ) 
		
		self.menu_abt = wx.Menu()
		self.menu_item_abt = wx.MenuItem( self.menu_abt, wx.ID_ANY, u"关于(A)", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_abt.AppendItem( self.menu_item_abt )
		
		self.menu_bar.Append( self.menu_abt, u"帮助(H)" ) 
		
		self.SetMenuBar( self.menu_bar )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"苍龙服务器发布工具", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer5 = wx.FlexGridSizer( 0, 2, 5, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"版本选择：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer5.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		choi_releaChoices = [ u"测试", u"日文", u"韩文", u"台湾", u"东南亚" ]
		self.choi_relea = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 180,-1 ), choi_releaChoices, 0 )
		self.choi_relea.SetSelection( 0 )
		fgSizer5.Add( self.choi_relea, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		fgSizer4.Add( fgSizer5, 1, wx.EXPAND, 5 )
		
		fgSizer6 = wx.FlexGridSizer( 0, 2, 5, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"服务器选择：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer6.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		choi_srvChoices = [ u"游戏服", u"游戏2服", u"战斗服", u"列表服" ]
		self.choi_srv = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 180,-1 ), choi_srvChoices, 0 )
		self.choi_srv.SetSelection( 0 )
		fgSizer6.Add( self.choi_srv, 0, wx.ALL, 5 )
		
		
		fgSizer4.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( fgSizer4, 0, 0, 5 )
		
		fgSizer37 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer37.SetFlexibleDirection( wx.BOTH )
		fgSizer37.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"文 件 夹：", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer37.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.dir_picker = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( 450,-1 ), wx.DIRP_DEFAULT_STYLE|wx.DIRP_SMALL )
		fgSizer37.Add( self.dir_picker, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( fgSizer37, 0, wx.EXPAND, 5 )
		
		fgSizer38 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer38.SetFlexibleDirection( wx.BOTH )
		fgSizer38.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer39 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer39.SetFlexibleDirection( wx.BOTH )
		fgSizer39.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer39.SetMinSize( wx.Size( 260,-1 ) ) 
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"状    态：", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer39.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_status = wx.StaticText( self, wx.ID_ANY, u"未开始", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.text_status.Wrap( -1 )
		fgSizer39.Add( self.text_status, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer38.Add( fgSizer39, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer41 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer41.SetFlexibleDirection( wx.BOTH )
		fgSizer41.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.btn_start = wx.Button( self, wx.ID_ANY, u"开始发布", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		fgSizer41.Add( self.btn_start, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer38.Add( fgSizer41, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( fgSizer38, 0, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"发布文件" ), wx.VERTICAL )
		
		self.text_files = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		sbSizer2.Add( self.text_files, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer2.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"发布结果" ), wx.VERTICAL )
		
		self.text_result = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		sbSizer4.Add( self.text_result, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer2.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.dir_picker.Bind( wx.EVT_DIRPICKER_CHANGED, self.dir_changed )
		self.btn_start.Bind( wx.EVT_BUTTON, self.start )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def dir_changed( self, event ):
		event.Skip()
	
	def start( self, event ):
		event.Skip()
	
