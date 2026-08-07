import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pytz

# --- Modern Color Palette ---
BG_COLOR = "#121212"          # Main background
CARD_BG = "#1E1E1E"           # Clock card background
TEXT_MAIN = "#FFFFFF"         # Main text (White)
TEXT_SUB = "#888888"          # Subtitle text (Gray)
ACCENT = "#007ACC"            # Button / Highlight color
TIME_COLOR = "#00D4FF"        # Digital clock color (Cyan)
DANGER = "#FF4C4C"            # Delete button color

class ModernWorldClock:
    def __init__(self, root):
        self.root = root
        self.root.title("World Clock")
        self.root.geometry("450x650") 
        self.root.configure(bg=BG_COLOR)
        
      
        self.clocks = [("UTC / GMT", "UTC")]
        self.clock_widgets = []
        
        
        self.tz_mapping = self._build_timezone_mapping()
        self.search_keys = sorted(list(self.tz_mapping.keys()))

        self._setup_ui()
        self.update_clocks()

    def _build_timezone_mapping(self):
        """Creates a dictionary mapping 'Country - City' to standard timezone strings."""
        mapping = {}
        
       
        tz_to_country = {}
        for country_code, timezones in pytz.country_timezones.items():
            country_name = pytz.country_names[country_code]
            for tz in timezones:
                tz_to_country[tz] = country_name

        for tz in pytz.all_timezones:
            
            city = tz.split("/")[-1].replace("_", " ")
            
            if tz in tz_to_country:
                country = tz_to_country[tz]
                display_name = f"{country} - {city}"
            else:
                display_name = tz 

            if display_name in mapping:
                display_name = f"{display_name} ({tz})"
                
            mapping[display_name] = tz
            
        return mapping

    def _setup_ui(self):
      
        header = tk.Label(self.root, text="World Clock", font=("Segoe UI", 24, "bold"), 
                          bg=BG_COLOR, fg=TEXT_MAIN)
        header.pack(pady=(20, 10))

       
        search_frame = tk.Frame(self.root, bg=BG_COLOR)
        search_frame.pack(fill="x", padx=20)

        search_lbl = tk.Label(search_frame, text="Search Country or City:", font=("Segoe UI", 10), 
                              bg=BG_COLOR, fg=TEXT_SUB)
        search_lbl.pack(anchor="w")

        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_timezones)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 12),
                                bg="#2C2C2C", fg=TEXT_MAIN, insertbackground=TEXT_MAIN, 
                                relief="flat", highlightthickness=1, highlightbackground="#333", highlightcolor=ACCENT)
        search_entry.pack(fill="x", ipady=5, pady=(5, 5))

        
        list_frame = tk.Frame(search_frame, bg=BG_COLOR)
        list_frame.pack(fill="x")
        
        self.tz_listbox = tk.Listbox(list_frame, height=4, font=("Segoe UI", 10),
                                     bg="#2C2C2C", fg=TEXT_MAIN, selectbackground=ACCENT, 
                                     relief="flat", highlightthickness=0, borderwidth=0)
        self.tz_listbox.pack(side="left", fill="x", expand=True)
        
       
        list_scroll = tk.Scrollbar(list_frame, orient="vertical", command=self.tz_listbox.yview)
        list_scroll.pack(side="right", fill="y")
        self.tz_listbox.config(yscrollcommand=list_scroll.set)

        
        self.filter_timezones()

        # Add Button
        add_btn = tk.Button(search_frame, text="Add Clock", font=("Segoe UI", 10, "bold"),
                            bg=ACCENT, fg=TEXT_MAIN, activebackground="#005A9E", activeforeground=TEXT_MAIN,
                            relief="flat", cursor="hand2", command=self.add_clock)
        add_btn.pack(fill="x", pady=10, ipady=4)

       
        self.canvas = tk.Canvas(self.root, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(10, 20))

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y", pady=(10, 20), padx=(0, 10))

        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.clock_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.clock_frame, anchor="nw")

        self.clock_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

    def filter_timezones(self, *args):
        """Filters the listbox based on what the user types in the search box."""
        search_term = self.search_var.get().lower()
        self.tz_listbox.delete(0, tk.END)
        
        for display_name in self.search_keys:
           
            if search_term in display_name.lower() or search_term in self.tz_mapping[display_name].lower():
                self.tz_listbox.insert(tk.END, display_name)

    def add_clock(self):
        selection = self.tz_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a location from the list first.")
            return
            
        selected_display = self.tz_listbox.get(selection[0])
        selected_tz = self.tz_mapping[selected_display]

      
        if any(tz == selected_tz for _, tz in self.clocks):
            messagebox.showwarning("Duplicate", f"The timezone for '{selected_display}' is already displayed.")
            return

  
        self.clocks.append((selected_display, selected_tz))
        self.render_clocks()
        
        
        self.search_var.set("")

    def remove_clock(self, index):
        if index > 0: 
            del self.clocks[index]
            self.render_clocks()

    def render_clocks(self):
        """Draws the cards for each timezone."""
        for widget in self.clock_frame.winfo_children():
            widget.destroy()

        self.clock_widgets = []

        for i, (display_name, tz_name) in enumerate(self.clocks):
            card = tk.Frame(self.clock_frame, bg=CARD_BG, padx=15, pady=15)
            card.pack(fill="x", pady=(0, 10))

           
            info_frame = tk.Frame(card, bg=CARD_BG)
            info_frame.pack(side="left", fill="y", expand=True)
            
            
            tk.Label(info_frame, text=display_name, font=("Segoe UI", 12, "bold"), 
                     bg=CARD_BG, fg=TEXT_MAIN, wraplength=200, justify="left").pack(anchor="w")
            tk.Label(info_frame, text=tz_name, font=("Segoe UI", 9), 
                     bg=CARD_BG, fg=TEXT_SUB).pack(anchor="w")

           
            time_frame = tk.Frame(card, bg=CARD_BG)
            time_frame.pack(side="right")

            time_lbl = tk.Label(time_frame, text="--:--:--", font=("Consolas", 18, "bold"), 
                                bg=CARD_BG, fg=TIME_COLOR)
            time_lbl.pack(anchor="e")
            
            date_lbl = tk.Label(time_frame, text="----/--/--", font=("Segoe UI", 9), 
                                bg=CARD_BG, fg=TEXT_SUB)
            date_lbl.pack(anchor="e")

            self.clock_widgets.append((time_lbl, date_lbl, tz_name))

            
            if i > 0:
                del_btn = tk.Label(card, text="✕", font=("Segoe UI", 12), bg=CARD_BG, fg=DANGER, cursor="hand2")
                del_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=-5)
                del_btn.bind("<Button-1>", lambda e, idx=i: self.remove_clock(idx))

    def update_clocks(self):
        """Ticks every second to update the digital time."""
        now_utc = datetime.now(pytz.utc)

        if len(self.clock_widgets) != len(self.clocks):
            self.render_clocks()

        for (time_lbl, date_lbl, tz_name) in self.clock_widgets:
            try:
                tz = pytz.timezone(tz_name)
                local_time = now_utc.astimezone(tz)
                time_lbl.config(text=local_time.strftime("%I:%M:%S %p"))
                date_lbl.config(text=local_time.strftime("%a, %b %d, %Y"))
            except Exception:
                time_lbl.config(text="Error")

        self.root.after(1000, self.update_clocks)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernWorldClock(root)
    root.mainloop()