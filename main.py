#!/usr/bin/env python
import wx
import MainFrame

app = wx.App(False)
frame = MainFrame.MainFrame(None, "Hello World")
app.MainLoop()
