from InoutManager.excelInout import *

file = open('C:\\Users\\zhandonbi\\Documents\\Tencent Files\\1430789575\\FileRecv\\18级选课方案-职场英语.xlsx', 'rb')
print(read(file, 'Sheet1'))
