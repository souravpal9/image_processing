import math
import cv2
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import *
def Ratio(height, width):
    # Find the GCD of the numerator and denominator
    gcd = math.gcd(height, width)
    global lowest_height
    global lowest_width
    # Divide both numerator and denominator by the GCD to simplify the fraction
    lowest_height = height // gcd
    lowest_width = width // gcd
    
    return lowest_height, lowest_width


def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global img
        global height,width
        img = cv2.imread(file_path)

        # Get the height and width of the image
        height, width, _ = img.shape
        print(img.shape)
        
        lowest_height, lowest_width = Ratio(height, width) 


        if height <= 720 and width <= 1080:
            if lowest_height<=5 and lowest_width<=5:
                img =cv2.resize(img,(width,height))
            else :
                 img =cv2.resize(img,(width,height))
        
        elif height <=1080 and width <=1980:
            height = lowest_height*50
            width = lowest_width*50
            img =cv2.resize(img,(width,height))
        
        elif lowest_height<6 and lowest_width<6:
            height = lowest_height*200
            width = lowest_width*200
            img =cv2.resize(img,(width,height))
        
        elif lowest_height<10 and lowest_width<17:
            height = lowest_height*50
            width = lowest_width*50
            img =cv2.resize(img,(width,height))

        elif lowest_height >100 and lowest_width >100:
            height = lowest_height
            width = lowest_width
            img =cv2.resize(img,(width,height))
        else:
            height = lowest_height*40
            width = lowest_width*40
            img =cv2.resize(img,(width,height))

        cv2.imshow("image", img)
    print (img.shape)

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    global b, g, r, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        detect_color()


# Reading csv file with pandas lib. and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname



def detect_color():
    global clicked, img_copy
    if clicked:
        # Create a copy of the image to update
        img_copy = img.copy()

        if width <=500:
            fontscale = 0.6
        else :
            fontscale = 0.8

        # (image,start point , end point , color, thickness ) -1 fills entire rectangle 
        cv2.rectangle(img_copy, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text  string to display (color name and RGB values)
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        #(image , text,start,font (0-7),fontscale, color ,thickness , linetype )
        cv2.putText(img_copy, text, (50, 50), 2, fontscale, (255, 255, 255), 2, cv2.LINE_AA)
        
        #for very light color we will display text in black color  
        if r + g + b >= 600:
            cv2.putText(img_copy, text, (50, 50), 2, fontscale, (0, 0, 0), 2, cv2.LINE_AA)
        
        # Display the updated image
        cv2.imshow("image", img_copy)
        
        clicked = False

def crop_image():
    global img, img_copy
    if img is not None:
        # Open a new window for cropping
        cv2.namedWindow('Crop Image')
        roi = cv2.selectROI('Crop Image', img, fromCenter=False, showCrosshair=False)
        print(roi[0],roi[1],roi[2],roi[3])
        print(roi)
        print("height of ROI",roi[3])
        print(roi[1]+roi[3])
        print(roi[1:1+roi[3]])
                # Crop the selected region 
        cropped_img = img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

        # Display the cropped image
        cv2.imshow('Cropped Image', cropped_img)
        img_copy = cropped_img


def cartoonify_image():
    global img, img_copy
    if img is not None:
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply median blur to smooth the image
        smooth = cv2.medianBlur(gray, 5)
        
        # Detect edges using adaptive thresholding
        edges = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        
        # Apply bilateral filter to reduce noise and keep edges sharp
        color = cv2.bilateralFilter(img, 9, 300, 300)
        
        # Combine the cartoon image and edges using bitwise_and
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        # Display the cartoonified image
        cv2.imshow("image", cartoon)
        img_copy = cartoon

def black_and_white_image():
    global img, img_copy
    if img is not None:
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("image", gray)
        img_copy = gray

def convert_to_sketch(image):
    global img, img_copy
    if image is not None:
        

           # Convert the image to grayscale using cvtColor()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #  Invert the grayscale image using bitwise_not()
        inverted = cv2.bitwise_not(gray)

        #  Apply Gaussian Blur to the inverted image
        #blurr = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
        blur = cv2.GaussianBlur(inverted, (21, 21), 0)

        #  Divide operation for normalization
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)

        # Display the sketched image
        cv2.imshow("image", sketch)

        img_copy = sketch

def save_image():
    global img_copy
    if img_copy is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, img_copy)
            print(f"Image saved at {file_path}")

def refresh_image():
    global img, img_copy
    cv2.imshow("image", img)
    img_copy = None



# Global variables
clicked = False
b = g = r = 0
img_copy = None

# Create the OpenCV window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

# creating a tkinter window
root = tk.Tk()
root.title("Image Processing Tool")

# Set Size of Tkinter Window 
root.geometry("300x500")
root.minsize(150,410)
root.maxsize(300,500)

# Set Background image
bg = PhotoImage(file = "himal.png") 
label1 = Label( root, image = bg) 
label1.place(x = 0, y = 0) 

#change icon with ico file 
root.iconbitmap("himalaya.ico")

# width for all buttons 
btn_width = 15 

# Create GUI components
upload_button = tk.Button(root, text="Upload Image", bg='grey',command=upload_image, width=btn_width)
upload_button.pack(pady=10)

detect_button = tk.Button(root, text="Detect Color", bg='#89cff0',command=detect_color, width=btn_width)    # baby blue color
detect_button.pack(pady=10)

cartoonify_button = tk.Button(root, text="Cartoonify Image", bg='grey', command=cartoonify_image, width=btn_width)
cartoonify_button.pack(pady=10)

black_and_white_button = tk.Button(root, text="Black & White",bg='grey', command=black_and_white_image, width=btn_width)
black_and_white_button.pack(pady=10)

sketch_button = tk.Button(root, text="Sketch Image", bg='grey',command=lambda: convert_to_sketch(img), width=btn_width)
sketch_button.pack(pady=10)

crop_button = tk.Button(root, text="Crop Image",bg='grey', command=crop_image, width=btn_width)
crop_button.pack(pady=10)

save_button = tk.Button(root, text="Save Image",bg='#7fffd4', command=save_image, width=btn_width)   #  Aquamarine
save_button.pack(pady=10)

refresh_button = tk.Button(root, text="Refresh Image",bg='#7fffd4', command=refresh_image, width=btn_width)
refresh_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", bg='#7fffd4',command=root.destroy, width=btn_width)
exit_button.pack(pady=10)

root.mainloop()
cv2.destroyAllWindows()
