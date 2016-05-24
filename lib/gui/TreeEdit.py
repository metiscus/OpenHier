#!/usr/bin/env python
import wx
import wx.lib.agw.aui as aui
import wx.dataview as dv

#Encapsulate the tree editing functionality
class TreeEdit(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onEdit)

        # Vertical box sizer for controls
        #box = wx.BoxSizer(wx.VERTICAL)
        #box.Add(self.control, 1, wx.EXPAND)
        #self.SetAutoLayout(True)
        #self.SetSizer(box)
        #self.Layout()

        self.root = self.AddRoot("Project")
        self.Show(True)

    # Add a new item
    def onAddChild(self, event):
        focused = self.GetFocusedItem()
        if focused.IsOk():
            self.AppendItem(focused, 'New Item')
            self.Expand(focused)
        elif self.IsEmpty():
            self.AddRoot("Project")
        self.__updateBold()

    # Delete an item and all children
    def onDelItem(self, event):
        focused = self.GetFocusedItem()
        if focused.IsOk() and focused is not self.GetRootItem():
            self.tree.Delete(focused)

    # Edit the title of an item
    def onEdit(self, event):
        self.EditLabel(event.GetItem())

    # Moves node and all of its children to live under parent
    def __moveTree(self, node, parent):
        if not node.IsOk():
            return
        # Create the current node under the new parent
        newParent = self.AppendItem(parent, self.GetItemText(node), -1, -1, self.GetItemData(node))

        if self.ItemHasChildren(node):
            (itr, cookie) = self.GetFirstChild(node)
            while True and itr.IsOk():
                self.__moveTree(itr, newParent)
                (itr, cookie) = self.GetNextChild(node, cookie)
        self.tree.Delete(node)
        self.__updateBold()

    # Ensures that all children of the root node are bold
    def __updateBold(self):
        root = self.GetRootItem()
        if not root.IsOk():
            return
        if self.ItemHasChildren(root):
            (itr, cookie) = self.GetFirstChild(root)
            while True and itr.IsOk():
                self.SetItemBold(itr, True)
                (itr, cookie) = self.GetNextChild(root, cookie)

    # Moves node and all children up one level
    def onUnindent(self, event):
        focused = self.GetFocusedItem()
        if focused.IsOk() and focused is not self.GetRootItem():
            theParent = self.GetItemParent(focused)
            theParentParent = self.GetItemParent(theParent)
            if theParentParent.IsOk():
                self.__moveTree(focused, theParentParent)

    # Moves node and all children under previous node
    def onIndent(self, event):
        focused = self.GetFocusedItem()
        if focused.IsOk() and focused is not self.GetRootItem():
            theSibling = self.GetPrevSibling(focused)
            if theSibling.IsOk():
                self.__moveTree(focused, theSibling)
