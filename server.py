from libs import WeChat

wx = WeChat()

# 发送消息
who = "文件传输助手"
for i in range(1):
    wx.SendMsg(f"wxauto测试{i+1}", who)


print("wxauto测试完成！")
