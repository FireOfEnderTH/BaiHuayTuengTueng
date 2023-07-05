#debugging elements
from colorama import Fore
from colorama import init as color_init
color_init(convert=True)
def debugText(txt):
    print(Fore.LIGHTRED_EX + str(txt) + Fore.WHITE)

#main elements
from tkinter import *
from PIL import Image, ImageTk
from random import randint, seed
from math import *
from time import sleep, time
from threading import Thread
import pygame
pygame.init()
pygame.mixer.init()

#overall style configures
f_family = 'Mitr'
bg_color = '#21060f'

#create window
root = Tk()
root.title("ใบ้หวยตึงๆ")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

min_x = int(screen_width/3)
min_y = int(screen_height-(screen_height*0.2))
root.minsize(min_x,min_y)
root.maxsize(screen_width,screen_height)
root.resizable(width=False,height=False)
root.iconphoto(False,PhotoImage(file='icon.png'))

win_x = (screen_width/2) - (min_x/2)
win_y = (screen_height/2) - ((min_y+100)/2)

root.geometry('%dx%d+%d+%d' % (min_x,min_y,win_x,win_y))

root.config(bg=bg_color)

gif_canvas = Canvas(root,bg=bg_color,width=min_x,height=min_y)
gif_canvas.place(x=0,y=0)

head = Label(root,text="กดปุ่มเพื่อเสี่ยงโชค!",font=(f_family, int(min_y/18), 'bold'),fg='#fff9bf',bg=bg_color)
head.pack()
root.update()
head.place(x=(min_x/2)-(head.winfo_width()/2),y=(min_y*5/36)-(head.winfo_height()/2))

blessing = [" ~งวดนี้รวย~ "," ~สาธุเอาเด้อ~ "," ~เงินทองไหลมาเทมา~ "," ~หมานๆ เด้อ~ "," ~โชคดีมีชัย~ "]
bottom = Label(root,text=blessing[randint(0,len(blessing)-1)],font=(f_family, int(min_y/24), 'italic'),fg='#ffcf0d',bg=bg_color,anchor=CENTER)
bottom.pack()
root.update()
bottom.place(x=(min_x/2)-(bottom.winfo_width()/2),y=(min_y*32/36)-(bottom.winfo_height()/2))

slot_frame = Frame(root,bg=bg_color,width=int(min_x*6/10+(min_x/10)),height=int(min_x*3/20),bd=0,highlightthickness=0)
slot_frame.pack()
root.update()
slot_frame.place(x=(min_x/2)-(slot_frame.winfo_width()/2),y=(min_y*9/30)-(slot_frame.winfo_height()/2))

button_frame = Frame(root,bg=bg_color,width=int(min_x*3/5),height=int(min_x*2/5),bd=0,highlightthickness=0)
button_frame.pack()
root.update()
button_frame.place(x=(min_x/2)-(button_frame.winfo_width()/2),y=(min_y*33/60)-(button_frame.winfo_height()/2))

textbox = Entry(root,width=int(min_x*7/200),font=(f_family, int(min_y/32)),bg='#3b260d',fg='#fff9bf')
textbox.pack()
root.update()
textbox.place(x=(min_x/2)-(textbox.winfo_width()/2),y=(min_y*39/50)-(textbox.winfo_height()/2))

#create slots row
slot_enabled = ImageTk.PhotoImage(Image.open('assets/slot_enabled.png').resize((int(min_x/10),int(min_x*3/20)),Image.ANTIALIAS))
slot_disabled = ImageTk.PhotoImage(Image.open('assets/slot_disabled.png').resize((int(min_x/10),int(min_x*3/20)),Image.ANTIALIAS))

slot_list = {}
for i in range(6):
    s = Canvas(slot_frame,width=int(min_x/10),height=int(min_x*3/20),bg=bg_color,highlightthickness=0)
    s.grid(row=0,column=i,sticky=N+W,padx=int(min_x/120))
    bg = s.create_image(0,0,anchor=NW,image=slot_disabled,tags='Image')

    t = s.create_text(int(int(s['width'])/2),int(int(s['height'])/2),tags='Number',text='',font=(f_family, int(min_y/18)),fill='#261605')

    slot_list[f'slot{i}'] = s

