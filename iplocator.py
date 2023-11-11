import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import time

# Define the API endpoint (initially set to ipapi.co)
api_url = "https://ipapi.co/json/"

class IPInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address Info")
        
        self.ip_history = []
        
        self.label = tk.Label(root, text="Public IP Address Information", font=("Helvetica", 16))
        self.label.pack(pady=10)
        
        self.ip_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.ip_label.pack()
        
        self.city_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.city_label.pack()
        
        self.region_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.region_label.pack()
        
        self.country_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.country_label.pack()
        
        self.isp_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.isp_label.pack()
        
        self.asn_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.asn_label.pack()
        
        self.update_button = ttk.Button(root, text="Update IP Info", command=self.update_info)
        self.update_button.pack(pady=10)
        
        self.history_button = ttk.Button(root, text="Show IP History", command=self.show_history)
        self.history_button.pack()
        
        self.api_endpoint_label = tk.Label(root, text="API Endpoint (e.g., https://ipapi.co/json/):", font=("Helvetica", 12))
        self.api_endpoint_label.pack()
        
        self.api_endpoint_entry = tk.Entry(root)
        self.api_endpoint_entry.insert(0, api_url)
        self.api_endpoint_entry.pack()
        
        self.api_key_label = tk.Label(root, text="API Key (if required):", font=("Helvetica", 12))
        self.api_key_label.pack()
        
        self.api_key_entry = tk.Entry(root)
        self.api_key_entry.pack()
        
        self.update_interval_entry = tk.Entry(root)
        self.update_interval_entry.insert(0, "10")  # Default to 10 seconds
        self.update_interval_entry.pack()

        self.update_interval_button = ttk.Button(root, text="Update Interval", command=self.update_interval)
        self.update_interval_button.pack()

        
        
        self.start_update_thread()
    
    def testIp(self,ip_address):
        assert ip_address!="", "No IP Address Found!"
        return print("IP Address Successfully Obtained: " + ip_address)

    def update_interval(self):
        # Get the new update interval from the entry field
        new_interval = int(self.update_interval_entry.get())

        # Stop the current update thread
        if hasattr(self, "update_thread") and self.update_thread.is_alive():
            self.update_thread_stop.set()
            self.update_thread.join()

        # Schedule the auto_update method to run periodically with the new interval
         
        self.root.after(new_interval * 1000, self.auto_update, new_interval)

        
    def show_error(self, error_message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")

        error_label = tk.Label(error_window, text=error_message, font=("Helvetica", 12), fg="red")
        error_label.pack(pady=10)


    def update_info(self):
        api_url = self.api_endpoint_entry.get()
        api_key = self.api_key_entry.get()
        try:
            response = requests.get(api_url, headers={"User-Agent": "IPInfoApp"})
            if response.status_code == 200:
                data = response.json()
                ip_address = data["ip"]
                city = data["city"]
                region = data["region"]
                country = data["country_name"]
                isp = data["org"]
                asn = data["asn"]

                self.ip_label.config(text=f"IP Address: {ip_address}")
                self.city_label.config(text=f"City: {city}")
                self.region_label.config(text=f"Region: {region}")
                self.country_label.config(text=f"Country: {country}")
                self.isp_label.config(text=f"ISP: {isp}")
                self.asn_label.config(text=f"ASN: {asn}")

                # Add to IP history
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.ip_history.append(f"{timestamp}: {ip_address}")

                
            else:
                self.ip_label.config(text="Failed to retrieve IP information.")
            return ip_address
        except requests.RequestException as req_exc:
            self.show_error(f"Request error: {str(req_exc)}")
        except ValueError as json_exc:
            self.show_error(f"JSON decoding error: {str(json_exc)}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}")
    
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("IP Address History")
        
        history_label = tk.Label(history_window, text="IP Address History", font=("Helvetica", 16))
        history_label.pack(pady=10)
        
        scrollbar = tk.Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_text = tk.Text(history_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        history_text.pack()
        
        for item in self.ip_history:
            history_text.insert(tk.END, item + "\n")
        
        scrollbar.config(command=history_text.yview)
    
    def start_update_thread(self):
        update_interval = int(self.update_interval_entry.get())
        update_thread = threading.Thread(target=self.auto_update, args=(update_interval,))
        update_thread.daemon = True
        update_thread.start()
    
    def auto_update(self, interval):
        self.update_info()

        # Schedule the auto_update method to run again after the specified interval
        self.root.after(interval * 1000, self.auto_update, interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPInfoApp(root)
    root.mainloop()


