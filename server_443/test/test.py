import os
import pymysql


def insert_sql(db, sql_cmd):
    cursor = db.cursor()
    print(sql_cmd)
    try:
        cursor.execute(sql_cmd)
        db.commit()
    except:
        pass


def select(db, sql_cmd):
    cursor = db.cursor()

    cursor.execute(sql_cmd)
    return cursor.fetchall()


if __name__ == '__main__':

    my_db = pymysql.connect(host="qiaohequan.com", user="root", passwd="qiaohejiayou", db="qiaohe", port=3306,
                            charset='utf8')

    if 0:
        cmd = "select role,role_character from qiaohe.playbook_player where pid=38"
        for line in select(my_db, cmd):
            print(line)
            cmd = "insert into qiaohe.playbook_role_info (pid,playbook_name,role_name,role_character)values(3,'愤怒的葡萄','%s','%s')" % (line[0],line[1])
            insert_sql(my_db,cmd)

    if 0:
        cmd = "select nickname,played_book from qiaohe.user"
        for line in select(my_db, cmd):
            # print(line)
            nickname = line[0]
            played_book = line[1]
            try:
                tmp_l = played_book.split(';')
                # print(tmp_l)
                res = []
                for e in tmp_l:
                    if e not in res:
                        res.append(e)

                cmd = "update qiaohe.user set played_book='%s' where nickname='%s'" % (';'.join(res), nickname)
                print(cmd)
                insert_sql(my_db, cmd)
            except:
                pass

    if 1:
        cmdx = "select role,role_character from playbook_player  where pid = 43"
        res = select(my_db, cmdx)
        print(res)
    if 1:
        cmdx = "select nickname from playbook_player where pid = 43"
        res = select(my_db, cmdx)
        # print(res)
        for line in res:
            nickname =line[0]
            cmd = "select nickname,m_character from user where nickname='%s'" % nickname
            print(select(my_db,cmd))

    if 0:

        cmd = "SELECT weixin_id,nickname,level FROM qiaohe.playbook_player where pid = 43"
        for line in select(my_db,cmd):
            # print(line)
            weixin_id=line[0]
            nickname = line[1]
            if 1:
                cmdx = "select * from user where nickname='%s'" % nickname
                res=select(my_db,cmdx)
                print(res)


            # if len(res) >0:
            #     cmdx = "update user set weixin_id='%s',played_book=concat(played_book,';%s') where nickname='%s'" % (
            #     weixin_id, '致命巧克力', nickname)
            # else:
            #     cmdx="insert into user(weixin_id,nickname,level,played_book) values('%s','%s','%s','%s')" % (weixin_id,nickname,'F',"酒红色的谋杀")
            #     # pass
            # # print(cmdx)
            # insert_sql(my_db,cmdx)


