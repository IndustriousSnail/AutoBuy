from tkinter import *  # 导入 Tkinter 库

from log import log


class GUI(object):

    def __init__(self):
        root = Tk()  # 创建窗口对象的背景色
        root.geometry('600x400')
        # # 创建两个列表
        # li = ['C', 'python', 'php', 'html', 'SQL', 'java']
        # movie = ['CSS', 'jQuery', 'Bootstrap']
        # listb = Listbox(root)  # 创建两个列表组件
        # listb2 = Listbox(root)
        # for item in li:  # 第一个小部件插入数据
        #     listb.insert(0, item)
        #
        # for item in movie:  # 第二个小部件插入数据
        #     listb2.insert(0, item)
        #
        # listb.pack()  # 将小部件放置到主窗口中
        # listb2.pack()

        def cmd():
            log.debug("点击了登陆按钮")

        login_button = Button(root, text='登陆', width=20, height=6, command=cmd)
        login_button.place(x=290, y=197)
        login_button.pack()

        root.mainloop()  # 进入消息循环


if __name__ == '__main__':
    GUI()
