#同时打开多个工作文件，shf/irf

import os 
import socket

# computername=input('请输入电脑名称:1.MyWorkStation;2.MyMacWin;3.PLRWorkstation;')
hostname=socket.gethostname()

if hostname=='MyWorkstation':
    os.startfile(u'I:/MyZoteroFiles_SHF/SHF15120101 Python学习笔记.docx')
    os.startfile(u'I:/MyZoteroFiles_IRF/IRF19021701 量化编程系统说明书.docx')
    os.startfile(u'I:/MyZoteroFiles_IRF/IRF19100306 量化投资学习笔记.docx')
elif hostname=='MyMacWin10':
    os.startfile(u'C:/Users/aaron/Documents/MyZoteroFiles_SHF/SHF15120101 Python学习笔记.docx')
    #os.startfile(u'C:/Users/aaron/Documents/MyZoteroFiles_SHF/SHF15120101 Python学习笔记.docx')
    os.startfile(u'C:/Users/aaron/Documents/MyZoteroFiles_IRF/IRF19021701 量化编程系统说明书.docx')
    os.startfile(u'C:/Users/aaron/Documents/MyZoteroFiles_IRF/IRF19100306 量化投资学习笔记.docx')