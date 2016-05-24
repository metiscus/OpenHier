#!/usr/bin/env python
import wx
import wx.lib.agw.aui as aui
import wx.dataview as dv

#Encapsulate the tree editing functionality
class TreeEdit(wx.TreeCtrl):
    def __init__(self, main, parent, id, pos, size, style):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onEdit)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.onEditPost)
        self.main = main
        self.root = self.AddRoot("Project")
        self.Show(True)

    # Add a new item
    def onAddChild(self, event, id):
        focused = self.GetFocusedItem()
        if focused.IsOk():
            data = wx.TreeItemData()
            req = self.main.GetRequirement(id)
            data.SetData(id)
            self.AppendItem(focused, req.GetName(), data=data)
            (itr,cookie) = self.GetFirstChild(self.root)
            self.__update(itr, cookie)
            self.Expand(focused)
        elif self.IsEmpty():
            self.AddRoot("Project")
        self.__updateBold()

    # Delete an item and all children
    def onDelItem(self, event):
        focused = self.GetFocusedItem()
        if focused.IsOk() and focused is not self.GetRootItem():
            self.Delete(focused)

    # Edit the title of an item
    def onEdit(self, event):
        self.EditLabel(event.GetItem())

    def onEditPost(self, event):
        data = self.GetItemData(event.GetItem())
        if data:
            req_id = data.GetData()
            self.main.GetRequirement(req_id).SetName(event.GetLabel())

    def __update(self, itr, cookie):
        if not itr.IsOk():
            return
        data = self.GetItemData(itr)
        if data:
            req = self.main.GetRequirement(data.GetData())
            self.SetItemText(itr, req.GetName())
        while(itr.IsOk()):
            (itr, cookie) = self.GetNextChild(self.root, cookie)
            self.__update(itr, cookie)


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
        self.Delete(node)
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
