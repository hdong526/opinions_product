from db_oracle import OracleBase

from config_db import *
from config_spider import *

class OracleEngine(OracleBase):
    def __init__(self, uname=ORACLE_UNAME, passwd=ORACLE_PASSWORD, addr=ORACLE_ADDR):
       super(OracleEngine,self).__init__(uname,passwd,addr)

    def update_table(self, table, condition=None, **kwargs):
        #print(condition)
        str_update = ','.join([list(kwargs.keys())[i-1] + '=:' + str(i) for i in range(1, len(kwargs)+1)])
        #print(str_update)
        if condition:
            str_sql = '''update  {} set {} where {}'''.format(
                table,
                str_update,
                condition
            )
        else:
            str_sql = '''update  {} set {}'''.format(
                table,
                str_update
            )
        print(str_sql)
        self.opt_sql(str_sql, list(kwargs.values()))


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
    #db = OracleEngine('h_dong', 'h_dong', '192.168.1.107:1521/orcl')
    db = OracleEngine()
    df = db.select_table('yuqing_domain', 'flag=1')[['DOMAIN', 'DOMAIN_NAME']]
    domain = df.set_index('DOMAIN')['DOMAIN_NAME'].to_dict()
    # print(list(df['DOMAIN']))
    df2 = db.select_table('yuqing_domain', '')[['DOMAIN', 'DOMAIN_NAME']]
    domain_2 = df2.set_index('DOMAIN')['DOMAIN_NAME'].to_dict()
    print(domain_2, len(domain_2))
    # db.update_table('yuqing_domain',
    #     **{
    #         'flag':'asd',
    #         'c0001':'sasdasdad',
    #         'c0002':6666,
    #     }
    # )

    # for i in DICTDOMAIN:
    #     db.update_table('yuqing_domain', "domain='{}'".format(i),
    #         **{
    #             'flag':'1',
    #         }
    #     )
    #print(DICTDOMAIN_2)
##    db.insert_one_data('temp_emp',
##        **{
##            'ename': 'd',
##            'comm': 134,
##            'dname': 'rr',
##        }
##    )
