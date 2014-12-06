from wx import *
import os
import subprocess


class GUIApp(App):
    def OnInit(self):
        self.program = Program()

        frame = GUIFrame(None, -1, "GUI", self.program)
        frame.Show(True)

        self.SetTopWindow(frame)

        return True


class GUIFrame(Frame):
    def __init__(self, parent, id, title, program):
        wx.Frame.__init__(self, parent, id, title)

        self.program = program

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.editor = wx.stc.StyledTextCtrl(self)
        self.button = Button(self, label="EXECUTE")
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


class Program:
    def __init__(self, filename = None):
        if(filename == None): filename = "test.txt"
        self.filename = os.path.join(os.path.expanduser("~"), filename)

    def save(self, text):
        file = open(self.filename, "w+")
        file.write(text)
        file.close()

    def run(self, text = None):
        if text != None: self.save(text)
        out = subprocess.check_output(["./interpreterMain-c", self.filename])
        return out.strip()


if __name__ == "__main__":
    app = GUIApp(0)
    app.MainLoop()