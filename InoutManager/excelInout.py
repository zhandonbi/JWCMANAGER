import numpy as np
import pandas

from db_operator.op_message import EditMessage


def read(groupName, file, sheetName):
    em = EditMessage()
    file = pandas.read_excel(file, sheet_name=sheetName)
    file = file.astype(object).where(pandas.notnull(file), None)
    list_name = file.columns.values
    file_list = np.array(file).tolist()
    res = em.creat_group(groupName, list_name, file_list)
    em.close_link()
    return res
