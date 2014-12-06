from wx import *
import os
import subprocess


class GUIApp(App):
    def OnInit(self):
        frame = GUIFrame(None, -1, "GUI")
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
        openMenuItem = fileMenu.Append(wx.NewId(), "Open", "Open a program")
        saveMenuItem = fileMenu.Append(wx.NewId(), "Save", "Save the program")
        exitMenuItem = fileMenu.Append(wx.NewId(), "Exit", "Exit the application")

        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpenMenu, openMenuItem)
        self.Bind(wx.EVT_MENU, self.OnSaveMenu, saveMenuItem)
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, exitMenuItem)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.editor = wx.stc.StyledTextCtrl(self)
        self.button = Button(self, label="Save and Run")
        self.output = TextCtrl(self, style=wx.TE_READONLY)

        self.button.Bind(wx.EVT_BUTTON, self.OnButtonPress)

        botSizer = BoxSizer(HORIZONTAL)
        botSizer.Add(self.output, 1)
        botSizer.Add(self.button)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(self.editor, 1, flag=EXPAND)
        sizer.Add(botSizer, flag=EXPAND)
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
        self.program.save(self.editor.GetText())


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
        out = subprocess.check_output(["./interpreterMain-c", self.filename])
        return out.strip()

    def read(self):
        file = open(self.filename, "r")
        text = file.read()
        file.close()
        return text


if __name__ == "__main__":
    app = GUIApp(0)
    app.MainLoop()