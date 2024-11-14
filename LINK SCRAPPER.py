import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

def scrape_links():
    url = entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [(link.get_text(strip=True), link.get('href')) for link in soup.find_all('a') if link.get('href')]
        
        if not links:
            messagebox.showinfo("No Data", "No links found on the page.")
            return
        
        # Ask the user to choose a file location and name
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Link Text", "URL"])
                writer.writerows(links)
            messagebox.showinfo("Success", f"Data saved to {file_path}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

# GUI Setup
root = tk.Tk()
root.title("Link Scraper")

tk.Label(root, text="Enter URL to Scrape:").pack()
entry = tk.Entry(root, width=50)
entry.pack()

tk.Button(root, text="Scrape and Save Links", command=scrape_links).pack()
root.mainloop()
