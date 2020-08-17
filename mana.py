# coding=utf-8
import re
import log_handler
from AutomatorR import *

log = log_handler.LOG('log/mana.txt')  # 初始化日志文件


def run_main(address, account, password, fun, kickflag=0):
    # 主功能体函数
    # 请在本函数中自定义需要的功能

    a = AutomatorR(address, account)
    a.start()
    print('>>>>>>>即将登陆的账号为：', account, '密码：', password, '<<<<<<<', '\r\n')
    a.login_auth(account, password)  # 注意！请把账号密码写在zhanghao.txt内
    log.Account_Login(account)
    a.init_home()  # 初始化，确保进入首页
    a.sw_init()  # 初始化刷图
    a.dianzan(1)
    a.dixiacheng()  # 地下城 如果是首次使用需要跳过剧情，可以在括号中填入参数1
    a.shouqu()  # 收取所有礼物
    if kickflag == 1:
        a.tichuhanghui()

    a.change_acc()  # 退出当前账号，切换下一个
    log.Account_Logout(account)


def invitemain(address, account, password, inviteUID):
    # 邀请入会函数，请不要更改本函数中的功能
    a = AutomatorR(address, account)
    a.start()
    print('>>>>>>>即将登陆的账号为：', account, '密码：', password, '<<<<<<<', '\r\n')
    a.login_auth(account, password)  # 注意！请把账号密码写在zhanghao.txt内
    a.init_home()
    a.yaoqinghanghui(inviteUID)
    a.change_acc()  # 退出当前账号，切换下一个


def acceptmain(address, account, password):
    # 接受入会邀请函数，请不要更改本函数中的功能
    a = AutomatorR(address, account)
    a.start()
    print('>>>>>>>即将登陆的账号为：', account, '密码：', password, '<<<<<<<', '\r\n')
    a.login_auth(account, password)  # 注意！请把账号密码写在zhanghao.txt内
    a.init_home()
    a.jieshouhanghui()
    a.change_acc()  # 退出当前账号，切换下一个


def connect():  # 连接adb与uiautomator
    try:
        os.system('adb connect 127.0.0.1:62001')  # Nox
        os.system('python -m uiautomator2 init')
    except:
        print('连接失败')

    result = os.popen('adb devices')  # 返回adb devices列表
    res = result.read()
    lines = res.splitlines()[0:]
    while lines[0] != 'List of devices attached':
        del lines[0]
    del lines[0]  # 删除表头

    device_dic = {}  # 存储设备状态
    for i in range(0, len(lines) - 1):
        lines[i], device_dic[lines[i]] = lines[i].split('\t')[0:]
    lines = lines[0:-1]
    for i in range(len(lines)):
        if device_dic[lines[i]] != 'device':
            del lines[i]
    print(lines)
    emulatornum = len(lines)
    return lines, emulatornum


def read(filename):  # 读取账号
    account_dic = {}
    fun_dic = {}
    fun_list = []
    pattern = re.compile('\\s*(.*?)[\\s-]+([^\\s-]+)[\\s-]*(.*)')
    with open(filename, 'r') as f:  # 注意！请把账号密码写在zhanghao.txt内
        for line in f:
            result = pattern.findall(line)
            if len(result) != 0:
                account, password, fun = result[0]
            else:
                continue
            account_dic[account] = password
            fun_dic[account] = fun
            fun_list.append(fun_dic[account])
    account_list = list(account_dic.keys())
    accountnum = len(account_list)
    return account_list, account_dic, accountnum, fun_list, fun_dic


