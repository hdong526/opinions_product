import cx_Oracle
import pandas as pd

class OracleBase(object):
    def __init__(self, uname, passwd, addr):
        self.o_db = cx_Oracle.connect(uname, passwd, addr, encoding='utf8')
        self.cursor = self.o_db.cursor()

    def __del__(self):
        self.cursor.close()
        self.o_db.close()

    def opt_sql(self, str_sql, list_values=None):
        #print(str_sql)
        if list_values is None:
            self.cursor.execute(str_sql)
        else:
            #print(str_sql, list_values)
            self.cursor.execute(str_sql, list_values)
        self.o_db.commit()

    def get_data(self, str_sql):
        self.cursor.execute(str_sql)
        rows = self.cursor.fetchall()
        return rows

    def get_DataFrame(self, str_sql, columns=[]):
        #print(str_sql)
        self.cursor.execute(str_sql)
        rows = self.cursor.fetchall()
        if columns:
            df = pd.DataFrame(rows,columns = columns)
        else:
            df = pd.DataFrame(rows,columns = [i[0] for i in self.cursor.description])
        df = df.fillna('')
        return df

    def get_one_data(self, str_sql):
        #print(str_sql)
        self.cursor.execute(str_sql)
        data = self.cursor.fetchone()
        return data
