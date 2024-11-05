
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:07:32 2024

@author: kmedhi
"""

#GUI for EOB extraction
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import re
import sys
import os
from PIL import  Image
from PIL import ImageTk
import pandas as pd
import cv2
import numpy as np
import datetime
import pytesseract
import math
from pdf2image import convert_from_path
import numpy as np
from pytesseract import Output
import matplotlib.pyplot as plt
import csv


# global resi_factor , prev_page_no, scroll_amount
# resi_factor = 1.0
# prev_page_no =''
# scroll_amount = 0

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 6 lang=eng'

def Error_Log():
    global      Log_Error
    # This module write any error into ErrorLog text file
    now = datetime.now()
    date_time_string = now.strftime("%Y%m%d%H%M%S")
    date_string_log_file = now.strftime("%Y%m%d")
    #create a file pointer for file with append mode
    log_file = open( '\ErrorLog ' + date_string_log_file  + '.txt', "a+")
    #write the error message into file using file pointer
    log_file.write(date_time_string  +'|' + Log_Error )
    log_file.write('\n')
    log_file.close()




def GUI_Componant():
    global gui, Width, Height,Log_Error, xscrollbar,yscrollbar, canvas, canvas_image, frame
    #------------------------- Textbox variable--------------------------------
    global text_check_no, text_check_date,text_check_amount
    text_font_size = 12   
    #initialise GUI object
    gui=tk.Tk()
    text_box_height = 25
    from win32api import GetSystemMetrics
    #screen width height
    Width = GetSystemMetrics(0)
    Height = GetSystemMetrics(1)
    window_size = (Width, Height)
    #define size of window
    gui.geometry('{window_size[0]}x{window_size[1]}'.format(window_size=window_size))
    #add title of of GUI
    gui.title('Check Details Extraction')
    #Set background color of GUI
    gui.configure(background='#CDCDCD')


    #------Add heading to the GUI-------------
    heading = tk.Label(gui, text="Check Detail Extraction",pady=20, font=('arial',20,'bold'))
    heading.configure(background='#CDCDCD',foreground='#364156')
    heading.pack()

    #---------------------- Create the text label for check details------------------------
    left = 50
    check_label_top = 50
    label = tk.Label(gui, text="Check Number")
    label.configure(background='#CDCDCD',foreground='#364156',font=('arial',12,'bold'))
    label.place(x=left, y=check_label_top)

    label = tk.Label(gui, text="Check Date")
    label.configure(background='#CDCDCD',foreground='#364156',font=('arial',12,'bold'))
    left = left + 200
    label.place(x=left, y=check_label_top)

    label = tk.Label(gui, text="Check Amount")
    label.configure(background='#CDCDCD',foreground='#364156',font=('arial',12,'bold'))
    left = left + 200
    label.place(x=left, y=check_label_top)

    # -----------------------------Create the text box for check details----------------------------------
    left = 50
    top = check_label_top + 30
    text_check_no = tk.Entry(gui, font=("Arial", text_font_size))
    text_check_no.pack()
    text_check_no.place(x=left, y=top, width=150,height=text_box_height)
    
    text_check_date = tk.Entry(gui,  font=("Arial", text_font_size))
    left = left + 200
    text_check_date.place(x=left, y=top, width=150,height=text_box_height)

    text_check_amount = tk.Entry(gui,font=("Arial", text_font_size))
    text_check_amount.pack()
    left = left + 200
    text_check_amount.place(x=left, y=top, width=150,height=text_box_height)  
    
    #---------------------------- Create Frame to add Image --------------------------------
    frame = tk.Frame(gui, bd=2)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    #add horizontal scrollbar into frame
    xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
    #add vertical scrollbar into frame
    yscrollbar = tk.Scrollbar(frame)
    yscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
    #add frame to canvas
    canvas = tk.Canvas(frame, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)
    frame.place(x=50, y=150, width=int(Width/1.1 ), height=int(Height/1.4 ))


#================================== Moudle to display data ====================
def Image_Show():
    global  canvas,gui,  Log_Error, file_dir, df_data, Width, Height
    #--------------------------value valriables--------------------------------
    global check_no, check_amount, check_date
    
    #------------------------- Textbox variable--------------------------------
    global text_check_no, text_check_date,text_check_amount

    #set input File path from from directory
    gui_file = Tk()
    input_folder_path = filedialog.askopenfilename()
    #destroy open file dialog
    gui_file.destroy() 
    #read all images of folder in loop and convert into text files
    file_path= input_folder_path.upper()
    # find the directory
    file_dir = os.path.dirname(file_path)
    
    #call GUI
    GUI_Componant()
    #Upload first image of File descriptor default image
    try:
        
        image = Image.open(file_path)
        # Get the original width and height of the image
        width, height = image.size
        # Resize the image to 500x500 pixels
        image = image.resize((int(Width/1.1),int(Height/1.4)))
        #open image as tk inter compatible
        img = ImageTk.PhotoImage(image)
        #Set that image will display from to left corner in frame
        canvas_image = canvas.create_image(0, 0,image=img, anchor="nw")
        #enable scroll for big image
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
        canvas.itemconfig(canvas_image, image=img)  # Update the canvas image
        #set the uploaded image in frame
        canvas.image = img
        #extract check data
        check_details_extract(image, width, height)
        #find all files in directory
        file_descriptor_all =  os.listdir(file_dir)
        #uppercase the file name
        file_descriptor_all = [x.upper() for x in file_descriptor_all]
        #keep only .CSV files
        file_csv = [x for x in file_descriptor_all if  x.endswith('.CSV') ]
        if len(file_csv) == 1:
            try:
                csv_data_file = file_csv[0]
                #read the file
                df_data = pd.read_csv(csv_data_file, dtype=str, encoding="Latin-1")
                print("One data file found")
                #print('df_data length',len(df_data))
            except Exception as e :
                print('CSV file could not Read '+ str(e))
                LOG_Error = e
        elif len(file_csv) == 0:
            print("No data file found")
        else:
            print("Anomaly!!! Multiple .csv File found. Please keep one and run GUI Again")
        #set extracted details into textbox
        set_check_details()
    except Exception as e :
        Log_Error = str(e) + ' Image_Show() ' + 'Image ' 
        print(Log_Error)
    #Display the GUI
    gui.mainloop()

def check_details_extract(img,width, height):
    check_amount_extracted = 0
    check_date_extracted = 0
    check_number_extracted = 0
    check_no, check_date, check_amount = '', '', ''
    try:
        open_cv_image = np.array(img)
        # Convert RGB to BGR
        img = open_cv_image[:, :, ::-1].copy()
        #-----------------------Check detals/date amount ROI-----------------------------------
        img_roi = img[30:int(2*height/3),int(1.8*width/4):width-50]
        # show image
        plt.imshow(img_roi)
        plt.show()
        #process ROI to remove dot noise
        #img_roi = check_details_roi_process(img_roi)
        #--------------set check details coordinates-------
        x_coordinate = int(2.5*width/4)
        
        y_coordinate = 30
        value_width = width-50 - x_coordinate
        value_height = int(2*height/3) - y_coordinate
        
        #decrease size for tesseract
        #img_tess = cv2.resize(img, None, fx=.7, fy=.7, interpolation=cv2.INTER_CUBIC)#increase resize
        d_check = pytesseract.image_to_data(img_roi, config=custom_config,output_type=Output.DICT)
        
        text_check_details =  ' '.join(x for x in d_check['text'] )  #join with space only alphabates
        #remove , from text
        text_check_details = text_check_details.replace(',', '')
        
        #----------------------------Extract check amount---------------------------
        match_tesseract = re.search( '\d+\.\d{2}', text_check_details.replace(' ', ''))
        if match_tesseract and check_amount_extracted == 0:
                    # Yes, process key value
                    check_amount = match_tesseract.group(0).strip()
                    print('Check amount        : ',check_amount)
                    check_amount_extracted = 1
                    #set Cordinate
                    check_amount_coordinate = (x_coordinate, y_coordinate , value_width , value_height)
        #--------------------------Extract check date-------------------------
        pattern_str1 = r'\d{1,2}-\d{1,2}-\d{1,4}|\d{1,2}/\d{1,2}/\d{1,4}|'
        pattern_str2= r'^JANUARY \d{1,2}, \d{4}$|^FEBRUARY \d{1,2}, \d{4}$|^MARCH \d{1,2}, \d{4}$|^APRIL \d{1,2}, \d{4}$|^MAY \d{1,2}, \d{4}$|^JUNE \d{1,2}, \d{4}$|^JULY \d{1,2}, \d{4}$|^AUGUST \d{1,2}, \d{4}$|^SEPTEMBER \d{1,2}, \d{4}$|^OCTOBER \d{1,2}, \d{4}$|^NOVEMBER \d{1,2}, \d{4}$|^DECEMBER \d{1,2}, \d{4}$'

        match_tesseract = re.search( pattern_str1 + pattern_str2, text_check_details)
        
        
        if match_tesseract and check_date_extracted ==0:
            # Yes, process key value
            check_date = match_tesseract.group(0).strip()
            #now validate by current date
            #check_date = validate_by_current_date(check_date)
            if check_date != '':
                   print('Check date          : ',check_date)
                   check_date_extracted = 1
                   #set Cordinate
                   check_date_coordinate = (x_coordinate, y_coordinate , value_width , value_height)
        #Extract check number
        match_tesseract = re.search( '\s\d{6,12}\s|\.\d{5,12}\s|\s\d{5,12}\.\s', text_check_details)
        
        if match_tesseract and check_number_extracted == 0:
                    # Yes, process key value
                    check_no = match_tesseract.group(0).replace('.','').strip()
                    print('Check number          : ',check_no)
                    check_number_extracted = 1
                    #set Cordinate
                    check_no_coordinate = (x_coordinate, y_coordinate , value_width , value_height)
        #write check details in .csv file
        data = ['img', check_no, check_date, check_amount ]
        with open( 'output.csv', 'wt', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(('IMAGENAME',	 'CHECK NUMBER',	 'CHECK DATE',	 'CHECK AMOUNT'))
            writer.writerow(data)    
    except Exception as e:
         Log_Error = str(e) + ' check_details_extract() ' + 'Image ' 
         print(Log_Error)
         
         
def set_check_details():
    global df_data, Log_Error
    try:
        #Select row of current image 
        selected_row = df_data
        print('row',selected_row['IMAGENAME'])
        check_no = selected_row['CHECK NUMBER'].iloc[0]
        if pd.isna(check_no):
            check_no = ''
        check_date =selected_row['CHECK DATE'].iloc[0]
        if pd.isna(check_date):
            check_date = ''
        check_amount = selected_row['CHECK AMOUNT'].iloc[0]
        if pd.isna(check_amount):
            check_amount = ''
        print('check_no :',check_no)
        print('check_date :',check_date)
        print('check_amount :', check_amount)

        #set value in text box  
        text_check_date.delete(0, tk.END)  # Clear previous text
        text_check_date.insert(0, check_date) # set new text

        text_check_no.delete(0, tk.END)  # Clear previous text
        text_check_no.insert(0, check_no) # set new text

        text_check_amount.delete(0, tk.END)  # Clear previous text
        text_check_amount.insert(0, check_amount) # set new text
        
    except Exception as e:
         Log_Error = str(e) + ' set_check_details() ' + 'Image ' 
         print(Log_Error)
                             
#call Data_Extract()
if __name__ == "__main__":

    Image_Show()