import glob
import json
import logging
import os
import re
import time
import tkinter as tk
import tkinter.messagebox

window = tk.Tk()

window.title("Demo APP")

width = 640
height = 730

# 设置窗口适应属性
window.resizable(width=False, height=False)
window.attributes("-alpha",0.7)
window.attributes('-toolwindow', False, 
                '-alpha', 1, 
                '-fullscreen', False, 
                '-topmost', True)
# window.overrideredirect(True)  

# 获取当前屏幕分辨率
screenwidth = window.winfo_screenwidth()  
screenheight = window.winfo_screenheight() 

# 根据分辨率设置窗口大小
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/1, (screenheight-height)/5)
window.geometry(alignstr)

# ----frame-----
frame_main1 = tk.Frame(window, bg = "#F2F2F2", height=100, width=360)
frame_main1.grid(column=1,row=1,padx=10,pady=10)

frame_main2 = tk.Frame(window, bg = "#F2F2F2", height=100, width=400)
frame_main2.grid(column=2,row=1)

frame_main3 = tk.Frame(window, bg = "#F2F2F2", height=200, width=370)
frame_main3.grid(column=1,row=2)

frame_main4 = tk.Frame(window, bg ="#F2F2F2", height=200, width=360)
frame_main4.grid(column=2,row=2)

frame_main5 = tk.Frame(window, bg = "#F2F2F2", height=300, width=720)
frame_main5.grid(column=1,row=3,columnspan=2,padx=15,pady=15)

# -----menu菜单功能，暂时不要后续添加--------
# meun_main = tk.Menu()
# # meun_main.grid()
# filemenu = tk.Menu(meun_main, tearoff=1)
# meun_main.add_cascade(label='File', menu=filemenu)
# filemenu.add_command(label='Monkey')
# filemenu.add_command(label='Screen')
# filemenu.add_command(label='Instructions')
# filemenu.add_command(label='About')
# window.config(menu = filemenu)

# -------Log缓存区域，显示自定义日志--------
lable_log=tk.Label(frame_main5,text="日志区",font = ("微软雅黑",14))
lable_log.grid(column=1,row=1)

text_log = tk.Text(frame_main5,bg="#5B5B5B",fg="#FFFFFF")
text_log.grid(column=1,row=2)


def clear_log():
    text_log.delete("1.0","end")

button_clearLog = tk.Button(frame_main5,text="Clear",font = ("微软雅黑",8),bg="#836FFF", fg= "#FFFFFF",command=clear_log)
button_clearLog.grid(column=2,row=2,sticky="n")

# text_log.insert("end","adasd21dadd")


# ------主页lable显示引导---------------
# 刷新设备说明
lable_main1 = tk.Label(frame_main1, justify="left", height=5, width=35, bg="#E5E5E5", font = ("微软雅黑",10), text="准备工作：\n1.进入开发者选项打开测试机USB调试功能\n2.点击刷新设备\n3.手机端确认USB调试（若未提示则跳过此步骤）\n4.设备连接成功")
lable_main1.grid()
# monkey参数说明
lable_main2 = tk.Label(frame_main2, justify="left", height=5, width=40, bg="#E5E5E5", font = ("微软雅黑",10), text="参数说明：\n1.Package：包名，可点击获取，也可以手动输入\n2.Seeds：随机值，默认取当天日期，也可手动输入\n3.Throttle：点击频率，默认300ms，可手动输入\n4.Count：总操作数，默认50万，可手动修改")
lable_main2.grid()

# ----listbox用于显示当前设备列表-----
lb = tk.Listbox(frame_main3,height=9, width=28, bg="#CDCDB4", fg="#551A8B")
lb.grid(column=0,row=0,padx=10,pady=10)


# -----frame4上的参数配置-----
lab1 = tk.Label(frame_main4,text="配置项",bg="#F2F2F2",font=(11))
lab2 = tk.Label(frame_main4,text="Package",bg="#F2F2F2" )
lab3 = tk.Label(frame_main4,text="Seeds",bg="#F2F2F2" )
lab4 = tk.Label(frame_main4,text="Throttle",bg="#F2F2F2" )
lab5 = tk.Label(frame_main4,text="Count",bg="#F2F2F2" )
lab6 = tk.Label(frame_main4,text="参数",bg="#F2F2F2",font=(11) )  #第二列标题哦


lab1.grid(column=1,row=1,padx=5,pady=5)
lab2.grid(column=1,row=2,padx=5,pady=5,sticky="w")
lab3.grid(column=1,row=3,padx=5,pady=5,sticky="w")
lab4.grid(column=1,row=4,padx=5,pady=5,sticky="w")
lab5.grid(column=1,row=5,padx=5,pady=5,sticky="w")
lab6.grid(column=2,row=1,padx=1,pady=1)


# -----entry monkey参数配置-------
entry1 = tk.Entry(frame_main4)
entry2 = tk.Entry(frame_main4)
entry3 = tk.Entry(frame_main4)
entry4 = tk.Entry(frame_main4)

