from project4 import IPInfoApp
import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import time

root = tk.Tk()
tester = IPInfoApp(root)
ipAdd = tester.update_info()
testResult = tester.testIp(ipAdd)

root.mainloop()


