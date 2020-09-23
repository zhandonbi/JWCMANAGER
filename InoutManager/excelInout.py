import pandas
from db_operator.op_message import EditMessage
import os

file = open('C:\\Users\\zhandonbi\\Documents\\Tencent Files\\1430789575\\FileRecv\\18级选课方案-职场英语.xlsx', 'rb')
a = pandas.read_excel(file)
print(a.values.tolist())
b = 1


def read(file, sheetName):
    file = pandas.read_excel(file, sheet_name=sheetName)
    return file.values.tolist()[1:]
