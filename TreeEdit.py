#!/usr/bin/env python
import wx
import wx.lib.agw.aui as aui
import wx.dataview as dv

#Encapsulate the tree editing functionality
class TreeEdit(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, size=(-1,-1))
        self.treeId = wx.NewId()
        self.control = wx.TreeCtrl(self, self.treeId, size=(-1,-1))
        self.tree = self.control

        # Vertical box sizer for controls
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.control, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

        self.root = self.control.AddRoot("Project")
        self.Show(True)

    # Add a new item
    def onAddChild(self, event):
        focused = self.tree.GetFocusedItem()
        if focused.IsOk():
            self.tree.AppendItem(focused, 'New Item')
            self.tree.Expand(focused)
        elif self.tree.IsEmpty():
            self.tree.AddRoot("Project")
        self.__updateBold()

    # Delete an item and all children
    def onDelItem(self, event):
        focused = self.tree.GetFocusedItem()
        if focused.IsOk() and focused is not self.tree.GetRootItem():
            self.tree.Delete(focused)

    # Edit the title of an item
    def onEdit(self, event):
        self.tree.EditLabel(event.GetItem())

    # Moves node and all of its children to live under parent
    def __moveTree(self, node, parent):
        if not node.IsOk():
            return
        # Create the current node under the new parent
        newParent = self.tree.AppendItem(parent, self.tree.GetItemText(node), -1, -1, self.tree.GetItemData(node))

        if self.tree.ItemHasChildren(node):
            (itr, cookie) = self.tree.GetFirstChild(node)
            while True and itr.IsOk():
                self.__moveTree(itr, newParent)
                (itr, cookie) = self.tree.GetNextChild(node, cookie)
        self.tree.Delete(node)
        self.__updateBold()

    # Ensures that all children of the root node are bold
    def __updateBold(self):
        root = self.tree.GetRootItem()
        if not root.IsOk():
            return
        if self.tree.ItemHasChildren(root):
            (itr, cookie) = self.tree.GetFirstChild(root)
            while True and itr.IsOk():
                self.tree.SetItemBold(itr, True)
                (itr, cookie) = self.tree.GetNextChild(root, cookie)

    # Moves node and all children up one level
    def onUnindent(self, event):
        focused = self.tree.GetFocusedItem()
        if focused.IsOk() and focused is not self.tree.GetRootItem():
            theParent = self.tree.GetItemParent(focused)
            theParentParent = self.tree.GetItemParent(theParent)
            if theParentParent.IsOk():
                self.__moveTree(focused, theParentParent)

    # Moves node and all children under previous node
    def onIndent(self, event):
        focused = self.tree.GetFocusedItem()
        if focused.IsOk() and focused is not self.tree.GetRootItem():
            theSibling = self.tree.GetPrevSibling(focused)
            if theSibling.IsOk():
                self.__moveTree(focused, theSibling)
