import cv2
import numpy as np
import pytesseract
import pyautogui
import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import os
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Detection App")

        # Set the coordinates and size of the region to capture
        self.x, self.y, self.width, self.height = 360, 560, 250, 100
        #360, 560, 250, 100
        # Flags to indicate whether the mouse has already been moved for each trade type
        self.spy_trade_opened = False
        self.spy_trade_closed = False
        self.spx_trade_opened = False
        self.spx_trade_closed = False
        self.opened_strike_price = 0;

        self.total_trades = 0

        # Create label for displaying screen capture
        self.img_label = ttk.Label(self.root)
        self.img_label.pack()

        # Create text widget for displaying OCR text
        self.text_widget = tk.Text(self.root, width=50, height=5)
        self.text_widget.pack()

        self.detected_label = ttk.Label(self.root, text="", font=("Helvetica", 16))
        self.detected_label.pack()

        self.total_trades_label = ttk.Label(self.root, text=f"Total Trades: {self.total_trades}")
        self.total_trades_label.pack()

        # Create button for starting and stopping detection
        self.detect_button = ttk.Button(self.root, text="Start Detection", command=self.toggle_detection)
        self.detect_button.pack()

        self.detecting = False

    def toggle_detection(self):
        if self.detecting:
            self.detecting = False
            self.detect_button.config(text="Start Detection")
        else:
            self.detecting = True
            self.detect_button.config(text="Stop Detection")
            self.detect_text()

    def detect_text(self):
        hour = 14
        minute = 45

        while self.detecting:
            # Capture the region of the screen
            img = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))

            # Convert the image to grayscale and apply thresholding
            gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Perform OCR on the thresholded image
            text = pytesseract.image_to_string(Image.fromarray(thresh))

            self.detected_label.config(text=text)

            # Check if the text "BTO SPY XXXc" is present
            if re.search(r'.*[Bb][Tt][Oo].*[Ss][Pp][Yy].*\d+[Cc¢]', text):
                strike_price = re.search(r'.*[Bb][Tt][Oo].*[Ss][Pp][Yy].*(\d+)[Cc¢]', text).group(1)
                # Open a new SPY trade if one hasn't already been opened
                if not self.spy_trade_opened and not self.spx_trade_opened:
                    self.text_widget.insert("end", "Trade opened: BTO SPY XXXc\n")
                    pyautogui.moveTo(1780, 200)
                    pyautogui.click()
                    self.spy_trade_opened = True
                    self.spy_trade_closed = False
                    self.opened_strike_price = strike_price

            # Check if the text "STC SPY XXXc" is present
            if re.search(r'[Ss][Tt][Cce].*[Ss][Pp][Yy].*\d+[Cc¢]', text):
                strike_price = re.search(r'[Ss][Tt][Cce].*[Ss][Pp][Yy].*(\d+)[Cc¢]', text).group(1)
                # Close the current SPY trade if one has been opened but not yet closed
                if self.spy_trade_opened and not self.spy_trade_closed and self.opened_strike_price == strike_price:
                    self.text_widget.insert("end", "Trade closed: STC SPY XXXc\n")
                    pyautogui.moveTo(1700, 200)
                    pyautogui.click()
                    self.spy_trade_closed = True
                    self.spy_trade_opened = False
                    self.total_trades += 1
                    self.total_trades_label.config(text=f"Total Trades: {self.total_trades}")

            if re.search(r'[Bb][Tt][Oo].*[Ss][Pp][Yy].*\d+[Pp]', text):
                strike_price = re.search(r'.*[Bb][Tt][Oo].*[Ss][Pp][Yy].*(\d+)[Pp]', text).group(1)
                # Open a new SPY trade if one hasn't already been opened
                if not self.spy_trade_opened and not self.spx_trade_opened:
                    self.text_widget.insert("end", "Trade opened: BTO SPY XXXp\n")
                    pyautogui.moveTo(1780, 200)
                    pyautogui.click()
                    self.spy_trade_opened = True
                    self.spy_trade_closed = False
                    self.opened_strike_price = strike_price

            # Check if the text "STC SPY XXXc" is present
            if re.search(r'[Ss][Tt][Cce].*[Ss][Pp][Yy].*\d+[Pp]', text):
                strike_price = re.search(r'.*[Ss][Tt][Cce].*[Ss][Pp][Yy].*(\d+)[Pp]', text).group(1)
                # Close the current SPY trade if one has been opened but not yet closed
                if self.spy_trade_opened and not self.spy_trade_closed and self.opened_strike_price == strike_price:
                    self.text_widget.insert("end", "Trade closed: STC SPY XXXp\n")
                    pyautogui.moveTo(1700, 200)
                    pyautogui.click()
                    self.spy_trade_closed = True
                    self.spy_trade_opened = False
                    self.total_trades += 1
                    self.total_trades_label.config(text=f"Total Trades: {self.total_trades}")

            if re.search(r'[Bb][Tt][Oo].*[Ss][Pp][Xx].*\d+[Cc¢]', text):
                strike_price = re.search(r'.*[Bb][Tt][Oo].*[Ss][Pp][Xx].*(\d+)[Cc¢]', text).group(1)
                # Open a new SPY trade if one hasn't already been opened
                if not self.spx_trade_opened and not self.spy_trade_opened:
                    self.text_widget.insert("end", "Trade opened: BTO SPX XXXc\n")
                    pyautogui.moveTo(1780, 200)
                    pyautogui.click()
                    self.spx_trade_opened = True
                    self.spx_trade_closed = False
                    self.opened_strike_price = strike_price

            # Check if the text "STC SPY XXXc" is present
            if re.search(r'[Ss][Tt][Cce].*[Ss][Pp][Xx].*\d+[Cc¢]', text):
                strike_price = re.search(r'.*[Ss][Tt][Cce].*[Ss][Pp][Xx].*(\d+)[Cc¢]', text).group(1)
                # Close the current SPY trade if one has been opened but not yet closed
                if self.spx_trade_opened and not self.spx_trade_closed and self.opened_strike_price == strike_price:
                    self.text_widget.insert("end", "Trade closed: STC SPX XXXc\n")
                    pyautogui.moveTo(1700, 200)
                    pyautogui.click()
                    self.spx_trade_closed = True
                    self.spx_trade_opened = False
                    self.total_trades += 1
                    self.total_trades_label.config(text=f"Total Trades: {self.total_trades}")

            if re.search(r'[Bb][Tt][Oo].*[Ss][Pp][Xx].*\d+[Pp]', text):
                strike_price = re.search(r'.*[Bb][Tt][Oo].*[Ss][Pp][Xx].*(\d+)[Pp]', text).group(1)
                # Open a new SPY trade if one hasn't already been opened
                if not self.spy_trade_opened and not self.spx_trade_opened:
                    self.text_widget.insert("end", "Trade opened: BTO SPX XXXp\n")
                    pyautogui.moveTo(1780, 200)
                    pyautogui.click()
                    self.spx_trade_opened = True
                    self.spx_trade_closed = False
                    self.opened_strike_price = strike_price

            # Check if the text "STC SPY XXXc" is present
            if re.search(r'[Ss][Tt][Cce].*[Ss][Pp][Xx].*\d+[Pp]', text):
                strike_price = re.search(r'.*[Ss][Tt][Cce].*[Ss][Pp][Xx].*(\d+)[Pp]', text).group(1)
                # Close the current SPY trade if one has been opened but not yet closed
                if self.spx_trade_opened and not self.spx_trade_closed and self.opened_strike_price == strike_price:
                    self.text_widget.insert("end", "Trade closed: STC SPX XXXp\n")
                    pyautogui.moveTo(1700, 200)
                    pyautogui.click()
                    self.spx_trade_closed = True
                    self.spx_trade_opened = False
                    self.total_trades += 1
                    self.total_trades_label.config(text=f"Total Trades: {self.total_trades}")

            current_time = time.localtime()

            # Check if the current time matches the sleep time
            if current_time.tm_hour == hour and current_time.tm_min == minute:
                # Put the computer into sleep mode
                os.system("rundll32.exe powrprof.dll,SetSuspendState Standby")
                break

            # Update the image label with the latest screenshot
            img = Image.fromarray(np.array(img))
            imgtk = ImageTk.PhotoImage(image=img)
            self.img_label.imgtk = imgtk
            self.img_label.configure(image=imgtk)
            self.root.update()




def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
