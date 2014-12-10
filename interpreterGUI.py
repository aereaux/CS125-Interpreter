from wx import *
import os
import subprocess


class GUIApp(App):
    def OnInit(self):

        frame = GUIFrame(None, -1, "ASMGUI")
        frame.Show(True)

        self.SetTopWindow(frame)

        return True


class GUIFrame(Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        program = Program()
        self.program = program

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        newMenuItem = fileMenu.Append(wx.NewId(), "New", "Create a new program")
        openMenuItem = fileMenu.Append(wx.NewId(), "Open", "Open a program")
        saveMenuItem = fileMenu.Append(wx.NewId(), "Save", "Save the program")
        saveAsMenuItem = fileMenu.Append(wx.NewId(), "Save As", "Save to a different file")
        exitMenuItem = fileMenu.Append(wx.NewId(), "Exit", "Exit the application")

        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnSaveAsMenu, saveAsMenuItem)
        self.Bind(wx.EVT_MENU, self.OnNewMenu, newMenuItem)
        self.Bind(wx.EVT_MENU, self.OnOpenMenu, openMenuItem)
        self.Bind(wx.EVT_MENU, self.OnSaveMenu, saveMenuItem)
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, exitMenuItem)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.editor = wx.stc.StyledTextCtrl(self)
        self.button = Button(self, label="Save and Run")
        self.clearButton = Button(self, label="Clear")
        self.output = wx.stc.StyledTextCtrl(self, style=wx.TE_READONLY)

        font = wx.Font(9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        face = font.GetFaceName()
        size = font.GetPointSize()
        self.output.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,"face:%s,size:%d" % (face, size))

        self.clearButton.Bind(wx.EVT_BUTTON, self.OnClearButton)
        self.button.Bind(wx.EVT_BUTTON, self.OnButtonPress)

        brSizer = BoxSizer(VERTICAL)
        brSizer.Add(self.button, 1)
        brSizer.Add(self.clearButton, 1)

        botSizer = BoxSizer(HORIZONTAL)
        botSizer.Add(self.output, 1, flag=wx.EXPAND)
        botSizer.Add(brSizer, flag=wx.EXPAND)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(self.editor, 1, flag=EXPAND)
        sizer.Add(botSizer, 1, flag=EXPAND)
        self.SetSizer(sizer)


    def OnCloseWindow(self, event):
        self.Destroy()


    def OnButtonPress(self, event):
        out = self.program.run(self.editor.GetText())
        self.output.ChangeValue(out)

    def OnOpenMenu(self, event):
        dlg = wx.FileDialog(self, style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()

        self.program = Program(path)
        self.editor.SetText(self.program.read())

    def OnSaveMenu(self, event):
        if self.program.filename.endswith(".swap"): self.OnSaveAsMenu(event)
        else: self.program.save(self.editor.GetText())

    def OnNewMenu(self, event):
        self.program = Program()
        self.editor.SetText("")

    def OnSaveAsMenu(self, event):
        dlg = wx.FileDialog(self, style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()

        self.program = Program(path)
        self.program.save(self.editor.GetText())

    def OnClearButton(self, event):
        self.output.ClearAll()


class Program:
    def __init__(self, filename=None):
        if filename is None: filename = ".swap"
        self.filename = os.path.join(os.curdir, filename)

    def save(self, text):
        file = open(self.filename, "w")
        file.write(text)
        file.close()

    def run(self, text = None):
        if text is not None: self.save(text)
        out = subprocess.check_output(['python2', 'interpreterMain.py', self.filename])
        return out

    def read(self):
        file = open(self.filename, "r")
        text = file.read()
        file.close()
        return text


if __name__ == "__main__":
    app = GUIApp(0)
    app.MainLoop()