#!/usr/bin/env python
import wx
import wx.lib.agw.aui as aui
import wx.dataview as dv

#Encapsulate the tree editing functionality
class DetailEdit(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, size=(-1,-1))

        self.control = wx.Panel(self)
        # Vertical box sizer for controls
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.control, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
