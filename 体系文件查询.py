import itchat
from itchat.content import *
import os
import glob
import re
import urllib.request

def auto_reply(msg,username):#自动回复信息
    if "体系文件 " in msg.text:#接收到的消息是否符合查询命令
        #接收信息，并开始查询对应文件
        file_Suffix = ".pdf"#查询文件的后缀名
        itchat.send("您好，体系文件查询助手为您服务", toUserName=username)
        Search_String = msg.text.replace("体系文件 ", "") #取得查询字符串
        # if Search_String.find(".pdf") > 0:#判断发送的信息是否包含后缀名，如有后缀名，则替换后缀名
        #     Search_String = Search_String.replace(".pdf", "")  # 替换后缀名
        # elif Search_String.find(".") > 0:#查询文件不是.pdf文件时，则退出
        #     itchat.send("您好，仅能查询pdf文件，请重试", toUserName=username)
        #     return
        itchat.send("正在查询关键字为：{"+Search_String + "} 的文件，请稍后", toUserName=username)
        # PATH = r'G:\京山轻机工作文档\2019桌面\质量体系\新建文件夹\体系文件'
        PATH = r'G:\京山轻机工作文档'
        file_list = []
        path_list = []
        for root,dirs,files in os.walk(PATH):
            # file_pattern = os.path.join(root,'*' + Search_String + '*' + file_Suffix)
            if Search_String.find(".") > 0:
                file_pattern = os.path.join(root, '*' + Search_String)
            else:
                file_pattern = os.path.join(root, '*' + Search_String + '*.*')

            for f in glob.glob(file_pattern):
                # Search_Filename = f.replace(root+"\\","")
                if not f.replace(root+"\\","") in file_list and not "~" in f:#不存在时则加入到列表中
                    file_list.append(f.replace(root+"\\",""))
                    path_list.append(root)
        #根据文件列表长短判定是否为查询文件名
        if len(file_list) <= 0:
            itchat.send("未找到对应的文件，请缩小或更换关键字，再重新尝试", toUserName=username)
        elif len(file_list) > 1:#长度大于1，则提示选择对应文件
            itchat.send("一共找出 %d 个文件"% len(file_list), toUserName=username)
            itchat.send("找出的文件如下：", toUserName=username)
            for f in file_list:
                if file_list.index(f)>20:
                    itchat.send("仅显示前20个文件，请扩大关键字再查找", toUserName=username)
                    break
                else:
                    Search_Filename = f#获得文件名
                    Search_FileRoot = path_list[file_list.index(f)]#获得对应的路径
                    itchat.send("体系文件 " + Search_Filename, toUserName=username)
            itchat.send("请复制对应的文件名称，并重新发送即可", toUserName=username)
        else:#找到对应文件，则发送对应文件
            itchat.send("已查找到文件，文件正在传输中...", toUserName=username)
            Search_Filename = file_list[0] #获得文件名
            Search_FileRoot = path_list[0] #获得对应的路径
            itchat.send_file(Search_FileRoot + "\\" + Search_Filename, toUserName=username)#发送文件

# 处理群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def group_reply(msg):
    gname = "体系文件测试"#设置处理消息的群名
    # 获取消息房间名
    username = ""
    myroom = itchat.get_chatrooms(update=True)
    for room in myroom:
        if room['NickName'] == gname:
            username = room['UserName']

    auto_reply(msg,username)#根据命令执行对应信息
    # itchat.send_msg("测试信息", username)#发送群消息##

# 处理文本类消息
# 包括文本、位置、名片、通知、分享
@itchat.msg_register(TEXT)
def friend_reply(msg):
    username=msg['FromUserName']#获取发送人的名字
    auto_reply(msg, username)#根据命令执行对应信息

    # if "体系文件 " in msg.text:#接收到的消息是否符合查询命令
    #     #接收信息，并开始查询对应文件
    #     file_Suffix = ".pdf"#查询文件的后缀名
    #     itchat.send("您好，体系文件查询助手为您服务", toUserName=msg['FromUserName'])
    #     Search_String = msg.text.replace("体系文件 ", "") #取得查询字符串
    #     if Search_String.find(".pdf") > 0:#判断发送的信息是否包含后缀名，如有后缀名，则替换后缀名
    #         Search_String = Search_String.replace(".pdf", "")  # 替换后缀名
    #     elif Search_String.find(".") > 0:#查询文件不是.pdf文件时，则退出
    #         itchat.send("您好，仅能查询pdf文件，请重试", toUserName=msg['FromUserName'])
    #         return
    #     itchat.send("正在查询关键字为：{"+Search_String + "} 的文件，请稍后", toUserName=msg['FromUserName'])
    #     PATH = r'G:\京山轻机工作文档\2019桌面\质量体系\新建文件夹\体系文件'
    #     file_list = []
    #     path_list = []
    #     for root,dirs,files in os.walk(PATH):
    #         file_pattern = os.path.join(root,'*' + Search_String + '*' + file_Suffix)
    #         for f in glob.glob(file_pattern):
    #             # Search_Filename = f.replace(root+"\\","")
    #             file_list.append(f.replace(root+"\\",""))
    #             path_list.append(root)
    #     #根据文件列表长短判定是否为查询文件名
    #     if len(file_list) <= 0:
    #         itchat.send("未找到对应的文件，请缩小或更换关键字，再重新尝试", toUserName=msg['FromUserName'])
    #     elif len(file_list) > 1:#长度大于1，则提示选择对应文件
    #         itchat.send("一共找出 %d 个文件"% len(file_list), toUserName=msg['FromUserName'])
    #         itchat.send("找出的文件如下：", toUserName=msg['FromUserName'])
    #         for f in file_list:
    #             Search_Filename = f#获得文件名
    #             Search_FileRoot = path_list[file_list.index(f)]#获得对应的路径
    #             itchat.send("体系文件 " + Search_Filename, toUserName=msg['FromUserName'])
    #         itchat.send("请复制对应的文件名称，并重新发送即可", toUserName=msg['FromUserName'])
    #     else:#找到对应文件，则发送对应文件
    #         itchat.send("已查找到文件，文件正在传输中...", toUserName=msg['FromUserName'])
    #         Search_Filename = file_list[0] #获得文件名
    #         Search_FileRoot = path_list[0] #获得对应的路径
    #         itchat.send_file(Search_FileRoot + "\\" + Search_Filename, toUserName=msg['FromUserName'])#发送文件


if __name__ == '__main__':
    itchat.auto_login()
    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["NickName"]
    itchat.run()


# 处理多媒体类消息
# 包括图片、录音、文件、视频
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])

# 处理好友添加请求
# @itchat.msg_register(FRIENDS)
