import os
from pdfCropMargins import pdfCropMargins
import PyPDF2
import subprocess
from shutil import move
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def openfile():
 
    Dir = filedialog.askdirectory()
    path.set(Dir)
    

def dooo():
    
    bu1.config(state="disable") 
    text1.config(state="disable")
    ro.config(state="disable") 
    cr.config(state="disable")
    bu2.config(state="disable")

    if os.path.exists(text1.get())==False :
        messagebox.showinfo('提示','请选择文件夹')
        return

    rootDir = str(text1.get())
    ro_Flag = ro_state.get()
    cr_Flag = cr_state.get()

    if ro_Flag == False and cr_Flag == False:
        messagebox.showinfo('提示','您什么也没让我干呐！')
        return

    text_but.set("开始啦！")
    window.update()
    
    count_all = 0
    count_finish = 0
    for root,dirs,files in os.walk(rootDir):
        for filespath in files:
            if filespath.endswith(".pdf"):
                count_all = count_all + 1
    try:
        print(count_all)
        for root,dirs,files in os.walk(rootDir):
            for filespath in files:
                if filespath.endswith(".pdf"):
                    fullpath=os.path.join(root,filespath)
                    pdf_in = open(fullpath , 'rb')
                    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
                    pdf_writer = PyPDF2.PdfFileWriter()

                    input_file_path = fullpath
                    output_file_path = fullpath + "-rotated"

                    if ro_Flag:
                        input_file_path = fullpath + "-rotated"
                        for pagenum in range(pdf_reader.numPages):
                            page = pdf_reader.getPage(pagenum)
                            ro_deg = page.get('/Rotate')
                            if(ro_deg == None):
                                page_out = page.rotateCounterClockwise(90)
                            else:
                                page_out = page
                            pdf_writer.addPage(page_out) 
                        pdf_out = open(input_file_path, 'wb')
                        pdf_writer.write(pdf_out) 
                        pdf_out.close()
                        pdf_in.close()
                        
                    if cr_Flag:
                        output_file_path = fullpath + "-cropped"
                        sys.argv.clear()
                        args = ["", "-s", "-p", "0", "-pdl", "-o"]
                        args.append(output_file_path)
                        args.append(input_file_path)
                        sys.argv.extend(args)
                        print(sys.argv)
                        try:
                            pdfCropMargins.main()

                        except SystemExit:
                            exit_code = str(sys.exc_info()[1])
                            if '0' != exit_code:
                                print("pdfCropMargins exit: " + exit_code)
                                raise

                        print("Crop finish")
                        #subprocess.call("pdf-crop-margins -s -p 0 -pdl -o \"" + fullpath + "-cropped\" \"" + fullpath + "-rotated\"")
                        #subprocess.call("pdf-crop-margins -s -p 0 -pdl -o \"" + fullpath + "-cropped\" \"" + fullpath + "-rotated\"", shell=True )
                        #subprocess.call("pdf-crop-margins -s -p 0 -pdl -o \"" + fullpath + "-cropped\" \"" + fullpath + "\"")
                        #subprocess.call("pdf-crop-margins -s -p 0 -pdl -o \"" + fullpath + "-cropped\" \"" + fullpath + "\"", shell=True)
                        
                    if ro_Flag:
                        os.remove(input_file_path)
                        print("Remove " + input_file_path)

                    move(output_file_path, fullpath)

                    count_finish = count_finish + 1
                    print(count_finish)
                    text_now = "在努力啦!已完成" + str(count_finish) + "/" + str(count_all)
                    print(text_now)
                    text_but.set(text_now)
                    window.update()
                                
        text_but.set("完成")
        bu1.config(state="normal") 
        text1.config(state="normal")
        ro.config(state="normal") 
        cr.config(state="normal")
        bu2.config(state="normal")
        #text_but.set("处理下一个？")
    except:
        text_but.set("神秘事件发生...转化失败")
        import traceback
        max_traceback_length = 300
        traceback.print_tb(sys.exc_info()[2], limit=max_traceback_length)
    
    
    
    
    
window = Tk()
#window.iconbitmap("RandCPDF.ico")
path = StringVar()
window.title("PDF旋转、裁剪小程序")
window.resizable(width=False, height=False)
#window.geometry('350x200')

la1 = Label(window,text = "路径选择")
la1.grid(row = 0, column = 0)

text1 = Entry(window,width=30, textvariable = path)
text1.grid(row = 0, column = 1,columnspan=2)

bu1 = Button(window, text = "打开", command = openfile)
bu1.grid(row = 0, column = 3)


ro_state = BooleanVar()
ro_state.set(True) #set check state
ro = Checkbutton(window, text='自动旋转', var = ro_state)
ro.grid(column=0, row=2,columnspan=2)

cr_state = BooleanVar()
cr_state.set(True) #set check state
cr = Checkbutton(window, text='自动裁剪', var = cr_state)
cr.grid(column=2, row=2,columnspan=2)



bu2 = Button(window, text = "确定" , command = dooo)
bu2.grid(column=0,row=3,columnspan=4)

text_but = StringVar()
text_but.set("时刻准备开始")
whatdoing = Label(window,textvariable = text_but)
whatdoing.grid(column=0,columnspan=4,row=4)

tips = Label(window,text = "tips:\n使用前记得备份。\n出现问题请联系gaoymmail@gmail.com")
tips.grid(column=0,columnspan=4,row=5)

window.mainloop()







 