entry1.grid(column=2,row=2,padx=5,pady=1,sticky="w")
entry2.grid(column=2,row=3,padx=5,pady=1,sticky="w")
entry3.grid(column=2,row=4,padx=5,pady=1,sticky="w")
entry4.grid(column=2,row=5,padx=5,pady=1,sticky="w")


# ------一些可能用到的全局变量------
select_var = ""
pkg_details = ""
button_state = ""
model_name = ""
# 创建一个空list存储设备
list_device = []
# monkey配置残水
p = ""
s = ""
t = ""
c = ""

def find_and_init():
    # def find_devices():
    global list_device,model_name
    list_device.clear()
    logging.basicConfig(level=logging.INFO)
    d_lists = os.popen("adb devices").readlines()
    logging.error(d_lists)
    d_lists.remove(d_lists[len(d_lists)-1])
    d_lists.remove(d_lists[0])
    lb.delete("0","end")
    logging.info(d_lists)
    # time.sleep(3)
    if len(d_lists)==0:
        lb.insert("end","未检测到设备，请连接测试机...")
        text_log.insert("end","未检测到设备，请连接测试机...\n")
        text_log.yview_moveto(1)
        text_log.update()
    elif "unauthorized" in d_lists[0]:
        lb.insert("end","请在手机上点击允许USB调试...")
        text_log.insert("end","请在手机上点击允许USB调试...\n")
        text_log.yview_moveto(1)
        text_log.update()
    else:
        
        text_log.insert("end","设备已连接，请选择设备进行后续操作！\n\n")
        text_log.yview_moveto(1)
        text_log.update()
        for i in d_lists:
            reg_serial = re.findall("(.*?)device", i)
            model_org = os.popen("adb -s "+str(reg_serial[0])+" shell getprop ro.product.model").readlines()
            logging.info(reg_serial[0].replace("\t","")+"："+model_org[0].replace("\n",""))

            # 将设备信息添加到listbox中
            per_list = reg_serial[0].replace("\t","")
            print("设备列表为：",per_list)
            os.system("adb -s "+str(per_list)+" logcat -c")
            lb.insert("end",model_org[0].replace("\n","").replace(" ","")+"："+per_list)
            model_name = model_org[0].replace("\n","").replace(" ","")
            list_device.append(per_list)


# ------读写配置文件-----------
    # def init_config():
    entry1.delete(0,"end")
    entry2.delete(0,"end")
    entry3.delete(0,"end")
    entry4.delete(0,"end")
    # time.sleep(3)
    if os.path.exists("config.json"):
        with open('config.json',encoding="utf-8") as ff:
            json_data = json.load(ff)
            entry1.insert("end",json_data["pkg"])
            entry2.insert("end", time.strftime("%Y%m%d%H%M%S", time.localtime())[2:8])
            entry3.insert("end", json_data["thr"])
            entry4.insert("end", json_data["total"])
            
    else:
        config_file = open('config.json','w',encoding='utf-8')
        # json_data = {"pkg":"请在此处填写包名...","sd":time.strftime("%Y%m%d%H%M%S", time.localtime())[2:8],"thr":"300","total":"500000"}
        json_data = {"pkg":"请在此处填写包名...", "thr":"300","total":"500000"}
        json.dump(json_data,config_file,ensure_ascii=False)
        config_file.close()

    # p=entry1.get()
    # s=entry2.get()
    # t=entry3.get()
    # c=entry4.get()

#  -----------按钮事件--------
# 刷新设备按钮
button = tk.Button(frame_main3,text="刷新设备",font = ("微软雅黑",15),bg="#8FBC8F", fg= "#FFFFFF", command=find_and_init)
button.grid(column=0,row=1)


# --------获取当前包名---------
def get_pkg():
    global select_var
    global pkg_details
    logging.info(select_var)
    # global select_var
    selected=lb.get(lb.curselection())

    print("我也不知道这里会不会报错 ",selected)

    print("原始的",selected,type(selected))
    reg_device=".*?：(.*)"
    select_device = re.findall(reg_device, selected)
    print("选择的设备是",select_device[0])
    select_var=select_device[0]
    
    try:
        cur = os.popen("adb -s "+str(select_var)+" shell dumpsys window | findstr mCurrentFocus").readline()
        result=re.findall("mCurrentFocus=Window{.*?u0 (.*?)/.*?}", cur)
        pkg_details = result[0]
        logging.info(cur)

    except IndexError:
        entry1.delete(0,"end")
        entry1.insert("end","获取失败...")
        tk.messagebox.showerror("Error了吧，哈哈哈！","请注意：\n  1.确认设备已经连接。\n  2.需要获取包名的应用处于前台状态！")
        entry1.delete(0,"end")
        entry1.insert("end","点击重试...")

    except TypeError:
        entry1.delete(0,"end")
        entry1.insert("end","未选择设备哦！")
        tk.messagebox.showerror("Error，这个不是Bug...","没有选择设备哦！")
        entry1.delete(0,"end")
        entry1.insert("end","点击重试...")


    else:
        
        entry1.delete(0,"end")
        entry1.insert("end",pkg_details)
        text_log.insert("end","获取包名成功！！！\n\n")
        text_log.yview_moveto(1)
        text_log.update()

