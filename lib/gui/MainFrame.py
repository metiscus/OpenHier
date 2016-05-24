#!/usr/bin/env python
import wx
import wx.lib.agw.aui as aui
import wx.dataview as dv
import TreeEdit
import DetailEdit

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(-1,-1))
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(100)
        self.tree_id = wx.NewId()
        self.tree = TreeEdit.TreeEdit(splitter, self.tree_id, wx.DefaultPosition,wx.DefaultSize,wx.TR_HAS_BUTTONS)
        self.details = DetailEdit.DetailEdit(splitter)
        splitter.SplitVertically(self.tree, self.details)
        self.control = splitter

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, "&About", "About this program")
        filemenu.Append(wx.ID_EXIT, "E&xit", "Exit the program");

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")

        self.SetMenuBar(menubar)

        idAddChild = wx.NewId()
        idDelItem = wx.NewId()
        idUnindent  = wx.NewId()
        idIndent  = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onAddChild, id=idAddChild)
        self.Bind(wx.EVT_MENU, self.onDelItem, id=idDelItem)
        self.Bind(wx.EVT_MENU, self.onUnindent, id=idUnindent)
        self.Bind(wx.EVT_MENU, self.onIndent, id=idIndent)
        #self.tree.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onEdit, id=1)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL,  ord('N'), idAddChild ),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, idDelItem ),
            (wx.ACCEL_SHIFT, wx.WXK_TAB, idUnindent ),
            (wx.ACCEL_NORMAL, wx.WXK_TAB, idIndent ),
        ])
        self.SetAcceleratorTable(accel_tbl)
        self.Show(True)

    def onAddChild(self, event):
        self.tree.onAddChild(event)
    def onDelItem(self, event):
        self.tree.onDelItem(event)
    def onEdit(self, event):
        self.tree.onEdit(event)
    def onUnindent(self, event):
        self.tree.onUnindent(event)
    def onIndent(self, event):
        self.tree.onIndent(event)
