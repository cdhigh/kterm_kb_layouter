#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#Kterm键盘可视化设计器，不依赖任何第三方库，Python>=3.8
#Author: cdhigh <https://github.com/cdhigh>
import os, sys, json, copy
from functools import partial
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
#Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
from tkinter.messagebox import *
from tkinter import filedialog  #.askopenfilename()
from tkinter import simpledialog  #.askstring()

__Version__ = 'v1.0'

ESC = {'image': 'esc', 'action': 'escape'}
BK = lambda w: {'display': '←', 'action': 'backspace', 'width': w * 100} #'image': 'back'
TAB = lambda w: {'display': '⇥', 'action': 'tab', 'width': w * 100} #'image': 'tab'
CAPSLK = lambda w: {'display': '⇪', 'action': 'modifier:caps', 'width': w * 100} #'image': 'capslk'
SHIFT = lambda w: {'display': '⇧', 'action': 'modifier:shift', 'width': w * 100} #'image': 'shift'
A15 = lambda a: {'display': a, 'width': 1500}
A30 = lambda a: {'display': a, 'width': 3000}
MOD1 = {'display': '⇄', 'action': 'modifier:mod1'} #'image': 'sym1'
MOD2 = {'display': '↭', 'action': 'modifier:mod2'} #'image': 'sym2'
CTRL = lambda w: {'image': 'ctrl', 'action': 'modifier:ctrl', 'width': w * 100}
ALT = {'image': 'alt', 'action': 'modifier:alt'}
SPACE = lambda w: {'display': ' ', 'action': 'space', 'width': w * 100}
ENTER = lambda w: {'display': '⤶', 'action': 'return', 'width': w * 100} #'image': 'return'
UP = {'display': '▲', 'action': 'up'} #'image': 'up'
DOWN = {'display': '▼', 'action': 'down'} #'image': 'down'
LEFT = {'display': '◀', 'action': 'left'} #'image': 'left'
RIGHT = {'display': '▶', 'action': 'right'} #'image': 'right'
F = lambda n: {'image': f'f{n}', 'action': f'f{n}'}
HOME = {'image': 'home', 'action': 'home'}
END = {'image': 'end', 'action': 'end'}
PGUP = {'display': '⤉', 'action': 'pageup'} #'image': 'pgup'
PGDOWN = {'display': '⤈', 'action': 'pagedown'} #'image': 'pgdn'
DEL = {'display': '␡', 'action': 'delete'} #'image': 'del'

#所有支持的action按键信息
ACTION_LIST = [ESC, BK(10), TAB(10), CAPSLK(10), SHIFT(10), MOD1, MOD2, CTRL(10), ALT, SPACE(10), 
    ENTER(10), UP, DOWN, LEFT, RIGHT, HOME, END, PGUP, PGDOWN]