#define functions
placeholder = 'ใส่ข้อความนำโชคซะสิ'
placeholder_color = '#d4c49f'
def click(*args):
    def forceFocus(event):
        if event.type == '2': #it's <Return> event
            root.focus()
        elif event.widget != textbox: #else it's a clicking event
            root.focus()
    if textbox.get() == placeholder and textbox['fg'] == placeholder_color:
        textbox.delete(0, 'end')
    textbox['fg'] = '#fff9bf'
    textbox.bind('<Return>', forceFocus)
    root.bind('<Button-1>', forceFocus)
def leave(*args):
    if textbox.get() == "":
        textbox.delete(0, 'end')
        textbox.insert(0, placeholder)
        textbox['fg'] = placeholder_color

leave() #put the placeholder
textbox.bind("<FocusIn>", click)
textbox.bind("<FocusOut>", leave)

animation_frames = []
for i in range(0, 79): #collect animation frames to the list
    image_path = f"assets/confetti/confetti_{'0'*(2-len(str(i)))}{i}.png"
    frame = ImageTk.PhotoImage(Image.open(image_path).resize((int(min_x),int(min_y))),Image.ANTIALIAS)
    animation_frames.append(frame)

def bomb(frame_index): #animation player after finished the randomization
    gif_canvas.delete("all")  #Clear the canvas

    #draw the current frame
    gif_canvas.create_image(0, 0, anchor=NW, image=animation_frames[frame_index])

    #schedule the next frame update
    if (frame_index + 1) % len(animation_frames) != 0:
        fps = 30
        root.after(int(1000/fps), bomb, (frame_index + 1) % len(animation_frames))

def soundPlayer(path,vol): #play audio file(s)
    sound = pygame.mixer.Sound(path)
    sound.set_volume(vol)
    return sound

def runNumber(digits): #randomize the number and return to the variable
    if textbox.get() != "" and textbox.get() != 'ใส่ข้อความนำโชคซะสิ':
        seed(textbox.get()) #get seed from textBox
    else:
        seed() #clear seed
    return str(randint(0,(10**digits)-1))

db = False #debounce, use to prevent functions from overlaping
def roll(digits, increasing): #main operation
    global db #call this variable from the global the the local function
    if not db:
        db = True
        overall_t = 0.7 #second(s) , time use per slot

        m = runNumber(digits)#get the randomized number

        #operate numbers revealing orders
        n = 0
        d = 1
        num = m + ('0'*(6-len(m)))
        if increasing: #True: from right, False: from left
            num = ('0'*(6-len(m))) + m
            n = 5 #start from max digits index
            d = -1 #else: from left, which have been set as you seen above

        for i in range(6): #set slots' images back to disable
            currentSlot = slot_list[f'slot{i}']
            currentSlot.itemconfig('Image',image=slot_disabled)
            currentSlot.itemconfig('Number',text='')
            currentSlot.itemconfig('Number',fill='#8a5d2d')
            if increasing:
                if i >= 6-digits:
                    currentSlot.itemconfig('Image',image=slot_enabled)
            else:
                if i <= digits-1:
                    currentSlot.itemconfig('Image',image=slot_enabled)

        def anim(currentSlot):
            fps = 14

            t = int((1/fps)*1000) #make it millisecond
            count = fps*overall_t

            seed() #clear see
            tick_sound = pygame.mixer.Sound('assets/tick.wav')
            tick_sound.set_volume(0.6)
            def changeNumber():
                currentSlot.itemconfig('Number',text=str(randint(0,9)))
                tick_sound.play()

            while count > 1:
                root.after(int(t*count), changeNumber)
                count -= 1

        def slotOperation(order):
            currentSlot = slot_list[f'slot{order}']

            def finishedAnim():
                currentSlot.itemconfig('Number',text=num[order])
                currentSlot.itemconfig('Number',fill='#261605')
                soundPlayer('assets/click.wav',1.4).play()

            anim(currentSlot) #get the character at 'order' index from randomized number
            root.after(int(overall_t*1000), finishedAnim)
        slotOperation(n)

        count = 0
        for i in range(n+d,abs(n-digits+1)+d,d):
            count += 1
            root.after(int(overall_t*1000)*(count), slotOperation, (i))#it uses millisecond

        def coffettiBomb():
            bomb(0)
            soundPlayer('assets/bomb.wav',0.7).play()
            global db
            db = False
            global buttons_list
            for i in range(len(buttons_list)):
                buttons_list[i].config(image=bt_normal)
        root.after(int(int(overall_t*1000)*(digits))+500, coffettiBomb)