def readauth(filename):  # 读取记有大号和会长账号的txt
    pattern3 = re.compile('\\s*(.*?)[\\s-]+([^\\s-]+)[\\s-]*([0-9]+)')
    pattern2 = re.compile('\\s*(.*?)[\\s-]+([^\\s-]+)')
    with open(filename, 'r') as f:  # 注意！请把大号和会长账号密码写在zhanghao.txt内
        line = f.readline()
        result = pattern3.findall(line)
        if len(result) != 0:
            account_boss, password_boss, UID = result[0]
        else:
            print("大号账号格式有误，请检查")
            exit(-1)
        line = f.readline()
        result = pattern2.findall(line)
        if len(result) != 0:
            account_1, password_1 = result[0]
        else:
            print("会长1账号格式有误，请检查")
            exit(-1)
        line = f.readline()
        result = pattern2.findall(line)
        if len(result) != 0:
            account_2, password_2 = result[0]
        else:
            print("会长2账号格式有误，请检查")
            exit(-1)
    return account_boss, password_boss, UID, account_1, password_1, account_2, password_2


def shuatu_auth(a, account, fun):  # 刷图总控制
    shuatu_dic = {
        '08': 'a.shuatu8()',
        '10': 'a.shuatu10()',
        '11': 'a.shuatu11()'
    }
    if len(fun) < 2:
        print("账号{}不刷图".format(account))
        return False
    tu_hao = fun[0:2]
    if tu_hao in shuatu_dic:
        # print("账号{}将刷{}图".format(account, tu_hao))
        # eval(shuatu_dic[tu_hao])
        return True
    else:
        print("账号{}的图号填写有误，请检查图号，图号应为两位数字，该账号将不刷图".format(account))
        return False


def run_party(filepath):
    # 读取账号
    account_list, account_dic, account_num, fun_list, fun_dic = read(filepath)
    # 多线程执行
    count = 0  # 完成账号数
    thread_list = []
    # 完整循环 join()方法确保完成后再进行下一次循环
    for i in range(int(account_num / emulatornum)):  # 完整循环 join()方法确保完成后再进行下一次循环
        for j in range(emulatornum):
            t = threading.Thread(target=run_main, args=(
                lines[j], account_list[i * emulatornum + j], account_dic[account_list[i * emulatornum + j]],
                fun_dic[account_list[i * emulatornum + j]]))
            thread_list.append(t)
            count += 1
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        thread_list = []
    # 剩余账号
    i = 0
    while count != account_num:
        t = threading.Thread(target=run_main,
                             args=(lines[i], account_list[count], account_dic[account_list[count]],
                                   fun_dic[account_list[count]]))
        thread_list.append(t)
        i += 1
        count += 1
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


# 主程序
if __name__ == '__main__':
    # 连接adb与uiautomator
    lines, emulatornum = connect()

    # 读取大号和会长账号
    account_boss, password_boss, UID, account_1, password_1, account_2, password_2 = readauth('config/admin.txt')

    # 执行一会刷mana
    run_party('config/party_1.txt')

    # 执行会长1的日常任务
    t = threading.Thread(target=run_main,
                         args=(lines[0], account_1, password_1, '11', 1))
    t.start()
    t.join()

    # 执行会长2的邀请大号任务
    t = threading.Thread(target=invitemain,
                         args=(lines[0], account_2, password_2, UID))
    t.start()
    t.join()

    # 执行大号的接受邀请任务
    t = threading.Thread(target=acceptmain,
                         args=(lines[0], account_boss, password_boss))
    t.start()
    t.join()

    # 执行二会刷mana
    run_party('config/party_2.txt')

    # 执行会长2的日常任务+踢出大号
    t = threading.Thread(target=run_main,
                         args=(lines[0], account_2, password_2, '', 1))
    t.start()
    t.join()
    # 执行会长1的邀请大号任务
    t = threading.Thread(target=invitemain,
                         args=(lines[0], account_1, password_1, UID))
    t.start()
    t.join()
    # 执行大号的接受邀请任务
    t = threading.Thread(target=acceptmain,
                         args=(lines[0], account_boss, password_boss))
    t.start()
    t.join()

    # 退出adb
    os.system('adb kill-server')
    os.system('echo -e "\a"')