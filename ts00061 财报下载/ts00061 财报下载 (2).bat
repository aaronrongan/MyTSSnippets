rem 191128 该文件停止更新，转为从Snippets文件夹直接更新。不再用Github维护（因为速度较慢，不够直观，手动更新原因）

rem 调用FinDownloader.py

rem 参数:
rem   codenumber = '002271'
rem   downloadtype = ’4‘  # 4-年报；1-1季报；2-中报；3-3季报；5-招股; 0-4个季度报表全部下载
rem   downloadflag = True  # True为实际下载，False为不下载
rem   debugflag = False  # True为输出调试信息，False为不输出
rem   yeartype 年度, 为’0‘则下载所有报表 #

rem	stock_fulllist.csv 股票代码对应表
rem	stock.csv	需要导出的股票列表


cd C:\Users\Aaron\PycharmProjects\FinReportDownloader\
python C:\Users\Aaron\PycharmProjects\FinReportDownloader\ExecDwnFR.py