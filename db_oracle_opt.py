from db_oracle import OracleBase

from config_db import *

class OracleEngine(OracleBase):
    def __init__(self, uname=ORACLE_UNAME, passwd=ORACLE_PASSWORD, addr=ORACLE_ADDR):
       super(OracleEngine,self).__init__(uname,passwd,addr)

    # 插入表可变长参数
    def insert_one_data(self, table, **kwargs):
        list_values = list(kwargs.values())
        #print(list_values)
        str_keys = ','.join(list(kwargs.keys()))
        str_info = ':' + ',:'.join([str(i) for i in range(1, len(kwargs) + 1)])
        str_sql = '''insert into {}({}) values ({})'''.format(
            table,
            str_keys,
            str_info
        )
        #print(str_sql)
        self.opt_sql(str_sql, list_values)

    def func_insert_df(self, data, table):
        dict_info = data.to_dict()
        self.insert_one_data(table, **dict_info)

    def insert_DataFrame(self, table, df):
        df.apply(self.func_insert_df, axis=1, args=(table, ))


    def clear_table(self, table):
        str_sql = 'delete from {}'.format(table)
        self.opt_sql(str_sql)

    def select_table(self, table, condition, bool_oneData=False, *args):
        #list_values = list(kwargs.values())
        if len(args):
            str_fields = ','.join(args)
        else:
            str_fields = '*'
        if condition:
            str_condition = 'where ' + condition
        else:
            str_condition = ''

        str_sql = 'select {} from {} {}'.format(str_fields, table, str_condition)
        if bool_oneData:
            df = self.get_one_data(str_sql)
        else:
            df = self.get_DataFrame(str_sql, args)
        return df
        #print(df)


if __name__ == '__main__':
    db = OracleEngine('h_dong', 'h_dong', '192.168.1.107:1521/orcl')

    #print(DICTDOMAIN_2)
##    db.insert_one_data('temp_emp',
##        **{
##            'ename': 'd',
##            'comm': 134,
##            'dname': 'rr',
##        }
##    )
