import requests
import bs4
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

class ScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Website Scraper Tool")

        self.var = tk.StringVar()
        self.var.set("WEBSITE SCRAPER TOOL")
        label = tk.Label(self, textvariable=self.var, bd=8, bg="yellow", font=("Helvetica", 35))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.URL = tk.StringVar()
        entry = tk.Entry(self, bd=5, font=7, textvariable=self.URL)
        entry.grid(row=1, column=0, ipadx=100, padx=10, pady=10)

        button = tk.Button(self, text="Scrap it!", bd=5, command=self.scrappin)
        button.grid(row=2, column=0, padx=10, pady=10)

        new_window_button = tk.Button(self, text="Open Scraped Content Viewer", bd=5, command=self.open_new_window)
        new_window_button.grid(row=3, column=0, padx=10, pady=10)

        history_button = tk.Button(self, text="History", bd=5, command=self.open_history_window)
        history_button.grid(row=3, column=1, padx=10, pady=10)

        # History list to store processed URLs
        self.history_urls = []

    def scrappin(self):
        url = self.URL.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL")
            return

        try: 
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses

            soup = bs4.BeautifulSoup(response.text, "html.parser")

            with asksaveasfile(title="Save File", defaultextension=".txt", mode='w') as file:
                if file is None:  # User cancelled the save dialog
                    return
                for paragraph in soup.select('p'):
                    file.write(paragraph.get_text() + "\n")

            with open("WEB_TEXT.txt", "w") as text_file:
                for paragraph in soup.select('p'):
                    text_file.write(paragraph.get_text() + "\n")

            with open("WEB_CODE.txt", "w") as code_file:
                for paragraph in soup.select('p'):
                    code_file.write(paragraph.prettify() + "\n")

            # Add URL to history
            self.history_urls.append(url)

            messagebox.showinfo("Success", "Web content saved successfully!")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_new_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("Scraped Content Viewer")

        new_url_label = tk.Label(new_window, text="Enter URL:")
        new_url_label.grid(row=0, column=0, padx=10, pady=10)

        new_url = tk.StringVar()
        new_url_entry = tk.Entry(new_window, textvariable=new_url, width=50)
        new_url_entry.grid(row=0, column=1, padx=10, pady=10)

        def display_content():
            url = new_url.get()
            if not url:
                messagebox.showwarning("Input Error", "Please enter a URL")
                return

            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = bs4.BeautifulSoup(response.text, "html.parser")

                content_text.delete(1.0, tk.END)  # Clear previous content
                for paragraph in soup.select('p'):
                    content_text.insert(tk.END, paragraph.get_text() + "\n")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Request Error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        display_button = tk.Button(new_window, text="Display Content", command=display_content)
        display_button.grid(row=1, column=1, padx=10, pady=10)

        content_text = tk.Text(new_window, wrap=tk.WORD, width=80, height=20)
        content_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def open_history_window(self):
        history_window = tk.Toplevel(self)
        history_window.title("History")

        history_label = tk.Label(history_window, text="Processed URLs:")
        history_label.pack(padx=10, pady=10)

        history_listbox = tk.Listbox(history_window, width=80, height=20)
        history_listbox.pack(padx=10, pady=10)

        for url in self.history_urls:
            history_listbox.insert(tk.END, url)

        def select_url_from_history(event):
            selected_url = history_listbox.get(history_listbox.curselection())
            self.URL.set(selected_url)

        history_listbox.bind('<<ListboxSelect>>', select_url_from_history)

if __name__ == "__main__":
    app = ScraperApp()
    app.mainloop()
