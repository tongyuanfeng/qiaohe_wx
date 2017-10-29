import re
import os
import pymysql


def get_cellphone(str):
    "电话"
    cellphone = ""

    try:
        pattern = re.compile(r'(13\d|14[57]|15[^4,\D]|17[13678]|18\d)\d{8}|170[0589]\d{7}')
        x = pattern.search(str)
        cellphone = str[x.regs[0][0]:x.regs[0][1]]
    except Exception as e:
        print(e)

    return cellphone


def get_mail(str):
    "邮箱"
    mail = ""

    try:
        pattern = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
        x = pattern.search(str)
        mail = str[x.regs[0][0]:x.regs[0][1]]
    except Exception as e:
        print(e)

    return mail


def get_birthday(str):
    "出生年月   匹配日期（年-月-日）  匹配日期（年/月/日） 88年4月 "
    birthday = ""

    try:
        pattern = re.compile(
            r'((((1[6-9]|[2-9]\d)\d{2})/(1[02]|0?[13578])/([12]\d|3[01]|0?[1-9]))|(((1[6-9]|[2-9]\d)\d{2})/(1[012]|0?[13456789])/([12]\d|30|0?[1-9]))|(((1[6-9]|[2-9]\d)\d{2})-0?2-(1\d|2[0-8]|0?[1-9]))|(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))-0?2-29-))')
        x = pattern.search(str)
        birthday += str[x.regs[0][0]:x.regs[0][1]]
    except Exception as e:
        print(e)
    try:
        pattern = re.compile(
            r'((((1[6-9]|[2-9]\d)\d{2})-(1[02]|0?[13578])-([12]\d|3[01]|0?[1-9]))|(((1[6-9]|[2-9]\d)\d{2})-(1[012]|0?[13456789])-([12]\d|30|0?[1-9]))|(((1[6-9]|[2-9]\d)\d{2})-0?2-(1\d|2[0-8]|0?[1-9]))|(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))-0?2-29-))')
        x = pattern.search(str)
        birthday += str[x.regs[0][0]:x.regs[0][1]]
    except Exception as e:
        print(e)
    try:
        pattern = re.compile(r'((((1[6-9]|[2-9]\d)\d{2})年(1[02]|0?[13578])月))')
        x = pattern.search(str)
        birthday += str[x.regs[0][0]:x.regs[0][1]]
    except Exception as e:
        print(e)

    return birthday


def get_sex(str):
    "性别"
    sex = ""
    try:
        pattern = re.compile(r'男')
        x = pattern.search(str)
        sex = str[x.regs[0][0]:x.regs[0][1]]
    except Exception as e:
        print(e)
    return sex


def get_name(str):
    "姓名"
    name = ""
    try:
        point = re.search(r'姓  名', str)
        x = point.regs[0][1]
        name += str[x:x + 6]
    except:
        pass

    try:
        point = re.search(r'姓名', str)
        x = point.regs[0][1]
        name += str[x:x + 6]
    except:
        pass

    try:
        point = re.search(r'流程状态', str)
        x = point.regs[0][0]
        name += str[x - 3:x]
    except:
        pass
    try:
        point = re.search(r'ID：', str)
        x = point.regs[0][0]

        name += str[x:].split('\n')[1]
    except:
        pass

    return name.strip('\n').strip('：').strip(':').strip('\r').strip(' ')


def get_graduate_institutions(str):
    "毕业院校"
    graduate_institutions = ""
    try:
        point = re.search(r'毕业院校', str)
        x = point.regs[0][1]

        graduate_institutions += str[x:].split('\n')[0]
        graduate_institutions += str[x:].split('\n')[1]
    except:
        pass

    try:
        point = re.search(r'教育经历', str)
        x = point.regs[0][1]

        graduate_institutions += str[x:].split('\n')[0]
        graduate_institutions += str[x:].split('\n')[1]
        graduate_institutions += str[x:].split('\n')[2]
    except:
        pass

    try:
        point = re.search(r'学　校', str)
        x = point.regs[0][1]

        graduate_institutions += str[x:].split('\n')[1]
        graduate_institutions += str[x:].split('\n')[0]
    except:
        pass

    return graduate_institutions.strip('\n').strip('：').strip(':').strip('\r').strip(' ')


