'''
Author: Mark Sikder
Date: 2025-08-26
'''

import tkinter as tk
from tkinter import filedialog, messagebox
from app.Anomaly import Anomaly
import pandas as pd
import os


class Window:
    def __init__(self):
        self.gt = Anomaly()
        # Global Variables to store the files
        self.file1 = None
        self.file2 = None
        self.missing_in_file1 = None
        self.missing_in_file2 = None
        self.slf1Label = None
        self.slf2Label = None
        self.result_frame = None
        self.f1tb = None
        self.f2tb = None
        self.f1_content = None
        self.f2_content = None
        self.tgBtn = None
        self.s1tb = None
        self.s2tb = None
        self.sheet1_content = None
        self.sheet2_content = None


    def select_files(self, file_category):
        """
        Functions allows the user to select the file(s) for mismatch
        """
        # select file(s)
        files = filedialog.askopenfilenames(
            initialdir= os.path.expanduser("~"),
            filetypes=([("Excel file", ".xlsx")])
        )

        if(files):
            # file1
            if file_category == "file1":
                self.file1 = self.gt.read_files(files, self.sheet1_content)
                self.slf1Label.config(text=f"Selected File(s): {', '.join(files)}")
            # file2
            else:
                self.file2 = self.gt.read_files(files, self.sheet2_content)
                self.slf2Label.config(text=f"Selected File(s): {', '.join(files)}")
                    
        else:
            print("File(s) not selected")

    def get_anomalies(self):
        """
        Function finds the mismatches between the selected file(s)
        """

        if self.file1 is None or self.file2 is None:
            messagebox.showwarning("Missing Files", "Please select files first.")
            return
        
        # check if columns were entered in the text box
        if self.f1_content is None and self.f1_content is None:
            messagebox.showwarning("Columns to compare not entered", "Please enter column names to compare between the files.")
            return

        try:
            #print(self.f1_content, self.f2_content)
            self.missing_in_file1, self.missing_in_file2 = self.gt.find_anomalies(self.file1, self.file2, self.f1_content, self.f2_content)
            # Clear old results
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            # Show links to download results
            if self.missing_in_file1 is not None:
                dash_link = tk.Label(self.result_frame, text="📂 Missing in File 1", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
                dash_link.pack(pady=5)
                dash_link.bind("<Button-1>", lambda e: self.download_results("file1"))

            if self.missing_in_file2 is not None:
                sart_link = tk.Label(self.result_frame, text="📂 Missing in File 2", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
                sart_link.pack(pady=5)
                sart_link.bind("<Button-1>", lambda e: self.download_results("file2"))
        except Exception as e:
            messagebox.showerror("Error", f"Please check the files selected\n{e}")


    def download_results(self, dataset):
        """
        Download the files    
        """

        data = self.missing_in_file1 if dataset == "file2" else self.missing_in_file2

        if data is None:
            messagebox.showwarning("No Data", "No results available to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title=f"Save Missing in {dataset.upper()} As"
        )

        if not save_path:
            return

        try:
            if save_path.endswith(".xlsx"):
                pd.DataFrame(data).to_excel(save_path, index=False)
            else:
                pd.DataFrame(data).to_csv(save_path, index=False)

            messagebox.showinfo("Success", f"Missing in {dataset.upper()} saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")


    def on_info_entered(self):
        """Enable Find Anomaly button when columns are entered"""
        self.f1_content = self.f1tb.get("1.0", tk.END).strip()
        self.f2_content = self.f2tb.get("1.0", tk.END).strip()
        self.sheet1_content = self.s1tb.get("1.0", tk.END).strip()
        self.sheet2_content = self.s2tb.get("1.0", tk.END).strip()
        
        if self.f1_content and self.f2_content and self.sheet1_content and self.sheet2_content:  # non-empty
            self.tgBtn.config(state="normal")
        else:
            self.tgBtn.config(state="disabled")


    def main(self):
        """
        Main Window
        """
        # Create the main window
        root = tk.Tk()
        root.title("Anomaly")
        root.geometry("900x700")  # width x height

        # Add a label
        label = tk.Label(root, text="ANOMALY", font=("Arial", 15))
        label.pack(pady=20)

        # Frame to hold the text boxes and labels
        stb_frame = tk.Frame(root)
        stb_frame.pack(pady=10)

        # Sheet 1 content
        s1_label = tk.Label(stb_frame, text="Enter Sheet Name to match with from File 1", font=("Arial", 12))
        s1_label.grid(row=0, column=0, padx=10, pady=(0,5))  # label above text box
        self.s1tb = tk.Text(stb_frame, height=1, width=30, font=("Arial", 12))
        self.s1tb.grid(row=1, column=0, padx=10)
        self.s1tb.bind("<KeyRelease>", lambda event: self.on_info_entered()) 

        # Sheet 2 content
        s2_label = tk.Label(stb_frame, text="Enter Sheet Name to match with from File 2", font=("Arial", 12))
        s2_label.grid(row=0, column=1, padx=10, pady=(0,5))  # label above text box
        self.s2tb = tk.Text(stb_frame, height=1, width=30, font=("Arial", 12))
        self.s2tb.grid(row=1, column=1, padx=10)
        self.s2tb.bind("<KeyRelease>", lambda event: self.on_info_entered()) 

        # file 1
        slf1Btn = tk.Button(root, text="Select First File(s)", command=lambda: self.select_files("file1"))
        slf1Btn.pack()
        self.slf1Label = tk.Label(root, text="No files selected.")
        self.slf1Label.pack(pady=(0, 20))  # add bottom padding to separate from SART

        # file 2
        slf2Btn = tk.Button(root, text="Select Second File(s)", command=lambda: self.select_files("file2"))
        slf2Btn.pack()
        self.slf2Label = tk.Label(root, text="No files selected.")
        self.slf2Label.pack(pady=(0, 20))  # add some spacing below too
        
        # Frame to hold the text boxes and labels
        tb_frame = tk.Frame(root)
        tb_frame.pack(pady=10)

        # File1 label and text box
        f1_label = tk.Label(tb_frame, text="Enter Column to match with from File 1", font=("Arial", 12))
        f1_label.grid(row=0, column=0, padx=10, pady=(0,5))  # label above text box
        self.f1tb = tk.Text(tb_frame, height=1, width=30, font=("Arial", 12))
        self.f1tb.grid(row=1, column=0, padx=10)
        self.f1tb.bind("<KeyRelease>", lambda event: self.on_info_entered()) 

        # File2 label and text box
        f2_label = tk.Label(tb_frame, text="Enter Column to match with from File 2", font=("Arial", 12))
        f2_label.grid(row=0, column=1, padx=10, pady=(0,5))  # label above text box
        self.f2tb = tk.Text(tb_frame, height=1, width=30, font=("Arial", 12))
        self.f2tb.grid(row=1, column=1, padx=10)
        self.f2tb.bind("<KeyRelease>", lambda event: self.on_info_entered()) 


        # Find Anomaly Button
        self.tgBtn = tk.Button(root, text="Find Anomaly", command=self.get_anomalies, state="disabled")
        self.tgBtn.pack(pady=20)

        # Frame to hold clickable result links
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=20)

        # Run the app
        root.mainloop()


if __name__ == "__main__":
    wndw = Window()
    wndw.main()