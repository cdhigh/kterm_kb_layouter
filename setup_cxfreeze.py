#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""使用cxFreeze打包成EXE文件
Author: cdhigh <https://github.com/cdhigh>
"""

import sys, os, re
from cx_Freeze import setup, Executable

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None
#base = None
APP_PATH = os.path.dirname(__file__)

appVer = '1.0'
appMain = os.path.join(APP_PATH, 'kterm_kb_layouter.py')
if os.path.exists(appMain):
    with open(appMain, 'r', encoding='utf-8') as f:
        slMain = f.read().split('\n')
    
    PATT_VERSION = r"^__Version__\s*=\s*[\"\']v{0,1}([0123456789.-]+?)[\"\'](.*)"
    for line in slMain:
        mt = re.match(PATT_VERSION, line)
        if mt:
            appVer = mt.group(1)
            break

build_exe_options = {'packages': ['tkinter'], 
                    'excludes' : ['pyQt5', 'PIL'],
                    'include_files' : [],
                    'optimize' : 2,
                    }

exe = Executable(script='kterm_kb_layouter.py',
    base=base,
    target_name='kterm_kb_layouter.exe')

setup(name='kterm_kb_layouter', 
    version=appVer,
    description='kterm_kb_layouter - Designer for kterm keyboard',
    options={'build_exe': build_exe_options},
    executables=[Executable(script='kterm_kb_layouter.py', base=base, icon='app.ico',)])