def get_profession(str):
    "专业"
    profession = ""
    try:
        point = re.search(r'专  业', str)
        x = point.regs[0][1]

        profession += str[x:].split('\n')[0]
        profession += str[x:].split('\n')[1]
        profession += str[x:].split('\n')[2]

    except:
        pass

    try:
        point = re.search(r'业：', str)
        x = point.regs[0][1]

        profession += str[x:].split('\n')[0]
        profession += str[x:].split('\n')[1]
        profession += str[x:].split('\n')[2]
    except:
        pass

    try:
        # if 1:
        point = re.search(r'专业：', str)
        x = point.regs[0][1]

        profession += str[x:].split('\n')[0]
        profession += str[x:].split('\n')[1]
        profession += str[x:].split('\n')[2]


    except:
        pass

    return profession.strip('\n').strip('：').strip(':').strip('\r').strip(' ')


def get_record(str):
    "最高学历"
    record = ""
    try:
        point = re.search(r'学  历', str)
        x = point.regs[0][1]

        record += str[x:].split('\n')[0]
        record += str[x:].split('\n')[1]

    except:
        pass

    try:
        point = re.search(r'学历：', str)
        x = point.regs[0][1]

        record += str[x:].split('\n')[0]
        record += str[x:].split('\n')[1]


    except:
        pass

    try:
        point = re.search(r'学位：', str)
        x = point.regs[0][1]

        record += str[x:].split('\n')[0]
        record += str[x:].split('\n')[1]
    except:
        pass

    try:
        point = re.search(r'学位', str)
        x = point.regs[0][1]

        record += str[x:].split('\n')[0]
        record += str[x:].split('\n')[1]
    except:
        pass

    return record.strip('\n').strip('：').strip(':').strip('\r').strip(' ')


def get_work_year(str):
    "工作年限"
    work_year = ""
    try:
        point = re.search(r'年工作经验', str)
        x = point.regs[0][0]

        print(str[x - 2:x].split('\n')[-1])
        print(str[x:].split('\n')[1])
        work_year += str[x - 2:x].split('\n')[-1]
        work_year += str[x:].split('\n')[1]

    except:
        pass
    try:
        point = re.search(r'工作年限', str)
        x = point.regs[0][1]

        print(str[x:].split('\n')[0])
        work_year += str[x:].split('\n')[0]
    except:
        pass

    try:
        point = re.search(r'工作年限：', str)
        x = point.regs[0][1]

        print(str[x:].split('\n')[0])
        print(str[x:].split('\n')[1])

        work_year += str[x:].split('\n')[0]
        work_year += str[x:].split('\n')[1]
    except:
        pass
    return work_year.strip('\n').strip('：').strip(':').strip('\r').strip(' ')


def insert_sql(db, sql_cmd,args):
    cursor = db.cursor()
    print(sql_cmd)
    cursor.execute(sql_cmd,args)
    db.commit()


if __name__ == '__main__':
    db = pymysql.connect(host="qiaohequan.com", user="root", passwd="qiaohejiayou", db="qiaohe", port=3306,
                         charset='utf8')

    for root, dirs, files in os.walk('newdir'):
        for file in files:
            filename = os.path.join(root, file)
            str = open(filename, 'r').read()

            cellphone = get_cellphone(str)
            mail = get_mail(str)
            birthday = get_birthday(str)
            sex = get_sex(str)
            name = get_name(str)
            graduate_institutions = get_graduate_institutions(str)
            profession = get_profession(str)
            record = get_record(str)
            work_year = get_work_year(str)
            newstr = ''.join(str.split())

            sql_cmd = """INSERT INTO qiaohe.resume (cellphone,mail,birthday,name,sex,graduate_institutions,profession,record,work_year,file) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            args= (cellphone, mail, birthday, name, sex, graduate_institutions, profession, record, work_year, newstr.replace('\'','\\\''))
            insert_sql(db, sql_cmd,args)
    db.close()
