#encoding=UTF-8
import MySQLdb

#mysql 初始化
class CORE():
    'mysql 登录'
    host = '127.0.0.1'
    user = 'root'
    passwd = ''
    db = 'portscan'
    port = 3306
    charset = 'utf-8'
    table_name = 'portlist'
    def __init__(self):
        try:
            self.db=MySQLdb.connect(host=CORE.host,user=CORE.user,passwd=CORE.passwd,charset='utf8')#登录数据库
            self.mysql = self.db.cursor()
            sql = "select schema_name from information_schema.schemata where schema_name='%s'" % (CORE.db)
            self.mysql.execute(sql)
            if not self.mysql.fetchone():
                sql = "CREATE DATABASE IF NOT EXISTS %s " % (CORE.db)
                self.mysql.execute(sql)
                self.db.select_db(CORE.db) #选择数据库
            else:
                self.db.select_db(CORE.db) #选择数据库
        except Exception,e:
            print e

#添加数据方法
    def increase(self,sql):
        try:
            self.mysql.execute(sql) #操作数据
            self.db.commit()#提交数据
        except Exception,e:
            print e

#添加数据
    def select(self,sql):
        try:
            self.mysql.execute(sql) #操作数据
            # 获取所有记录列表
            results = self.mysql.fetchall()
            return results
        except Exception,e:
            print e

    def create_table(self,CORE):
        try:
            self.increase("drop table if exists `portlist`")
            CORE.increase("""
                        create table portlist(
                        id int not null primary key auto_increment,
                        host varchar(50),
                        server_name varchar(50) not null default 'unknown',
                        port int not null
                        )charset utf8;
                    """)
            self.increase("drop table if exists `bannerlist`")
            CORE.increase("""
                        create table bannerlist(
                        url varchar(50),
                        status_code int,
                        title varchar(50) not null default 'unknown',
                        banner varchar(50) not null default 'unknown'
                        )charset utf8;
                    """)
        except:
            pass

    def close_db(self):
        self.db.close()

