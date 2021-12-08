from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import cv2, os, shutil, numpy as np

root = Tk()
window_width = 700
window_height = 700
root.geometry(f'{window_width}x{window_height}+750+10')
root.title("ReTouch")


def open():
    global filepath, openedimage, previmage, currentimage
    filepath = filedialog.askopenfilename(title="Open Image", filetypes=[('Images',"*.png *.jpg *.jpeg")])
    openedimage = ImageTk.PhotoImage(Image.open(filepath).resize((int(window_width*3.2/4),int(window_height)),Image.ANTIALIAS))
    imagelabel.config(image=openedimage)
    sidebar.grid(row=0,column=0)
    imagelabel.grid(row=0,column=1)
    previmage = openedimage
    currentimage = openedimage
    try: 
        os.mkdir(tempdir) 
    except OSError as error: 
        print(error)  

def save():
    global currentimage, display
    filesave = filedialog.asksaveasfilename(title="Save Image", filetypes=[('Images',"*.png *.jpg *.jpeg")], initialfile='ReTouch.jpg')
    if display ==1 :
        saveimage = cv2.imread(tempfilepath1)
    else:
        saveimage = cv2.imread(tempfilepath2)
    cv2.imwrite(filesave,saveimage)

def update():
    editupdate = ImageTk.PhotoImage(Image.open(tempfilepath1).resize((int(window_width*3.2/4),int(window_height)),Image.ANTIALIAS))
    imagelabel.config(image=editupdate)
    imagelabel.image=editupdate
    global previmage,currentimage, display
    previmage = currentimage
    currentimage = editupdate
    display = 1

def undo():
    global previmage,currentimage
    imagelabel.config(image=previmage)
    imagelabel.image=previmage
    currentimage = previmage
    global display
    display = 0

def end():
    try:
        shutil.rmtree(tempdir)
    except:
        pass
    quit()

def updatingtemp2(edit):
    try:
        cv2.imwrite(tempfilepath2,cv2.imread(tempfilepath1))
    except:
        cv2.imwrite(tempfilepath2,edit)

def grayscale():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # Logic
    edit = cv2.cvtColor(edit,cv2.COLOR_BGR2GRAY)
    # Logic
    cv2.imwrite(tempfilepath1,edit)
    update()

def sharp():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # logic
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    edit = cv2.filter2D(edit, -1, kernel)
    # logic
    cv2.imwrite(tempfilepath1,edit)
    update()

def sepia():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    img_sepia = np.array(edit, dtype=np.float64) # converting to float to prevent loss
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
    img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
    edit = np.array(img_sepia, dtype=np.uint8)
    cv2.imwrite(tempfilepath1,edit)
    update()

def blurscale():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # Logic part here
    figure_size = 9
    edit = cv2.blur(edit,(figure_size, figure_size))
    # Logic part here
    cv2.imwrite(tempfilepath1,edit)
    update()    

def medianblurscale():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # Logic part here
    edit = cv2.medianBlur(edit,5)
    # Logic part here
    cv2.imwrite(tempfilepath1,edit)
    update()        

def convolutionscale():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # Logic part here
    kernel = np.ones((5,5),np.float32)/25
    edit = cv2.filter2D(edit,-1,kernel)
    # Logic part here
    cv2.imwrite(tempfilepath1,edit)
    update()    

def clockwisescale():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # Logic part here
    edit = cv2.rotate(edit, cv2.cv2.ROTATE_90_CLOCKWISE)
    # Logic part here
    cv2.imwrite(tempfilepath1,edit)
    update()     

def invertvertically():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # Logic part here
    edit = cv2.rotate(edit, cv2.ROTATE_180)
    # Logic part here
    cv2.imwrite(tempfilepath1,edit)
    update()         

def sketch():
    global filepath
    edit = cv2.imread(filepath)
    updatingtemp2(edit)
    # Logic
    grey_img=cv2.cvtColor(edit, cv2.COLOR_BGR2GRAY)
    invert_img=cv2.bitwise_not(grey_img)
    blur_img=cv2.GaussianBlur(invert_img, (111,111),0)
    invblur_img=cv2.bitwise_not(blur_img)
    edit=cv2.divide(grey_img,invblur_img, scale=256.0)
    # Logic
    cv2.imwrite(tempfilepath1,edit)
    update()

def remove():
    global w1,w2,w3,w4,w5
    try:
        w1.grid_remove()
        w2.grid_remove()
        w3.grid_remove()
        w4.grid_remove()
        w5.grid_remove()
    except:
        pass

def filters():
    global w1,w2,w3,w4,w5
    remove()
    w1=Button(sidebar,text="Gray Scale",width=int(window_width/32),command=grayscale)
    w1.grid(row=1,column=0)
    w2=Button(sidebar,text="Sharpen",width=int(window_width/32),command=sharp)
    w2.grid(row=2,column=0)
    w3=Button(sidebar,text="Sepia",width=int(window_width/32),command=sepia)
    w3.grid(row=3,column=0)
    w4=Button(sidebar,text="Sketch",width=int(window_width/32),command=sketch)
    w4.grid(row=4,column=0)
    w5=Button(sidebar,text="Undo",width=int(window_width/32),command=undo)
    w5.grid(row=5,column=0)

def blurs():
    global w1,w2,w3,w4,w5
    remove()
    w1=Button(sidebar,text="Blur",width=int(window_width/32),command=blurscale)
    w1.grid(row=1,column=0)
    w2=Button(sidebar,text="Median Blur",width=int(window_width/32),command=medianblurscale)
    w2.grid(row=2,column=0)
    w3=Button(sidebar,text="Convultion",width=int(window_width/32),command=convolutionscale)
    w3.grid(row=3,column=0)
    w4=Button(sidebar,text="Undo",width=int(window_width/32),command=undo)
    w4.grid(row=4,column=0)
    # Button(sidebar,text="Clockwise Scale",width=int(window_width/32),command=clockwisescale).grid(row=7,column=0)

menubar = Menu(root)    
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open',command=open)
filemenu.add_command(label='Save',command=save)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=end)
menubar.add_cascade(label='File', menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label='Filters',command=filters)
editmenu.add_command(label='Blurs',command=blurs)
menubar.add_cascade(label='Edit', menu=editmenu)
root.config(menu=menubar)

tempdir = 'C:/Users/Public/Temp'
tempfilepath1 = 'C:/Users/Public/Temp/temp1.jpg'
tempfilepath2 = 'C:/Users/Public/Temp/temp2.jpg'
display = 0
w1=w2=w3=w4=w5=0
sidebar = Frame()
imagelabel = Label()

Label(sidebar,text="",width=int(window_width/32)).grid(row=1,column=0)


# Button(sidebar,text="Redo",width=int(window_width/32),command=redo).grid(row=3,column=0)
root.protocol("WM_DELETE_WINDOW", end)
root.mainloop()
