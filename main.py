#!/usr/bin/env python
import wx
import gettext
import lib.gui.MainFrame as MainFrame
import lib.edit.Requirement as Requirement


gettext.install('OpenHier')

app = wx.App(False)
frame = MainFrame.MainFrame(None, _('OpenHier'))
app.MainLoop()