def run_monkey():

    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())[4:12]

    if not os.path.exists("./Result/"+str(now_time)):
        text_log.insert("end","创建必要资源文件夹....\n\n")
        text_log.yview_moveto(1)
        text_log.update()
        os.makedirs("./Result/"+str(now_time))

    if not os.path.exists("./script/"+str(now_time)):
        text_log.insert("end","创建必要资源文件夹....\n\n")
        text_log.yview_moveto(1)
        text_log.update()
        os.makedirs("./script/"+str(now_time))
    global p,s,t,c
    p=entry1.get()
    s=entry2.get()
    t=entry3.get()
    c=entry4.get()

    global button_state
    button_state = "disabled"
    print(pkg_details)
    text_log.insert("end","即将开始初始化资源，请稍等...\n")
    if len(list_device)>0:

        if entry1.get() in (u"请在此处填写包名...",""):
            tk.messagebox.showerror("你又错了！！！","不出意外的话你包名肯定不对！！")

        else:

            for d in list_device:
                bat_monkey = str(d[:8])+"_monkey_"+str(pkg_details)+".bat"
                with open ("script\\"+str(now_time)+"\\"+bat_monkey, "w") as f:
                    text_log.insert("end","生成"+str(d)+"---monkey脚本...\n")
                    text_log.yview_moveto(1)
                    text_log.update()
                    f.write('@echo off\necho start  monkey test\ntitle Monkey\nadb -s '+str(d)+' shell monkey -s '+str(s)+' -p '+str(p)+' --throttle '+str(t)+' --ignore-crashes --ignore-native-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v -v '+str(c)+' > ./Result/'+str(now_time)+'/'+str(d[:8])+'_monkey.log')
                bat_fc = str(d[:8])+"_fc_"+str(pkg_details)+".bat"
                with open ("script\\"+str(now_time)+"\\"+bat_fc, "w") as ff:
                    text_log.insert("end","生成"+str(d)+"---crash监控脚本...\n")
                    text_log.yview_moveto(1)
                    text_log.update()
                    ff.write('@echo off\necho Start collecting crash logs\ntitle Crash\nadb -s '+str(d)+' logcat -s AndroidRuntime > ./Result/'+str(now_time)+'/'+str(d[:8])+'_crash.log')
                bat_memory = str(d[:8])+"_memory_"+str(pkg_details)+".bat"
                with open ("script\\"+str(now_time)+"\\"+bat_memory, "w") as fff:
                    text_log.insert("end","生成"+str(d)+"---内存监控脚本...\n\n")
                    text_log.yview_moveto(1)
                    text_log.update()
                    fff.write('@echo off\necho Start collecting memory logs\ntitle Memory\n:memory\nadb -s '+str(d)+' shell dumpsys meminfo '+str(p)+' | findstr TOTAL: > ./Result/'+str(now_time)+'/'+str(d[:8])+'_memory.log\nping -n 30 127.0.0.1>nul\ngoto memory')
            
            bat_finally = glob.glob("script\\"+str(now_time)+"\\*.bat")
            print("最终的bat有",bat_finally)
            time.sleep(2)
            text_log.insert("end","一切准备就绪，即将启动所有骚操作！！！\n\n")
            text_log.yview_moveto(1)
            text_log.update()

            text_log.insert("end","\n包名："+p)
            text_log.insert("end","\nseeds值："+s)
            text_log.insert("end","\nthrottle值："+t)
            text_log.insert("end","\n总测试数："+c)
            
            for gogo in bat_finally:
                os.system("start "+gogo)
                time.sleep(1)
    else:
        # len(list_device)==0:
        tk.messagebox.showerror("你又错了！！！","请注意：\n  1.确认设备已经连接。\n  2.确认包名不为空！！")

# 获取包名按钮
button_getpkg = tk.Button(frame_main4,text="获取包名", fg= "#FFFFFF",font = ("",9),bg="#8FBC8F",command=get_pkg)
button_getpkg.grid(column=3,row=2,padx=5,pady=5,sticky="w")
notice_lable = tk.Label(frame_main4,text="获取包名前，\n先选择设备。", justify="left",fg="red")
notice_lable.grid(column=3,row=3)

button_make_res = tk.Button()

# Monkey启动按钮
if button_state == "disabled":
    button_runmonkey = tk.Button(frame_main4,text="Run!!!",state="disabled", fg= "#FFFFFF",font = ("微软雅黑",15),bg="#8FBC8F",command=run_monkey)
    button_runmonkey.grid(column=2,row=7,padx=25,pady=5,sticky="w")
else:
    button_runmonkey = tk.Button(frame_main4,text="Run!!!", fg= "#FFFFFF",font = ("微软雅黑",15),bg="#8FBC8F",command=run_monkey)
    button_runmonkey.grid(column=2,row=7,padx=25,pady=5,sticky="w")
    button_state = "disabled"

window.mainloop()
