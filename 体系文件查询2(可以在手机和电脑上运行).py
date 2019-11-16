import itchat
from itchat.content import *
import os
import glob

MyFriendList = {}
myUserName = ""# 登录人员的动态username
myNickName = ""# 登录人员的昵称NickName
MyFileList = []# 文件列表

def auto_reply(msg,username):#自动回复信息
    global MyFileList
    # 显示下一页内容
    if "体系文件 下一页" in msg.text:
        if len(MyFileList) > 20:# 文件列表大于20个
            for i in range(1,20):
                itchat.send("体系文件 " + MyFileList[i-1], toUserName=username)
                MyFileList.pop(i-1)
            itchat.send("仅显示前20个文件，请扩大关键字再查找", toUserName=username)
            itchat.send("如需显示剩下的文件，请输入：体系文件 下一页", toUserName=username)
        else:
            for f in MyFileList:
                itchat.send("体系文件 " + f, toUserName=username)
                MyFileList.pop(MyFileList.index(f))
    # 显示查询内容
    if "体系文件 " in msg.text:#接收到的消息是否符合查询命令
        #接收信息，并开始查询对应文件
        itchat.send("您好，体系文件查询助手为您服务", toUserName=username)
        Search_String = msg.text.replace("体系文件 ", "") #取得查询字符串
        itchat.send("正在查询关键字为：{"+Search_String + "} 的文件，请稍后", toUserName=username)
        # PATH = r'/Download/MyPython/2019体系文件'
        PATH = os.getcwd() + '/2019体系文件'
        # PATH = os.getcwd() + '\\2019体系文件'
        file_list = []
        path_list = []
        for root,dirs,files in os.walk(PATH):# 在目录中查询
            # 如果查询的内容为完整文件，则直接发送对应文件
            if Search_String.find(".") > 0:
                file_pattern = os.path.join(root, '*' + Search_String)
            else: # 模糊查询
                file_pattern = os.path.join(root, '*' + Search_String + '*.*')
            # 取得符合关键字的文件列表
            for f in glob.glob(file_pattern):
                search_filename =  f.replace(root+"/","")
                # search_filename = f.replace(root + "\\", "")
                # print("root is: " + root)
                # print("search_filename is: " + search_filename)
                if not search_filename in file_list and not "~" in f:#不存在时则加入到列表中
                    file_list.append(f.replace(root+"/",""))
                    # file_list.append(f.replace(root + "\\", ""))
                    path_list.append(root)
        #根据文件列表长短判定是否为查询文件名
        if len(file_list) <= 0:
            itchat.send("未找到对应的文件，请缩小或更换关键字，再重新尝试", toUserName=username)
        elif len(file_list) > 1:#长度大于1，则提示选择对应文件
            MyFileList = file_list.copy()
            itchat.send("一共找出 %d 个文件"% len(file_list), toUserName=username)
            itchat.send("找出的文件如下：", toUserName=username)
            for f in file_list:
                if file_list.index(f)>20:
                    itchat.send("仅显示前20个文件，请扩大关键字再查找", toUserName=username)
                    itchat.send("如需显示剩下的文件，请输入：体系文件 下一页", toUserName=username)
                    break
                else:
                    Search_Filename = f#获得文件名
                    Search_FileRoot = path_list[file_list.index(f)]#获得对应的路径
                    itchat.send("体系文件 " + Search_Filename, toUserName=username)
                MyFileList.pop(MyFileList.index(f))  # 弹出已显示的文件
            itchat.send("请复制对应的文件名称，并重新发送即可", toUserName=username)
        else:#找到对应文件，则发送对应文件
            itchat.send("已查找到文件，文件正在传输中...", toUserName=username)
            Search_Filename = file_list[0] #获得文件名
            Search_FileRoot = path_list[0] #获得对应的路径
            itchat.send_file(Search_FileRoot + "/" + Search_Filename, toUserName=username)#发送文件
            # itchat.send_file(Search_FileRoot + "\\" + Search_Filename, toUserName=username)  # 发送文件

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
    if username != myUserName:
        auto_reply(msg, username)#根据命令执行对应信息

if __name__ == '__main__':
    # itchat.auto_login( enableCmdQR = True) # hotReload =True) #
    itchat.auto_login() # hotReload =True) #
    # 获取自己的UserName
    myFriends=itchat.get_friends(update=True)
    for i in range(len(myFriends)):
        # 获取所有联系人的动态username和昵称，并建立成字典
        MyFriendList[myFriends[i]["UserName"]] = myFriends[i]["NickName"]

    myUserName = myFriends[0]["UserName"]
    myNickName = myFriends[0]["NickName"]
    itchat.run()


# 处理多媒体类消息
# 包括图片、录音、文件、视频
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])

# 处理好友添加请求
# @itchat.msg_register(FRIENDS)
