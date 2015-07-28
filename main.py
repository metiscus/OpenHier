#!/usr/bin/env python
import wx
import MainFrame
import gettext

gettext.install('OpenHier')

app = wx.App(False)
frame = MainFrame.MainFrame(None, _('OpenHier'))
app.MainLoop()
