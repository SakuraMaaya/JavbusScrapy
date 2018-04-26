import pymysql

class DataTools:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234', db='Javbus', charset='utf8')
        self.cursor = self.conn.cursor()

    def get_type_id(self, type):
        self.cursor.execute('''SELECT id From TypeData WHERE type = '%s' '''
                            %(type))
        values = self.cursor.fetchall()

        if len(values) > 0:
            return values[0][0]
        else:
            self.cursor.execute('''SELECT max(id) From TypeData ''')
            values = self.cursor.fetchall()

            self.cursor.execute('''
                INSERT INTO TypeData(id, type, parent)
                VALUES (%s, '%s', '%s')
                ''' % (values[0][0] + 1, type, '暂无'))

            self.conn.commit()
            return values[0][0] + 1

    def get_actress_id(self,id):
        self.cursor.execute('''SELECT aid From ActressData WHERE aid = '%s' '''
                            %(id))
    def is_crawled(self, bango):
        self.cursor.execute('''SELECT bango From MovieData WHERE bango = '%s' '''
                            %(bango))
        values = self.cursor.fetchall()
        if len(values) > 0:
            return True
        return  False

    def __del__(self):
        self.cursor.close()
        self.conn.close()