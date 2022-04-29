* 参考文档
    1. http://xoomer.virgilio.it/infinity77/wxPython/widgets.html
    关于radiobutton/radiobox的使用说明

    2. 主要库
    操作界面    wxPython
    Word操作    from docx import Document

    3. Python打包 exe
        切换到代码目录
        pyinstaller -F xxx.py （这里的-F如果缺少，会导致生成一个main目录

* 版本
    V1
        实现主要功能
            不同文件名取号
            自动打开生成word

        Bug 
            文件名应该不带docx
            文件名显示不全

    V2
        实现功能
            txt
            取出文件名中docx
        Bug
            选择RNF/IRF等时，文件名应自动更新


