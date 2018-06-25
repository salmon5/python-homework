#_*_coding:utf-8_*_
__author__ = 'Alex Li'

import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASEDIR)

from plugins.base import BasePlugin

def monitor(frist_invoke=1):
    shell_command = 'sar -n DEV 1 5 |grep -v IFACE |grep Average'
    contents = BasePlugin('192.168.231.110', 22, 'root', 'oracle').exec_shell_cmd(shell_command)
    #result = subprocess.Popen(shell_command,shell=True,stdout=subprocess.PIPE).stdout.readlines()
    #print(result)
    value_dic = {'status':0, 'data':{}}
    li = contents['RESULT'].split("\n")  # 字符串转列表
    content_list = li[:len(li) - 1]  # 取列表开始到倒数第二个元素，最后一个元素为空

    for line in content_list:
        line = line.split()
        nic_name,t_in,t_out = line[1],line[4],line[5]
        value_dic['data'][nic_name] = {"t_in":line[4], "t_out":line[5]}
    return value_dic

if __name__ == '__main__':
    print(monitor())