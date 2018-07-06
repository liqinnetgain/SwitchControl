import xlwt
import xlrd
import pandas as pd
import re
import telnetlib
import time

def write_command(instance,command):
    finish = '\r'
    instance.write(command.encode('ascii')+finish.encode('ascii'))

#读Excel函数
def read_excel(file,row=0,clo=0):
    wb = xlrd.open_workbook(filename=file)
    sheet = wb.sheet_by_name('光衰清单')
    return sheet.cell_value(row,clo)

def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.colour_index = 4
    font.height = height
    style.font = font
    return style

def write_excel(file,row,clo,data):
    f = xlwt.Workbook()
    shee1 = f.add_sheet('Test',cell_overwrite_ok=True)
    shee1.write(row,clo,data,set_style('Times New Roman',220,True))
    f.save(file)


def telnet_switch(file,account):
    global IP,DEVICE_ID_,PON_PORT,ONU_ID#声明全局变量
    df = pd.read_excel(file)#打开光衰表文件
    olt_ip = str(re.findall(r'\d+.\d+.\d+.\d+', str(df[df['账号'] == account]['OLT-IP地址'])))#使用正则表达式匹配IP
    device = str(re.findall(r'[A-Z][A-Z0-9]{3,7}', str(df[df['账号'] == account]['设备型号'])))#使用正则表达式匹配设备型号
    pon = str(re.findall(r'\d/\d/\d', str(df[df['账号'] == account]['PON口'])))#使用正则表达式匹配Pon口
    onu = str(re.findall(r'\d*', str(df[df['账号'] == account]['ONUID'])))  # 使用正则表达式匹配Pon口
    IP = eval(olt_ip.strip('[[]]'))#去掉字符串两边的字符
    DEVICE_ID_ = eval(device.strip('[[]]'))#去掉字符串两边的字符
    PON_PORT = eval(pon.strip('[[]]'))#去掉字符串两边的字符
    ONU_ID = eval(onu.strip('[[]]'))  # 去掉字符串两边的字符
    print(onu)
    tn = telnetlib.Telnet(host=IP, port=5000)  # 开启Telnet
    if DEVICE_ID_ == 'MA5683T':
        pass
    elif DEVICE_ID_ == 'MA5680T':
        pass
    else:
        pass
    command_list = ['conf','terminal','exit']#待执行的命令
    for command in command_list:#输入命令并执行
        write_command(tn,command)
        time.sleep(0.5)

