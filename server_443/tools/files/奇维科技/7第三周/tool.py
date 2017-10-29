from win32com import client as wc
import os
import fnmatch

all_FileNum = 0
debug = 0


def Translate(path):
    '''''
    将一个目录下所有doc和docx文件转成txt
    该目录下创建一个新目录newdir
    新目录下fileNames.txt创建一个文本存入所有的word文件名
    本版本具有一定的容错性，即允许对同一文件夹多次操作而不发生冲突
    '''
    global debug, all_FileNum

        # 该目录下所有文件的名字
    files = os.listdir(path)
    # 该目下创建一个新目录newdir，用来放转化后的txt文本
    New_dir = os.path.abspath(os.path.join(path, 'newdir'))
    if not os.path.exists(New_dir):
        os.mkdir(New_dir)

        # 创建一个文本存入所有的word文件名
    fileNameSet = os.path.abspath(os.path.join(New_dir, 'fileNames.txt'))
    o = open(fileNameSet, "w")
    try:
        for filename in files:

                # 如果不是word文件：继续
            if not fnmatch.fnmatch(filename, '*.doc') and not fnmatch.fnmatch(filename, '*.docx'):
                continue;
                # 如果是word临时文件：继续
            if fnmatch.fnmatch(filename, '~$*'):
                continue;

            docpath = os.path.abspath(os.path.join(path, filename))

            # 得到一个新的文件名,把原文件名的后缀改成txt
            new_txt_name = ''
            if fnmatch.fnmatch(filename, '*.doc'):
                new_txt_name = filename[:-4] + '.txt'
            else:
                new_txt_name = filename[:-5] + '.txt'

            word_to_txt = os.path.join(os.path.join(path, 'newdir'), new_txt_name)

            wordapp = wc.Dispatch('Word.Application')
            doc = wordapp.Documents.Open(docpath)
            # 为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4
            doc.SaveAs(word_to_txt, 4)
            doc.Close()
            o.write(word_to_txt + '\n')
            all_FileNum += 1
    finally:
        wordapp.Quit()


if __name__ == '__main__':

    mypath = os.getcwd()
    print('生成的文件有:')
    Translate(mypath)
