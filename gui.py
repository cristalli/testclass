from distutils.command.build import build
import sys
import threading
import time

import wx


class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, title=args[0], size=(800, 600))
        self.initialize(parent, *args, **kwargs)

    def initialize(self, parent, *args, **kwargs) -> None:
        self.CreateStatusBar()
        self.root_panel = RootPanel(self)


class RootPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, wx.ID_ANY)
        self.initialize()

    def initialize(self) -> None:

        # 個別パネル作成
        self.image_panel = ImagePanel(self)
        self.button_panel = ButtonPanel(self)
        self.sever_control_panel = ServerControlPanel(self)
        self.log_panel = LogPanel(self)
        self.file_select_panel = FileSelectPanel(self)
        self.generic_dir_panel = GenericDirCtrlPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.button_panel, 1, wx.ALL | wx.GROW, 2)
        sizer.Add(self.sever_control_panel, 1, wx.ALL | wx.GROW, 2)
        sizer.Add(self.file_select_panel, 1, wx.ALL | wx.GROW, 2)
        sizer.Add(self.image_panel, 5, wx.ALL | wx.GROW, 2)
        sizer.Add(self.log_panel, 5, wx.ALL | wx.GROW, 2)

        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_left.Add(self.generic_dir_panel, 1, wx.ALL | wx.GROW, 2)

        sizer_total = wx.BoxSizer(wx.HORIZONTAL)
        sizer_total.Add(sizer_left, 1, wx.GROW)
        sizer_total.Add(sizer, 2, wx.GROW)

        self.SetSizer(sizer_total)


class GenericDirCtrlPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent, wx.ID_ANY)
        self.initialize()

    def initialize(self) -> None:
        self.dir_ctrl = wx.GenericDirCtrl(self,wx.ID_ANY)
        button = wx.Button(self, wx.ID_ANY, "LOAD")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dir_ctrl, 10, flag=wx.GROW)
        sizer.Add(button, 1, flag=wx.GROW)
        self.SetSizer(sizer)

        button.Bind(wx.EVT_BUTTON, self.click_button)

    def click_button(self, event):
        frame.root_panel.image_panel.set_image(self.dir_ctrl.GetFilePath())

class ServerControlPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent, wx.ID_ANY)
        self.initialize()

    def initialize(self) -> None:
        button_1 = wx.Button(self, wx.ID_ANY, "設定１")
        button_2 = wx.Button(self, wx.ID_ANY, "設定２")
        button_3 = wx.Button(self, wx.ID_ANY, "設定３")
        text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "ID")
        sizer = wx.BoxSizer()

        sizer.Add(button_1, 1, flag=wx.GROW)
        sizer.Add(button_2, 1, flag=wx.GROW)
        sizer.Add(button_3, 1, flag=wx.GROW)
        sizer.Add(text_ctrl, 1, flag=wx.GROW)

        self.SetSizer(sizer)

        button_1.SetToolTip("サーバーの接続設定をします")
        button_1.Bind(wx.EVT_BUTTON, self.click_button_1)

    def click_button_1(self, event):

        self.dialog = ServerDialog(self, wx.ID_ANY, "")
        self.dialog.ShowModal()
        self.dialog.Destroy()


class FileSelectPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.initialize()

    def initialize(self) -> None:

        self.button = wx.Button(self, wx.ID_ANY, "ファイル")
        style = wx.TE_MULTILINE | wx.TE_READONLY
        self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY, style=style)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.button, 1, flag=wx.GROW)
        sizer.Add(self.text_ctrl, 5, flag=wx.GROW)

        self.SetSizer(sizer)

        self.button.Bind(wx.EVT_BUTTON, self.OnBrowse)

    def OnBrowse(self, event):
        with wx.FileDialog(
            self,
            "Select Image File",
            wildcard="PNG files (*.jpg)|*.jpg",
            style=wx.FD_OPEN,
        ) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.text_ctrl.SetValue(dialog.GetPaths()[0])
                self.Layout()


class ImagePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.initialize()

    def initialize(self) -> None:

        self.image = None
        self.static_bitmap = wx.StaticBitmap(self, wx.ID_ANY)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.static_bitmap, 1, wx.EXPAND, 0)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_SIZE, self.OnSize)

    def set_image(self, image_name) -> None:

        self.image = wx.Image(image_name)
        self.bitmap = wx.Image.ConvertToBitmap(self.image)

        self.static_bitmap.SetBitmap(self.bitmap)
        self.ScaleToFit()

    def OnSize(self, event):
        if self.image:
            self.ScaleToFit()
            event.Skip()

    def ScaleToFit(self) -> None:
        if self.image:

            aspect = self.image.GetSize()[1] / self.image.GetSize()[0]
            cw, ch = self.GetSize()
            nw = cw
            nh = int(nw * aspect)
            if nh > ch:
                nh = ch
                nw = int(nh / aspect)
            nh = int(nh)
            nw = int(nw)

            if nh > 0 and nw > 0:
                image = self.image.Scale(nw, nh, quality=wx.IMAGE_QUALITY_HIGH)
                self.static_bitmap.SetBitmap(image.ConvertToBitmap())
                self.Layout()


class ButtonPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent, wx.ID_ANY)
        self.initialize()

    def initialize(self) -> None:
        button_1 = wx.Button(self, wx.ID_ANY, "A")
        button_2 = wx.Button(self, wx.ID_ANY, "AAAA")
        button_3 = wx.Button(self, wx.ID_ANY, "画像セット")
        button_4 = wx.Button(self, wx.ID_ANY, "D")

        sizer = wx.BoxSizer()
        sizer.Add(button_1, 1, flag=wx.GROW)
        sizer.Add(button_2, 1, flag=wx.GROW)
        sizer.Add(button_3, 1, flag=wx.GROW)
        sizer.Add(button_4, 1, flag=wx.GROW)

        self.SetSizer(sizer)

        button_1.SetToolTip("32コアで計算実施")
        button_1.Bind(wx.EVT_BUTTON, self.click_button_1)

        button_2.Bind(wx.EVT_BUTTON, self.click_button_2)
        button_3.Bind(wx.EVT_BUTTON, self.click_button_3)

    def click_button_1(self, event):
        frame.root_panel.image_panel.set_image("IMG_2016.jpg")
        frame.SetStatusText("ここがステータスバー")
        print(frame.root_panel.image_panel)

    def click_button_2(self, event):
        t1 = threading.Thread(target=self.calculation1)
        t1.start()

        t2 = threading.Thread(target=self.calculation2)
        t2.start()

    def click_button_3(self, event):
        frame.root_panel.image_panel.set_image("IMG_1932.jpg")

    def calculation1(self):
        time.sleep(1)
        print("cal-01 START")
        time.sleep(10)
        print("cal-01 END")
        wx.CallAfter(self.ending)

    def calculation2(self):
        time.sleep(2)
        print("cal-02 START")
        time.sleep(5)
        print("cal-02 END")
        wx.CallAfter(self.ending)

    def ending(self):
        print("Ending!!")


class LogPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.initialize()

    def initialize(self) -> None:

        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY, style=style)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.text_ctrl, 1, wx.GROW)

        sys.stdout = self.text_ctrl

        self.SetSizer(sizer)


class ServerDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwds):

        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, parent, *args, **kwds)

        self.SetTitle("サーバ設定")

        self.hostname = wx.StaticText(
            self, wx.ID_ANY, "HOSTNAME", style=wx.TE_CENTER
        )
        self.username = wx.StaticText(
            self, wx.ID_ANY, "USERNAME", style=wx.TE_CENTER
        )
        self.password = wx.StaticText(
            self, wx.ID_ANY, "PASSWORD", style=wx.TE_CENTER
        )

        self.hostname.BackgroundColour = "yellow"

        self.hostname1 = wx.TextCtrl(self, wx.ID_ANY, "aaa.bbb.ccc.ddd")
        self.username1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.password1 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PASSWORD)

        self.hostname2 = wx.TextCtrl(self, wx.ID_ANY, "eee.rrr.www.rrr")
        self.username2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.password2 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PASSWORD)

        self.ok_button = wx.Button(self, wx.ID_OK, "OK")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "CANCEL")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(3, 2, 0)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        sizer_2.Add(
            self.hostname, 1, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10
        )
        sizer_2.Add(
            self.username, 1, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10
        )
        sizer_2.Add(
            self.password, 1, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10
        )

        sizer_2.Add(self.hostname1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        sizer_2.Add(self.username1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        sizer_2.Add(self.password1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        sizer_2.Add(self.hostname2, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        sizer_2.Add(self.username2, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        sizer_2.Add(self.password2, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        sizer_3.Add(self.ok_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        sizer_3.Add(
            self.cancel_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10
        )

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.Layout()


app = wx.App(False)
frame = MainFrame(None, "auto gui")
frame.Show(True)
app.MainLoop()
