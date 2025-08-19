#!/usr/bin/env python3
"""
PingTest Config Editor - GUI application for modifying ping test configuration
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
from typing import List, Dict, Any


class ConfigEditor:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PingTest Configuration Editor")
        self.root.geometry("900x550")  # Reduced height from 700 since we removed settings section
        self.root.resizable(True, True)
        
        # Configuration file path
        self.config_file = "config.json"
        self.config_data = {}
        
        # Load configuration
        self.load_config()
        
        # Create GUI elements
        self.create_widgets()
        
        # Load current values
        self.load_current_values()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
                    
                    # Handle legacy config format (convert list of IPs to dict format)
                    if "ip_addresses" in self.config_data and isinstance(self.config_data["ip_addresses"], list):
                        # Convert old format to new format
                        old_ips = self.config_data["ip_addresses"]
                        self.config_data["ip_addresses"] = {}
                        for ip in old_ips:
                            self.config_data["ip_addresses"][ip] = ""
            else:
                # Create default config if file doesn't exist
                self.config_data = {
                    "ip_addresses": {
                        "8.8.8.8": "Google DNS",
                        "1.1.1.1": "Cloudflare DNS",
                        "208.67.222.222": "OpenDNS"
                    },
                    "ping_interval": 60,  # seconds
                    "ping_count": 4,      # number of pings per check
                    "timeout": 5,         # timeout in seconds
                    "log_file": "pingtest.log",
                    "total_runtime": 0    # total runtime in seconds (0 = run indefinitely)
                }
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            self.config_data = {}
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PingTest Configuration Editor", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))  # Increased padding
        
        # IP Addresses Section
        ip_frame = ttk.LabelFrame(main_frame, text="IP Addresses", padding="15")  # Increased padding
        ip_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))  # Increased padding
        ip_frame.columnconfigure(0, weight=1)
        
        # IP listbox with scrollbar
        ip_listbox_frame = ttk.Frame(ip_frame)
        ip_listbox_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))  # Increased padding
        ip_listbox_frame.columnconfigure(0, weight=1)
        
        # Create a frame for listbox and reorder buttons
        listbox_controls_frame = ttk.Frame(ip_listbox_frame)
        listbox_controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_controls_frame.columnconfigure(0, weight=1)
        
        self.ip_listbox = tk.Listbox(listbox_controls_frame, height=10)  # Increased height from 8
        ip_scrollbar = ttk.Scrollbar(listbox_controls_frame, orient=tk.VERTICAL, command=self.ip_listbox.yview)
        self.ip_listbox.configure(yscrollcommand=ip_scrollbar.set)
        
        # Reorder buttons frame
        reorder_frame = ttk.Frame(listbox_controls_frame)
        
        # Place listbox and scrollbar
        self.ip_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ip_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Place reorder buttons
        reorder_frame.grid(row=0, column=2, sticky=(tk.N, tk.S), padx=(5, 0))
        
        # UP and DOWN arrow buttons
        ttk.Button(reorder_frame, text="▲", width=3, command=self.move_ip_up).grid(row=0, column=0, pady=(0, 2))
        ttk.Button(reorder_frame, text="▼", width=3, command=self.move_ip_down).grid(row=1, column=0, pady=(2, 0))
        
        # Help text for reordering
        reorder_help = ttk.Label(ip_listbox_frame, text="Use ▲▼ buttons or Ctrl+↑↓ to reorder IPs", 
                                 font=("Arial", 8), foreground="gray")
        reorder_help.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Settings variables (needed for save_config and other methods)
        self.interval_var = tk.StringVar()
        self.count_var = tk.StringVar()
        self.timeout_var = tk.StringVar()
        self.runtime_var = tk.StringVar()
        self.log_file_var = tk.StringVar()
        
        # IP input and buttons
        ip_input_frame = ttk.Frame(ip_frame)
        ip_input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))  # Increased padding
        ip_input_frame.columnconfigure(0, weight=1)
        
        # IP entry
        ttk.Label(ip_input_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, pady=3)  # Increased padding
        self.ip_entry = ttk.Entry(ip_input_frame)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(15, 15), pady=3)  # Increased padding
        
        # Name entry
        ttk.Label(ip_input_frame, text="Name (optional):").grid(row=1, column=0, sticky=tk.W, pady=3)  # Increased padding
        self.name_entry = ttk.Entry(ip_input_frame)
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(15, 15), pady=3)  # Increased padding
        
        # Buttons frame
        button_frame = ttk.Frame(ip_input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))  # Increased padding
        
        ttk.Button(button_frame, text="Add IP", command=self.add_ip).grid(row=0, column=0, padx=(0, 8))  # Increased padding
        ttk.Button(button_frame, text="Remove IP", command=self.remove_ip).grid(row=0, column=1, padx=(0, 8))  # Increased padding
        ttk.Button(button_frame, text="Edit Name", command=self.edit_name).grid(row=0, column=2, padx=(0, 8))  # Increased padding
        ttk.Button(button_frame, text="Clear All", command=self.clear_ips).grid(row=0, column=3)
        
        # Buttons Section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(25, 0))  # Moved up from row 3
        
        # Make Save button more prominent
        save_button = ttk.Button(button_frame, text="💾 SAVE CONFIGURATION", 
                                command=self.save_config, 
                                style="Accent.TButton")
        save_button.grid(row=0, column=0, padx=(0, 15))  # Increased padding
        
        ttk.Button(button_frame, text="⚙️ Settings", command=self.open_settings_dialog).grid(row=0, column=1, padx=(0, 15))  # Added Settings button
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_to_defaults).grid(row=0, column=2, padx=(0, 15))  # Increased padding
        ttk.Button(button_frame, text="Exit", command=self.root.quit).grid(row=0, column=3)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self.save_config())
        self.root.bind('<Control-S>', lambda e: self.save_config())
        self.root.bind('<Control-Up>', lambda e: self.move_ip_up())
        self.root.bind('<Control-Down>', lambda e: self.move_ip_down())
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Press Ctrl+S to save quickly")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))  # Moved to row 3
    
    def load_current_values(self):
        """Load current configuration values into the GUI"""
        # Load IP addresses
        self.ip_listbox.delete(0, tk.END)
        for ip, name in self.config_data.get("ip_addresses", {}).items():
            self.ip_listbox.insert(tk.END, f"{ip} ({name})")
        
        # Load other settings
        self.interval_var.set(str(self.config_data.get("ping_interval", 60)))
        self.count_var.set(str(self.config_data.get("ping_count", 4)))
        self.timeout_var.set(str(self.config_data.get("timeout", 5)))
        self.runtime_var.set(str(self.config_data.get("total_runtime", 0)))
        self.log_file_var.set(self.config_data.get("log_file", "pingtest.log"))
    
    def add_ip(self):
        """Add a new IP address"""
        ip = self.ip_entry.get().strip()
        name = self.name_entry.get().strip()
        
        if not ip:
            messagebox.showwarning("Warning", "Please enter an IP address")
            return
        
        # Basic IP validation
        if not self.is_valid_ip(ip):
            messagebox.showwarning("Warning", "Please enter a valid IP address")
            return
        
        if ip in self.config_data["ip_addresses"]:
            messagebox.showwarning("Warning", "IP address already exists")
            return
        
        # Add IP with name to config
        self.config_data["ip_addresses"][ip] = name
        
        # Update listbox
        display_name = name if name else "No Name"
        self.ip_listbox.insert(tk.END, f"{ip} ({display_name})")
        
        # Clear entries
        self.ip_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.status_var.set(f"Added IP: {ip}" + (f" - {name}" if name else ""))
    
    def remove_ip(self):
        """Remove selected IP address"""
        selection = self.ip_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an IP address to remove")
            return
        
        ip_item = self.ip_listbox.get(selection[0])
        ip_text = ip_item.split(" (")[0] # Extract IP from "IP (Name)"
        
        if ip_text in self.config_data["ip_addresses"]:
            del self.config_data["ip_addresses"][ip_text]
            self.ip_listbox.delete(selection[0])
            self.status_var.set(f"Removed IP: {ip_text}")
        else:
            messagebox.showwarning("Warning", "IP address not found in configuration")
    
    def clear_ips(self):
        """Clear all IP addresses"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all IP addresses?"):
            self.ip_listbox.delete(0, tk.END)
            self.config_data["ip_addresses"] = {} # Clear the dictionary
            self.status_var.set("Cleared all IP addresses")
    
    def move_ip_up(self):
        """Move selected IP address up in the list"""
        selection = self.ip_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an IP address to move")
            return
        
        index = selection[0]
        if index == 0:  # Already at the top
            return
        
        # Get the IP item text
        ip_item = self.ip_listbox.get(index)
        
        # Remove from current position
        self.ip_listbox.delete(index)
        
        # Insert at new position (one up)
        self.ip_listbox.insert(index - 1, ip_item)
        
        # Select the moved item
        self.ip_listbox.selection_set(index - 1)
        
        self.status_var.set(f"Moved IP up: {ip_item.split(' (')[0]}")
    
    def move_ip_down(self):
        """Move selected IP address down in the list"""
        selection = self.ip_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an IP address to move")
            return
        
        index = selection[0]
        if index == self.ip_listbox.size() - 1:  # Already at the bottom
            return
        
        # Get the IP item text
        ip_item = self.ip_listbox.get(index)
        
        # Remove from current position
        self.ip_listbox.delete(index)
        
        # Insert at new position (one down)
        self.ip_listbox.insert(index + 1, ip_item)
        
        # Select the moved item
        self.ip_listbox.selection_set(index + 1)
        
        self.status_var.set(f"Moved IP down: {ip_item.split(' (')[0]}")
    
    def is_valid_ip(self, ip: str) -> bool:
        """Basic IP address validation"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    return False
            return True
        except:
            return False
    
    def save_config(self):
        """Save configuration to file"""
        try:
            # Validate inputs
            try:
                interval = int(self.interval_var.get())
                count = int(self.count_var.get())
                timeout = int(self.timeout_var.get())
                runtime = int(self.runtime_var.get())
                
                if interval <= 0 or count <= 0 or timeout <= 0 or runtime < 0:
                    raise ValueError("Values must be positive (except runtime)")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid numeric values: {e}")
                return
            
            # Get IP addresses with their names from the current config data
            ip_addresses = {}
            for item_index in range(self.ip_listbox.size()):
                ip_item = self.ip_listbox.get(item_index)
                ip_text = ip_item.split(" (")[0]  # Extract IP from "IP (Name)"
                
                # Get the name from the current config data
                name = self.config_data["ip_addresses"].get(ip_text, "")
                ip_addresses[ip_text] = name
            
            if not ip_addresses:
                messagebox.showerror("Error", "At least one IP address is required")
                return
            
            # Create new config
            new_config = {
                "ip_addresses": ip_addresses,
                "ping_interval": interval,
                "ping_count": count,
                "timeout": timeout,
                "log_file": self.log_file_var.get(),
                "total_runtime": runtime
            }
            
            # Show save confirmation with summary
            summary = f"Configuration Summary:\n\n"
            summary += f"IP Addresses: {len(ip_addresses)}\n"
            summary += f"Ping Interval: {interval} seconds\n"
            summary += f"Ping Count: {count}\n"
            summary += f"Timeout: {timeout} seconds\n"
            summary += f"Log File: {self.log_file_var.get()}\n"
            summary += f"Total Runtime: {runtime if runtime > 0 else 'Indefinite'} seconds\n\n"
            
            # Add IP list
            summary += "IP Addresses:\n"
            for ip, name in ip_addresses.items():
                if name:
                    summary += f"  {ip} → {name}\n"
                else:
                    summary += f"  {ip}\n"
            
            if not messagebox.askyesno("Confirm Save", f"{summary}\n\nSave this configuration?"):
                return
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(new_config, f, indent=4)
            
            # Update current config
            self.config_data = new_config
            
            self.status_var.set("Configuration saved successfully!")
            messagebox.showinfo("Success", f"Configuration saved successfully!\n\nFile: {self.config_file}\nIP Addresses: {len(ip_addresses)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            self.status_var.set("Error saving configuration")
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Confirm", "Are you sure you want to reset to default values?"):
            self.config_data = {
                "ip_addresses": {
                    "8.8.8.8": "Google DNS",
                    "1.1.1.1": "Cloudflare DNS",
                    "208.67.222.222": "OpenDNS"
                },
                "ping_interval": 60,
                "ping_count": 4,
                "timeout": 5,
                "log_file": "pingtest.log",
                "total_runtime": 0
            }
            self.load_current_values()
            self.status_var.set("Reset to default values")

    def edit_name(self):
        """Edit the name of a selected IP address"""
        selection = self.ip_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an IP address to edit")
            return
        
        ip_item = self.ip_listbox.get(selection[0])
        ip_text = ip_item.split(" (")[0]  # Extract IP from "IP (Name)"
        
        if ip_text not in self.config_data["ip_addresses"]:
            messagebox.showwarning("Warning", "IP address not found in configuration")
            return
        
        # Get current name
        current_name = self.config_data["ip_addresses"][ip_text]
        
        # Create a simple dialog for editing the name
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Name for {ip_text}")
        dialog.geometry("450x200")  # Increased from 400x150
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog content
        ttk.Label(dialog, text=f"IP Address: {ip_text}", font=("Arial", 10, "bold")).pack(pady=(20, 10))
        ttk.Label(dialog, text="Name (optional):").pack(pady=(0, 5))
        
        name_var = tk.StringVar(value=current_name)
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=50)  # Increased width
        name_entry.pack(pady=(0, 30))  # Increased bottom padding
        name_entry.focus()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=(0, 20))
        
        def save_name():
            new_name = name_var.get().strip()
            self.config_data["ip_addresses"][ip_text] = new_name
            
            # Update listbox
            display_name = new_name if new_name else "No Name"
            self.ip_listbox.delete(selection[0])
            self.ip_listbox.insert(selection[0], f"{ip_text} ({display_name})")
            
            self.status_var.set(f"Updated name for {ip_text}: {new_name if new_name else 'No Name'}")
            dialog.destroy()
        
        def cancel_edit():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_name).pack(side=tk.LEFT, padx=(0, 15))  # Increased padding
        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side=tk.LEFT)
        
        # Bind Enter key to save
        dialog.bind('<Return>', lambda e: save_name())
        dialog.bind('<Escape>', lambda e: cancel_edit())
    
    def open_settings_dialog(self):
        """Open the settings dialog"""
        SettingsDialog(self.root, self)
    
    def browse_log_file(self):
        """Browse for log file location"""
        filename = filedialog.asksaveasfilename(
            title="Select Log File",
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.log_file_var.set(filename)


class SettingsDialog:
    """Settings dialog for configuration parameters"""
    
    def __init__(self, parent, config_editor):
        self.parent = parent
        self.config_editor = config_editor
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("PingTest Settings")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Create widgets
        self.create_widgets()
        
        # Load current values
        self.load_current_values()
        
        # Bind Escape key to close
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
    
    def create_widgets(self):
        """Create the settings dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PingTest Settings", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Ping Interval
        ttk.Label(main_frame, text="Ping Interval (seconds):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.interval_entry = ttk.Entry(main_frame, textvariable=self.config_editor.interval_var, width=15)
        self.interval_entry.grid(row=1, column=1, sticky=tk.W, padx=(15, 0), pady=5)
        
        # Ping Count
        ttk.Label(main_frame, text="Ping Count per Check:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.count_entry = ttk.Entry(main_frame, textvariable=self.config_editor.count_var, width=15)
        self.count_entry.grid(row=2, column=1, sticky=tk.W, padx=(15, 0), pady=5)
        
        # Timeout
        ttk.Label(main_frame, text="Timeout (seconds):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.timeout_entry = ttk.Entry(main_frame, textvariable=self.config_editor.timeout_var, width=15)
        self.timeout_entry.grid(row=3, column=1, sticky=tk.W, padx=(15, 0), pady=5)
        
        # Total Runtime
        ttk.Label(main_frame, text="Total Runtime (seconds, 0=indefinite):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.runtime_entry = ttk.Entry(main_frame, textvariable=self.config_editor.runtime_var, width=15)
        self.runtime_entry.grid(row=4, column=1, sticky=tk.W, padx=(15, 0), pady=5)
        
        # Log File
        ttk.Label(main_frame, text="Log File:").grid(row=5, column=0, sticky=tk.W, pady=5)
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=5)
        log_frame.columnconfigure(0, weight=1)
        
        self.log_file_entry = ttk.Entry(log_frame, textvariable=self.config_editor.log_file_var)
        self.log_file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(log_frame, text="Browse", command=self.browse_log_file).grid(row=0, column=1)
        
        # Note about timestamping
        timestamp_note = ttk.Label(main_frame, text="Note: A timestamp will be automatically added to the log filename for each run", 
                                   font=("Arial", 8), foreground="gray")
        timestamp_note.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(30, 0))
        
        ttk.Button(button_frame, text="OK", command=self.dialog.destroy).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=1)
    
    def load_current_values(self):
        """Load current configuration values into the dialog"""
        # Values are already loaded via the StringVar references
        pass
    
    def browse_log_file(self):
        """Browse for log file location"""
        filename = filedialog.asksaveasfilename(
            title="Select Log File",
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.config_editor.log_file_var.set(filename)


def main():
    """Main function"""
    root = tk.Tk()
    
    # Set application icon if available
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    app = ConfigEditor(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
