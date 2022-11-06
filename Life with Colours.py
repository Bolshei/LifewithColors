from tkinter import *
from tkinter import filedialog
import cv2
import webcolors
import numpy as np


def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root = Tk()
root.title("Life with Colors")
center_window(500, 400)
bg = PhotoImage(file=r"palet.png")
canvas1 = Canvas( root, width=300, height=300)
canvas1.pack(fill="both", expand=True)
canvas1.create_image( 0, 0, image= bg, anchor="nw")
canvas1.create_text(260, 275, text = "Welcome")


def open_popup(color):
    top=Toplevel(root)
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    win_x = root_x -400
    win_y = root_y -200
    # top.geometry(f'+{win_x}+{win_y}')
    top.geometry("400x200")
    top.title("Color Found")
    # wheel=PhotoImage(r"C:\Users\fyene\Desktop\Color\wheel.png")
    label1=Label(top, text= "The Color is : " + str(color),font=("Caveat", 12))
    # label2=Label(top, image=wheel)
    label1.place(x=150,y=10)
    # label2.place(x=0,y=0)

def loaddialog():
    file=filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")], parent=root, title='Choose an image')
    print(file)
    img = cv2.imread(file)
    cv2.imshow('image', img)

    def closest_colour(requested_colour):
        min_colours = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            b_c, g_c, r_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]


    def closest_colour_onwheel(requested_colour):
        min_colour = 99999999
        min_colour_pos = [0, 0]
        img2 = cv2.imread("wheel.png")
        img2 = cv2.resize(img2, (400, 400))
        # print(requested_colour,img2[500,800])
        for i in range(len(img2[0])):
            for j in range(len(img2[1])):
                b_c, g_c, r_c = img2[i, j]
                rd = (int(r_c) - int(requested_colour[0])) ** 2
                gd = (g_c - requested_colour[1]) ** 2
                bd = (b_c - requested_colour[2]) ** 2
                if rd + gd + bd < min_colour:
                    min_colour = rd + gd + bd
                    min_colour_pos = [i, j]
        k=(min_colour_pos[0],min_colour_pos[1]) #name
        global l
        l=(requested_colour[0],requested_colour[1],requested_colour[2]) #rgb

        print(k)

        return k

    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb

    def click_event(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            # print(x, ' ', y)
            requested_colour = img[y, x]
            print(requested_colour)
            answer = closest_colour(requested_colour)
            # self.text_answer=answer
            print("The Color is : ", closest_colour(requested_colour),"Hexcode is:",requested_colour[0],requested_colour[1])
            # open_popup(closest_colour(requested_colour))
            # print(img[y,x])
            cv2.destroyAllWindows()
            # cv2.namedWindow("output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
            # im = cv2.imread("earth.jpg")  # Read image
            # imS = cv2.resize(im, (960, 540)
            img2 = cv2.imread(r"C:\Users\fyene\Desktop\Color\wheel.png")
            img2=cv2.resize(img2,(400,400))
            blank_image = np.zeros((400, 400,3), np.uint8)
            img2 = cv2.circle(img2, closest_colour_onwheel(requested_colour), 5, (0, 0, 0), 2)
            cv2.putText(blank_image, "Color : " + str(closest_colour(requested_colour)), (50, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, 2)
            cv2.putText(blank_image, "Hexcode : #"+str(rgb_to_hex(l)), (50, 200),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, 2)
            cv2.putText(blank_image, "RGB : " + str(l), (50, 300),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, 2)
            img3=np.concatenate((img2, blank_image), axis=1)
            # print(img2)
            # cv2.namedWindow("Color Wheel", cv2.WINDOW_NORMAL)
            # cv2.resizeWindow("Color Wheel", 800, 400)


            cv2.imshow('Color Wheel', img3)
            # cv2.waitKey(0)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)


button1 = Button(root, text="Exit", command=root.destroy)
button2 = Button(root, text="Load Image", command=loaddialog)
button1_canvas = canvas1.create_window(50, 330, anchor="nw", window=button1)
button2_canvas = canvas1.create_window(50, 300, anchor="nw", window=button2)

root.mainloop()