#create buttons
bt_click = ImageTk.PhotoImage(Image.open('assets/button_click.png').resize((int(min_x*3/5),int(min_x*2/20)),Image.ANTIALIAS))
bt_disabled = ImageTk.PhotoImage(Image.open('assets/button_disabled.png').resize((int(min_x*3/5),int(min_x*2/20)),Image.ANTIALIAS))
bt_normal = ImageTk.PhotoImage(Image.open('assets/button_normal.png').resize((int(min_x*3/5),int(min_x*2/20)),Image.ANTIALIAS))
bt_hover = ImageTk.PhotoImage(Image.open('assets/button_hover.png').resize((int(min_x*3/5),int(min_x*2/20)),Image.ANTIALIAS))

buttons_list = [] #set the list to store buttons, to be called later
def button_clicked(event):
    if not db:
        event.widget.config(image=bt_click)
        if event.widget == buttons_list[0]:
            Thread(target=roll, args=(6,True)).start()
        elif event.widget == buttons_list[1]:
            Thread(target=roll, args=(3,True)).start()
        elif event.widget == buttons_list[2]:
            Thread(target=roll, args=(3,False)).start()
        else:
            Thread(target=roll, args=(2,True)).start()
        for i in range(len(buttons_list)):
            if event.widget != buttons_list[i]:
                buttons_list[i].config(image=bt_disabled)
        soundPlayer('assets/button.wav',0.4).play()
                
def button_hovered(event):
    if not db:
        event.widget.config(image=bt_hover)

def button_left(event):
    if not db:
        event.widget.config(image=bt_normal)

for i in range(0,4):
    if i == 0:
        txt = "รางวัลที่ 1"
    elif i == 1:
        txt = "เลขท้าย 3 ตัว"
    elif i == 2:
        txt = "เลขหน้า 3 ตัว"
    else:
        txt = "เลขท้าย 2 ตัว"
    button = Button(button_frame,bg=bg_color,width=int(min_x*3/5),height=int(min_x*2/20),image=bt_normal,highlightthickness=0,bd=0,activebackground=bg_color,compound=CENTER,text=txt,font=(f_family, int(min_y/40)),activeforeground='#1f1402',fg='#1f1402')
    button.grid(row=i,column=0,sticky=W+E+N+S)
    buttons_list.append(button)
    button.bind("<Button-1>", button_clicked)
    button.bind("<Enter>", button_hovered)
    button.bind("<Leave>", button_left)

changed = False
decay = 0.8
def useless():
    global changed
    global decay
    if not changed:
        bottom.config(text=f" -{bottom['text'][2:-2]}- ",font=(f_family, int(min_y/26), 'italic'))
    else:
        bottom.config(text=f" ~{bottom['text'][2:-2]}~ ",font=(f_family, int(min_y/24), 'italic'))
    changed = not changed #Swap bool value
    root.update()
    bottom.place(x=(min_x/2)-(bottom.winfo_width()/2),y=(min_y*32/36)-(bottom.winfo_height()/2))
    root.after(int(decay*1000),useless)

if __name__ == "__main__": #check if it's the main file running
    soundPlayer('bgm.mp3',0.5).play(-1)
    root.after(int(decay*1000),useless)
    root.mainloop()