#几个预置的布局
#新增布局时注意每一行的按键宽度总和必须是1000的倍数
PROFILE_5R11C = {
    '_meta': {'default_width': 2000},
    'normal': [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', BK(30)],
        [A30('q'), 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '"'],
        [CAPSLK(20), 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', A30('ç')],
        [SHIFT(30), 'z', 'x', 'c', 'v', 'b', 'n', 'm', '!', '?', '-'],
        [MOD1, CTRL(20), '/', SPACE(80), MOD2, ',', '.', ENTER(30)],
    ],
    'caps': [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', BK(30)],
        [A30('Q'), 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', UP],
        [CAPSLK(20), 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', A30('Ç')],
        [SHIFT(30), 'Z', 'X', 'C', 'V', 'B', 'N', 'M', LEFT, RIGHT, DOWN],
        [MOD1, CTRL(20), '/', SPACE(80), MOD2, ';', "'", ENTER(30)],
    ],
    'mod1': [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', BK(30)],
        [A30('!'), '@', '#', '$', '%', '^', '&', '*', '(', ')', ';'],
        [CAPSLK(20), 'á', 'â', 'ã', 'à', 'é', 'ê', 'í', 'ó', 'ô', A30('õ')],
        [SHIFT(30), 'ú', '[', ']', '=', '+', '-', '_', '*', ':', '?'],
        [MOD1, CTRL(20), '\\', SPACE(80), MOD2, '/', "|", ENTER(30)],
    ],
    'mod2': [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', BK(20)],
        [A30('~'), '@', '#', '$', '%', '^', '&', '*', '(', ')', ':'],
        [CAPSLK(20), 'Á', 'Â', 'Ã', 'À', 'É', 'Ê', 'Í', 'Ó', 'Ô', A30('Õ')],
        [SHIFT(30), 'Ú', '{', '}', '/', ';', '`', '+', '-', ',', '.'],
        [MOD1, CTRL(20), '\\', SPACE(80), MOD2, '<', ">", ENTER(30)],
    ],
}

#防Kindle原生键盘
PROFILE_4R10C = {
    '_meta': {'default_width': 1000},
    'normal': [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        [A15('a'), 's', 'd', 'f', 'g', 'h', 'j', 'k', A15('l')],
        [CAPSLK(10), 'z', 'x', 'c', 'v', 'b', 'n', 'm', SHIFT(10), BK(10)],
        [MOD1, MOD2, SPACE(30), ';', ',', '.', ENTER(20)],
    ],
    'caps': [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        [A15('A'), 'S', 'D', 'F', 'G', 'H', 'J', 'K', A15('L')],
        [CAPSLK(10), 'Z', 'X', 'C', 'V', 'B', 'N', 'M', SHIFT(10), BK(10)],
        [MOD1, MOD2, SPACE(30), ';', ',', '.', ENTER(20)],
    ],
    'mod1': [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        [A15('$'), '&', '(', ')', '"', "'", '-', '+', A15('/')],
        [CAPSLK(10), '@', '!', '?', ':', ';', ',', '#', SHIFT(10), BK(10)],
        [MOD1, MOD2, SPACE(30), '_', ',', '.', ENTER(20)],
    ],
    'mod2': [
        [ESC, '%', '~', '^', '[', ']', '{', '}', '|', '\\'],
        [TAB(15), '`', '#', '<', '>', '-', '_', '*', A15('=')],
        [CAPSLK(10), '"', LEFT, RIGHT, UP, DOWN, PGUP, PGDOWN, SHIFT(10), BK(10)],
        [MOD1, MOD2, SPACE(30), ';', ',', '.', ENTER(20)],
    ],
}

#Kterm自带的布局
PROFILE_KERM = {
    '_meta': {'default_width': 1000},
    'normal': [
        [ESC, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', BK(20)],
        [TAB(20), 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
        [CAPSLK(20), 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", ENTER(20)],
        [SHIFT(20), '`', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', UP, SHIFT(10)],
        [CTRL(20), ALT, MOD1, SPACE(70), MOD2, LEFT, DOWN, RIGHT],
    ],
    'caps': [
        [ESC, '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', BK(20)],
        [TAB(20), 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
        [CAPSLK(20), 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', ENTER(20)],
        [SHIFT(20), '~', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', UP, SHIFT(10)],
        [CTRL(20), ALT, MOD1, SPACE(70), MOD2, LEFT, DOWN, RIGHT],
    ],
    'mod1': [
        [ESC, F(1), F(2), F(3), F(4), F(5), F(6), F(7), F(8), F(9), F(10), F(11), F(12), BK(20)],
        [TAB(20), 'à', 'á', 'ą', 'â', 'ä', 'å', 'ć', 'ç', 'è', 'é', 'ę', 'ë', '\\'],
        [CAPSLK(20), 'ì', 'í', 'î', 'ł', 'ñ', 'ń', 'ó', 'ò', 'ø', 'ö', 'ś', ENTER(20)],
        [SHIFT(20), '`', 'ß', 'ù', 'ú', 'û', 'ü', 'ý', 'ÿ', 'ż', 'ź', '/', PGUP, SHIFT(10)],
        [CTRL(20), ALT, MOD1, SPACE(70), MOD2, HOME, PGDOWN, END],
    ],
    'mod2': [
        [ESC, '¹', '²', '€', '£', '¥', '¢', '¡', '¿', '¶', '§', 'µ', '°', BK(20)],
        [TAB(20), 'À', 'Á', 'Ą', 'Â', 'Ä', 'Å', 'Ć', 'Ç', 'È', 'É', 'Ę', 'Ë', '\\'],
        [CAPSLK(20), 'Ì', 'Í', 'Î', 'Ł', 'Ñ', 'Ń', 'Ó', 'Ò', 'Ø', 'Ö', "Ś", ENTER(20)],
        [SHIFT(20), '`', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', '«', '»', 'Ż', 'Ź', '/', UP, SHIFT(10)],
        [CTRL(20), ALT, MOD1, SPACE(70), MOD2, LEFT, DOWN, RIGHT],
    ],
}

BUILTIN_PROFILES = {'5R11C': PROFILE_5R11C, '4R10C': PROFILE_4R10C, 'Kterm': PROFILE_KERM}

#为了避免额外依赖，不使用PIL和图像文件，使用一些UNICODE符号代替图像
PNG_UNICODE_MAP = {
    ' ': '␣',
    'left.png': '◀',
    'right.png': '▶',
    'up.png': '▲',
    'down.png': '▼',
    'pgup.png': '⏫',
    'pgdn.png': '⏬',
    'home.png': 'Hom',
    'end.png': 'End',
    'return.png': '⤶',
    'shift.png': '⇧',
    'capslk.png': '⇪',
    'tab.png': '⇥',
    'esc.png': 'Esc',
    'ctrl.png': 'Ctl',
    'alt.png': 'Alt',
    'sym1.png': '⇄',
    'sym2.png': '⎌',
    'del.png': 'Del',
    'back.png': '⬅',
    'f1.png': 'F1',
    'f2.png': 'F2',
    'f3.png': 'F3',
    'f4.png': 'F4',
    'f5.png': 'F5',
    'f6.png': 'F6',
    'f7.png': 'F7',
    'f8.png': 'F8',
    'f9.png': 'F9',
    'f10.png': 'F10',
    'f11.png': 'F11',
    'f12.png': 'F12',
}

appDir = os.path.dirname(os.path.abspath(__file__))
PROFILES_JSON = os.path.join(appDir, 'profiles.json')

#在python3.9之前的版本用来格式化xml
#使用方法：
#prettifyXml(root)
#ET.ElementTree(root).write('pretty.xml', encoding='utf-8', xml_declaration=True)
def prettifyXml(current, parent=None, index=-1, depth=0, indent='  '):
    for i, node in enumerate(current):
        prettifyXml(node, current, i, depth + 1, indent)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + (indent * depth)
        else:
            parent[index - 1].tail = '\n' + (indent * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + (indent * (depth - 1))

#界面使用作者自己的工具 vb6tkinter <https://github.com/cdhigh/vb6tkinter> 自动生成
class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master):
        super().__init__(master)
        self.master.title('Kterm Keyboard Layouter')
        self.master.geometry('921x534')
        self.icondata = """
            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
            ==="""
        self.iconimg = PhotoImage(data=self.icondata)
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.iconimg)
        self.master.protocol('WM_DELETE_WINDOW', self.EV_WM_DELETE_WINDOW)
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.cmdDeleteProfileVar = StringVar(value='Delete Profile')
        self.style.configure('TcmdDeleteProfile.TButton', font=('Arial',14))
        self.cmdDeleteProfile = Button(self.top, text='Delete Profile', textvariable=self.cmdDeleteProfileVar, command=self.cmdDeleteProfile_Cmd, style='TcmdDeleteProfile.TButton')
        self.cmdDeleteProfile.setText = lambda x: self.cmdDeleteProfileVar.set(x)
        self.cmdDeleteProfile.text = lambda : self.cmdDeleteProfileVar.get()
        self.cmdDeleteProfile.place(relx=0.591, rely=0.03, relwidth=0.183, relheight=0.062)

        self.topRadioVar = StringVar()
        self.style.configure('ToptMod2.TRadiobutton', font=('Arial',12))
        self.optMod2 = Radiobutton(self.top, text='Mod2', value='optMod2', variable=self.topRadioVar, command=self.optMod2_Cmd, style='ToptMod2.TRadiobutton')
        self.optMod2.setValue = lambda x: self.topRadioVar.set('optMod2' if x else '')
        self.optMod2.value = lambda : 1 if self.topRadioVar.get() == 'optMod2' else 0
        self.optMod2.place(relx=0.452, rely=0.135, relwidth=0.131, relheight=0.062)

        self.style.configure('ToptMod1.TRadiobutton', font=('Arial',12))
        self.optMod1 = Radiobutton(self.top, text='Mod1', value='optMod1', variable=self.topRadioVar, command=self.optMod1_Cmd, style='ToptMod1.TRadiobutton')
        self.optMod1.setValue = lambda x: self.topRadioVar.set('optMod1' if x else '')
        self.optMod1.value = lambda : 1 if self.topRadioVar.get() == 'optMod1' else 0
        self.optMod1.place(relx=0.307, rely=0.135, relwidth=0.131, relheight=0.062)

        self.style.configure('ToptCaps.TRadiobutton', font=('Arial',12))
        self.optCaps = Radiobutton(self.top, text='Caps', value='optCaps', variable=self.topRadioVar, command=self.optCaps_Cmd, style='ToptCaps.TRadiobutton')
        self.optCaps.setValue = lambda x: self.topRadioVar.set('optCaps' if x else '')
        self.optCaps.value = lambda : 1 if self.topRadioVar.get() == 'optCaps' else 0
        self.optCaps.place(relx=0.162, rely=0.135, relwidth=0.131, relheight=0.062)

        self.style.configure('ToptNormal.TRadiobutton', font=('Arial',12))
        self.optNormal = Radiobutton(self.top, text='Normal', value='optNormal', variable=self.topRadioVar, command=self.optNormal_Cmd, style='ToptNormal.TRadiobutton')
        self.optNormal.setValue = lambda x: self.topRadioVar.set('optNormal' if x else '')
        self.optNormal.value = lambda : 1 if self.topRadioVar.get() == 'optNormal' else 0
        self.optNormal.setValue(1)
        self.optNormal.place(relx=0.017, rely=0.135, relwidth=0.131, relheight=0.062)

        self.cmdSaveXmlVar = StringVar(value='Save Xml')
        self.style.configure('TcmdSaveXml.TButton', font=('Arial',14))
        self.cmdSaveXml = Button(self.top, text='Save Xml', textvariable=self.cmdSaveXmlVar, command=self.cmdSaveXml_Cmd, style='TcmdSaveXml.TButton')
        self.cmdSaveXml.setText = lambda x: self.cmdSaveXmlVar.set(x)
        self.cmdSaveXml.text = lambda : self.cmdSaveXmlVar.get()
        self.cmdSaveXml.place(relx=0.808, rely=0.03, relwidth=0.183, relheight=0.062)

        self.cmdSaveProfileVar = StringVar(value='Save Profile')
        self.style.configure('TcmdSaveProfile.TButton', font=('Arial',14))
        self.cmdSaveProfile = Button(self.top, text='Save Profile', textvariable=self.cmdSaveProfileVar, command=self.cmdSaveProfile_Cmd, style='TcmdSaveProfile.TButton')
        self.cmdSaveProfile.setText = lambda x: self.cmdSaveProfileVar.set(x)
        self.cmdSaveProfile.text = lambda : self.cmdSaveProfileVar.get()
        self.cmdSaveProfile.place(relx=0.374, rely=0.03, relwidth=0.183, relheight=0.062)

        self.cmbProfileList = ['',]
        self.cmbProfileVar = StringVar(value='')
        self.cmbProfile = Combobox(self.top, exportselection=0, state='readonly', textvariable=self.cmbProfileVar, values=self.cmbProfileList, font=('Arial',14))
        self.cmbProfile.setText = lambda x: self.cmbProfileVar.set(x)
        self.cmbProfile.text = lambda : self.cmbProfileVar.get()
        self.cmbProfile.place(relx=0.13, rely=0.03, relwidth=0.218)
        self.cmbProfile.bind('<<ComboboxSelected>>', self.cmbProfile_ComboboxSelected)

        self.canvas = Canvas(self.top, takefocus=1, bg='#FFE0C0')
        self.canvas.place(relx=0.009, rely=0.225, relwidth=0.983, relheight=0.753)
        self.canvas.bind('<Button-1>', self.canvas_Button_1)

        self.lblProfileVar = StringVar(value='Profile')
        self.style.configure('TlblProfile.TLabel', anchor='e', font=('Arial',14))
        self.lblProfile = Label(self.top, text='Profile', textvariable=self.lblProfileVar, style='TlblProfile.TLabel')
        self.lblProfile.setText = lambda x: self.lblProfileVar.set(x)
        self.lblProfile.text = lambda : self.lblProfileVar.get()
        self.lblProfile.place(relx=0.009, rely=0.03, relwidth=0.105, relheight=0.047)

class Application(Application_ui):
    def __init__(self, master):
        super().__init__(master)
        self.master.title(f'Kterm Keyboard Layouter {__Version__} [github.com/cdhigh]')
        self.master.bind("<Configure>", self.drawKeyboard) #大小变化后重新绘制
        self.layouts = {}
        self.dirty = False
        self.prevProfileIndex = 0
        self.loadProfiles()
        self.cmbProfileList = list(self.profiles.keys())
        self.cmbProfile.configure(values=self.cmbProfileList)
        self.cmbProfile.current(0)
        self.master.after(200, self.cmbProfile_ComboboxSelected)

    #窗口关闭时提醒
    def EV_WM_DELETE_WINDOW(self, event=None):
        if self.dirty and not askyesno(message='The current layout has not been saved.\nAre you sure to quit?'):
            return
        else:
            self.master.destroy()

    #从文件加载已保存的布局
    def loadProfiles(self):
        self.profiles = BUILTIN_PROFILES.copy()
        if not os.path.isfile(PROFILES_JSON):
            return

        try:
            with open(PROFILES_JSON, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
                if isinstance(profiles, dict):
                    self.profiles.update(profiles)
        except:
            pass

    #选择一个键盘布局
    def cmbProfile_ComboboxSelected(self, event=None):
        if self.dirty and not askyesno('Warning',  'The current layout has not been saved. \n'
            'If you switch to another layout, the current changes will be lost. \n'
            'Are you sure you want to continue?'):
            self.cmbProfile.current(self.prevProfileIndex)
            return

        self.prevProfileIndex = self.cmbProfile.current()
        name = self.cmbProfile.text()
        self.cmdDeleteProfile.configure(state='disable' if name in BUILTIN_PROFILES else 'normal')
        self.optNormal.setValue(1)
        self.createLayout(name)
        self.drawKeyboard()

    #根据预置的键盘布局创建一个layout字典对象，里面的信息更全面，可以直接绘制和保存到文件
    def createLayout(self, profileName):
        profile = self.profiles.get(profileName)
        self.layouts = {}
        self.dirty = False
        if not profile:
            return

        defaultWidth = profile.get('_meta', {}).get('default_width', 1000)
        _keyWidth = lambda k: defaultWidth if isinstance(k, str) else k.get('width', defaultWidth)
        for mode in ['normal', 'caps', 'mod1', 'mod2']:
            self.layouts[mode] = []
            for rowIdx, keyRow in enumerate(profile[mode]):
                row = []
                totalWidth = sum(_keyWidth(key) for key in keyRow)
                for key in keyRow:
                    width = _keyWidth(key)
                    keyObj = {} #生成详细的按键属性集
                    if isinstance(key, str):
                        keyObj['display'] = key
                    else:
                        keyObj['display'] = key.get('display') or f"{key.get('image')}.png"
                    keyObj['width'] = width
                    keyObj['wRatio'] = width / totalWidth  #按键宽度占屏幕宽度的比率
                    keyObj['action'] = '' if isinstance(key, str) else key.get('action')
                    row.append(keyObj)
                self.layouts[mode].append(row)
    
    #获取当前选择模式的键盘布局字典对象
    def getModLayout(self):
        if self.optNormal.value():
            return self.layouts.get('normal')
        elif self.optCaps.value():
            return self.layouts.get('caps')
        elif self.optMod1.value():
            return self.layouts.get('mod1')
        else:
            return self.layouts.get('mod2')

    #更新键盘，重新绘制
    def drawKeyboard(self, event=None):
        layout = self.getModLayout()
        canvas = self.canvas
        canvas.delete('all')
        if not layout:
            return

        MARGIN = 4 #上下左右留空像素，用于显示边框线
        cvsWidth = canvas.winfo_width() - MARGIN * 2
        cvsHeight = canvas.winfo_height() - MARGIN * 2
        rowHeight = cvsHeight / len(layout) #每行高度
        kbFont = Font(family='Courier New', size=16)
        smFont = Font(family='Courier New', size=12)
        for rowIdx, keyRow in enumerate(layout):
            x0 = MARGIN
            y0 = rowIdx * rowHeight + MARGIN
            y1 = y0 + rowHeight
            row = []
            for keyObj in keyRow:
                width = cvsWidth * keyObj.get('wRatio', 0)
                x1 = x0 + width
                canvas.create_rectangle(x0, y0, x1, y1, outline='grey')
                text = keyObj['display']
                if text == ' ' or text.endswith('.png'):
                    sym = PNG_UNICODE_MAP.get(text)
                    font = kbFont if len(sym) < 2 else smFont
                    canvas.create_text(x0 + width / 2, y0 + rowHeight / 2, text=sym, font=font)
                else:
                    canvas.create_text(x0 + width / 2, y0 + rowHeight / 2, text=text, font=kbFont)
                #这些坐标用于鼠标点击时判断点击的按键
                keyObj['x0'] = x0
                keyObj['x1'] = x1
                keyObj['y0'] = y0
                keyObj['y1'] = y1
                x0 = x1

    #更新某一个键
    #keyObj: 表示某个按键的一个字典对象
    #prop: 要修改的某些属性，可以为字典或字符串
    def updateKey(self, keyObj: dict, prop):
        self.dirty = True
        if isinstance(prop, dict):
            display = prop.get('display')
            if display:
                keyObj['display'] = display
            else:
                display = prop.get('image')
                if display:
                    keyObj['display'] = f'{display}.png'
            action = prop.get('action')
            if action:
                keyObj['action'] = action
        else:
            keyObj['display'] = prop
        self.drawKeyboard()

    #创建点击某个按钮的弹出菜单
    def createPopMenu(self, keyObj):
        self.keyMenu = Menu(self.master, tearoff=0, font=("Courier New", 14))
        self.lowerMenu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.upperMenu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.numMenu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.spCharMenu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.latin1Menu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.latin2Menu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.actionMenu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.fxMenu = Menu(self.keyMenu, tearoff=0, font=("Courier New", 14))
        self.keyMenu.add_cascade(label="Lower", menu=self.lowerMenu)
        self.keyMenu.add_cascade(label="Upper", menu=self.upperMenu)
        self.keyMenu.add_cascade(label="Number", menu=self.numMenu)
        self.keyMenu.add_cascade(label="Special Char", menu=self.spCharMenu)
        self.keyMenu.add_cascade(label="Latin Char 1", menu=self.latin1Menu)
        self.keyMenu.add_cascade(label="Latin Char 2", menu=self.latin2Menu)
        self.keyMenu.add_cascade(label="Action", menu=self.actionMenu)
        self.keyMenu.add_cascade(label="Fx", menu=self.fxMenu)

        for a in 'abcdefghijklmnopqrstuvwxyz':
            self.lowerMenu.add_command(label=a, command=partial(self.updateKey, keyObj=keyObj, prop=a))
        for a in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.upperMenu.add_command(label=a, command=partial(self.updateKey, keyObj=keyObj, prop=a))
        for a in '1234567890':
            self.numMenu.add_command(label=a, command=partial(self.updateKey, keyObj=keyObj, prop=a))
        for a in '''~!@#$%^&*()_+`'-={}[]\\/,.<>''':
            self.spCharMenu.add_command(label=a, command=partial(self.updateKey, keyObj=keyObj, prop=a))
        for a in 'àáâãäåāăąæćčçďđèéêëēĕėęěìíîïīįıļ':
            self.latin1Menu.add_command(label=a, command=partial(self.updateKey, keyObj=keyObj, prop=a))
        for a in 'ľñńņňòóôõöōőœøšùúûüůűųýÿźżž':
            self.latin2Menu.add_command(label=a, command=partial(self.updateKey, keyObj=keyObj, prop=a))
        for a in ACTION_LIST:
            a.pop('width', None)
            label = a.get('action', '')
            self.actionMenu.add_command(label=label, command=partial(self.updateKey, keyObj=keyObj, prop=a))
        for idx in range(1, 13):
            a = F(idx)
            self.fxMenu.add_command(label=f'F{idx}', command=partial(self.updateKey, keyObj=keyObj, prop=a))
        return self.keyMenu

    #切换查看不同的键盘模式
    def optMod2_Cmd(self, event=None):
        self.drawKeyboard()
    def optMod1_Cmd(self, event=None):
        self.drawKeyboard()
    def optCaps_Cmd(self, event=None):
        self.drawKeyboard()
    def optNormal_Cmd(self, event=None):
        self.drawKeyboard()

    #将当前布局保存为Kterm直接可用的三个xml
    def cmdSaveXml_Cmd(self, event=None):
        dir_ = filedialog.askdirectory(title="Choose directory to save")
        if not dir_ or not os.path.isdir(dir_):
            return

        kbXml = os.path.join(dir_, 'keyboard.xml')
        kb200Xml = os.path.join(dir_, 'keyboard-200dpi.xml')
        kb300Xml = os.path.join(dir_, 'keyboard-300dpi.xml')
        if os.path.isfile(kbXml) or os.path.isfile(kb200Xml) or os.path.isfile(kb300Xml):
            if not askyesno('Warning', 'The directory you selected contains the XML filenames '
                'that will be generated and overwritten. \nDo you want to continue?'):
                return

        kbRoot = ET.Element('keyboard')
        kbRoot.append(ET.Comment('keyboard for 167 dpi kindles: kt, kt2, kt3'))
        lay = ET.SubElement(kbRoot, 'layout', id="kt keyboard")
        
        normal = self.layouts.get('normal')
        caps = self.layouts.get('caps')
        mod1 = self.layouts.get('mod1')
        mod2 = self.layouts.get('mod2')
        if not all([normal, caps, mod1, mod2]):
            showinfo('Error', 'Not all layouts are valid, something wrong with the program')
            return

        #内嵌函数，比较两个按键是否完全一样
        def equalKeys(key1, key2):
            return ((key1.get('display') == key2.get('display')) and 
                key1.get('action') == key2.get('action'))

        for nmRow, cpRow, m1Row, m2Row in zip(normal, caps, mod1, mod2):
            xmlRow = ET.SubElement(lay, 'row')
            xmlKey = None
            for nmKey, cpKey, m1Key, m2Key in zip(nmRow, cpRow, m1Row, m2Row):
                xmlKey = self.addXmlKeyDefaultNode(xmlRow, nmKey)
                self.addXmlKeyCapsNode(xmlKey, nmKey, cpKey)
                self.addXmlKeyMod1Node(xmlKey, nmKey, m1Key)
                self.addXmlKeyMod2Node(xmlKey, nmKey, m2Key)
            #每行最后一个设置占满剩余空间，避免有的屏幕有剩余空间
            if xmlKey:
                xmlKey.set('fill', 'true')

        #保存文件
        if not event or not (event.state & 0x0004): #Ctrl键状态
            prettifyXml(kbRoot)
        kbXmlStr = ET.tostring(kbRoot, encoding='utf-8', xml_declaration=True).decode('utf-8')
        kb200XmlStr = kbXmlStr.replace('keyboard for 167 dpi kindles: kt, kt2, kt3', 'keyboard for 211 dpi kindles: pw1, pw2')
        kb200XmlStr = kb200XmlStr.replace('kt keyboard', 'kt keyboard 211')
        kb200XmlStr = kb200XmlStr.replace('image:img/', 'image:img-200dpi/')
        kb300XmlStr = kbXmlStr.replace('keyboard for 167 dpi kindles: kt, kt2, kt3', 'keyboard for 299 dpi kindles: pw3, kv, koa')
        kb300XmlStr = kb300XmlStr.replace('kt keyboard', 'kt keyboard 299')
        kb300XmlStr = kb300XmlStr.replace('image:img/', 'image:img-300dpi/')
        with open(kbXml, 'w', encoding='utf-8') as f:
            f.write(kbXmlStr)
        with open(kb200Xml, 'w', encoding='utf-8') as f:
            f.write(kb200XmlStr)
        with open(kb300Xml, 'w', encoding='utf-8') as f:
            f.write(kb300XmlStr)
        #ET.ElementTree(kbRoot).write(kbXml, encoding='utf-8', xml_declaration=True)
        showinfo('Success', f'Successfully saved three layout xml:\n{kbXml}\n{kb200Xml}\n{kb300Xml}')

    #生成XML的key节点，并添加default子节点
    #xmlRow: row节点
    #nmKey: normal状态要显示的按键属性字典
    #返回生成的 Key节点
    def addXmlKeyDefaultNode(self, xmlRow, nmKey):
        width = nmKey.get('width', 1000)
        display = nmKey.get('display', '')
        if (len(display) == 1) and display.islower():
            attrs = {'width': str(width), 'obey-caps': 'true'}
        else:
            attrs = {'width': str(width)}
        xmlKey = ET.SubElement(xmlRow, 'key', **attrs)

        attrs = {'display': f'image:img/{display}' if display.endswith('.png') else display}
        if (action := nmKey.get('action')):
            attrs['action'] = action
        ET.SubElement(xmlKey, 'default', **attrs)
        return xmlKey

    #添加XML Key节点的shifted子节点
    #xmlKey: Key节点
    #nmKey, cpKey: normal/caps状态的按键信息字典
    def addXmlKeyCapsNode(self, xmlKey, nmKey, cpKey):
        display = cpKey.get('display')
        action = cpKey.get('action')
        if ((nmKey.get('display') == display) and (nmKey.get('action') == action)):
            return

        attrs = {'display': f'image:img/{display}' if display.endswith('.png') else display}
        if action:
            attrs['action'] = action
        ET.SubElement(xmlKey, 'shifted', **attrs)

    #添加XML Key节点的mod1子节点
    #xmlKey: Key节点
    #nmKey, m1Key: normal/mod1状态的按键信息字典
    def addXmlKeyMod1Node(self, xmlKey, nmKey, m1Key):
        display = m1Key.get('display')
        action = m1Key.get('action')
        if ((nmKey.get('display') == display) and (nmKey.get('action') == action)):
            return

        attrs = {'display': f'image:img/{display}' if display.endswith('.png') else display}
        if action:
            attrs['action'] = action
        ET.SubElement(xmlKey, 'mod1', **attrs)

    #添加XML Key节点的mod2子节点
    #xmlKey: Key节点
    #nmKey, m2Key: normal/mod2状态的按键信息字典
    def addXmlKeyMod2Node(self, xmlKey, nmKey, m2Key):
        display = m2Key.get('display')
        action = m2Key.get('action')
        if ((nmKey.get('display') == display) and (nmKey.get('action') == action)):
            return

        attrs = {'display': f'image:img/{display}' if display.endswith('.png') else display}
        if action:
            attrs['action'] = action
        ET.SubElement(xmlKey, 'mod2', **attrs)

    #保存当前修改后的布局为json以便后续修改
    def cmdSaveProfile_Cmd(self, event=None):
        name = simpledialog.askstring('Name', 'Please enter a profile name to save')
        if not name:
            return

        if name in self.profiles and not askyesno('Warning', 'The name you entered already exists.\n'
                'Do you want to overwrite the existing layout?'):
            return

        profiles = copy.deepcopy(self.profiles)
        profiles[name] = copy.deepcopy(self.layouts)
        if self.writeProfileToFile(profiles):
            self.profiles[name] = self.layouts
            if name not in self.cmbProfileList:
                self.cmbProfileList.append(name)
            self.cmbProfile.configure(values=self.cmbProfileList)
            self.cmbProfile.current(self.cmbProfileList.index(name))
            self.cmdDeleteProfile.configure(state='disable' if name in BUILTIN_PROFILES else 'normal')
            self.dirty = False

    #将布局写到文件
    def writeProfileToFile(self, profiles):
        for pName in BUILTIN_PROFILES: #保存前移除内置的布局
            profiles.pop(pName, None)

        #去除里面实时计算的元素
        for pName in profiles:
            for mode in profiles[pName]:
                for row in profiles[pName][mode]:
                    for key in row:
                        key.pop('wRatio', None)
                        key.pop('x0', None)
                        key.pop('x1', None)
                        key.pop('y0', None)
                        key.pop('y1', None)

        try:
            with open(PROFILES_JSON, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            showinfo('Error', f'Failed to write {PROFILES_JSON}: {ste(e)}')
            return False

    #删除当前布局
    def cmdDeleteProfile_Cmd(self, event=None):
        name = self.cmbProfile.text()
        if name in BUILTIN_PROFILES:
            showinfo('Built in profile', 'You cannot delete built-in profiles')
            return

        if not askyesno('Confirmation', f'Please confirm if you want to delete the layout "{name}"?'):
            return

        profiles = copy.deepcopy(self.profiles)
        profiles.pop(name, None)
        if self.writeProfileToFile(profiles):
            self.profiles.pop(name, None)
            if name in self.cmbProfileList:
                self.cmbProfileList.remove(name)
            self.cmbProfile.configure(values=self.cmbProfileList)
            self.cmbProfile.current(0)
            self.cmbProfile_ComboboxSelected()
            name = self.cmbProfile.text()
            self.cmdDeleteProfile.configure(state='disable' if name in BUILTIN_PROFILES else 'normal')
            self.dirty = False

    #点击某个键盘按键后弹出菜单，选择其他的字符或动作
    def canvas_Button_1(self, event):
        x = event.x
        y = event.y
        for row in (self.getModLayout() or []):
            for keyObj in row:
                kget = keyObj.get
                if (kget('x0') <= x <= kget('x1')) and (kget('y0') <= y <= kget('y1')):
                    self.createPopMenu(keyObj).post(event.x_root, event.y_root)
                    break

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()

