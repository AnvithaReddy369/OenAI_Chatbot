# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 19:26:29 2023

@author: ANVITHA
"""

import openai
import tkinter as tk
from PIL import ImageTk, Image, ImageOps
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ANVITHA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
from tkinter import filedialog
import time
openai.api_key = "enter your API key here"



def generate_response():
    model_engine = "text-davinci-003"
    prompt = input_text.get('1.0', 'end-1c')
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = completion.choices[0].text
    
    # clear the output area
    output_text.delete('1.0', tk.END)
    
    # print each letter with a delay of 0.02 seconds
    for char in response:
        output_text.insert(tk.END, char)
        output_text.update()
        time.sleep(0.02)


def browse_file():
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if filename:
        image = Image.open(filename)
        text = pytesseract.image_to_string(image)

        input_text.delete('1.0', tk.END)
        input_text.insert(tk.END, text)

def scan_text():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow("Scan Text", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite("scan.jpg", frame)
            cap.release()
            cv2.destroyAllWindows()
            break
 
    # Load the original image
    image = Image.open("scan.jpg")#.convert('L')

    
        # Flip the image horizontally
   # mirrored_image = image.transpose(method=ImageOps.Transpose.FLIP_LEFT_RIGHT)
    mirrored_image = ImageOps.mirror(image)
    
    # Perform OCR on the mirrored image
    text = pytesseract.image_to_string(mirrored_image)
    
    # Display the mirror image text in a Tkinter text widget
    input_text.delete('1.0', tk.END)
    input_text.insert(tk.END, text)
 
        



# create the GUI
root = tk.Tk()



root.title("OpenAI Chatbot")

# create the input prompt
input_frame = tk.Frame(root, bg="#383838")
input_label = tk.Label(input_frame, text="Enter a prompt:", font=("Helvetica", 14), fg="white", bg="#383838")
input_label.pack(side=tk.LEFT)
input_text = tk.Text(input_frame, width=50, height=3, font=("Helvetica", 14))
input_text.pack(side=tk.LEFT)
input_frame.pack(pady=(10, 20))

# create the browse button
#browse_button = tk.Button(root, text="Browse Image", font=("Helvetica", 12), command=browse_file)
browse_button_style = {
    "font": ("Helvetica", 12),
    "command": browse_file,
    "bg": "#383838",
    "fg": "white",
    "bd": 0,
    "activebackground": "#383838",
    "activeforeground": "white",
    "highlightthickness": 0,
}
browse_button = tk.Button(root, text="Browse Image", **browse_button_style)
browse_button.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10, width=120, height=37.5)
input_text.pack(side=tk.LEFT, padx=(10, 0))
#browse_button.pack()


# create the scan button
#scan_button = tk.Button(root, text="Scan Text", font=("Helvetica", 12), command=scan_text)
#scan_button.pack()

scan_button_style = {
    "font": ("Helvetica", 12),
    "command": scan_text,
    "bg": "#383838",
    "fg": "white",
    "bd": 0,
    "activebackground": "#383838",
    "activeforeground": "white",
    "highlightthickness": 0,
}
scan_button = tk.Button(root, text="scan Image", **scan_button_style)
scan_button.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=40, width=120, height=37.5)
input_text.pack(side=tk.LEFT, padx=(40, 0))
# create the output response
output_frame = tk.Frame(root, bg="#383838")
output_label = tk.Label(output_frame, text="Response:", font=("Helvetica", 14), fg="white", bg="#383838")
output_label.pack(side=tk.LEFT)
output_text = tk.Text(output_frame, width=50, height=10, font=("Helvetica", 14))
output_text.pack(side=tk.LEFT)
output_frame.pack(pady=(20, 10))

# create the generate button
button_frame = tk.Frame(root)
generate_button = tk.Button(button_frame, text="Generate", font=("Helvetica", 14), bg="#383838", fg="white", command=generate_response)
generate_button.pack(side=tk.LEFT, padx=10)
button_frame.pack()


# create the reset button
reset_button = tk.Button(root, text="Reset", command=lambda: reset())
reset_button.pack()

# reset function
def reset():
    input_text.delete('1.0', tk.END)
    output_text.delete('1.0', tk.END)
# run the GUI
root.mainloop()
