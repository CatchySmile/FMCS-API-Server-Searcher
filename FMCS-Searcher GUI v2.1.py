import tkinter as tk
from tkinter import scrolledtext, ttk
import urllib.request
import json
import logging

# Configure logging
logging.basicConfig(filename='FMCS-output.log', level=logging.INFO)

class App:
    def __init__(self, master):
        self.master = master
        master.title("FindMcServers GUI")
        master.configure(bg='#2c3e50')  # Background color

        style = ttk.Style()
        style.configure('TButton', foreground='#333333', background='#555555', font=('Helvetica', 12))
        style.configure('TLabel', foreground='#ffffff', background='#2c3e50', font=('Helvetica', 12))
        style.configure('TCheckbutton', foreground='#ffffff', background='#2c3e50', font=('Helvetica', 12))
        style.configure('Horizontal.TProgressbar', troughcolor='#2c3e50', background='#3498db')

        self.log_var = tk.BooleanVar()
        self.log_var.set(False)  # Default to not logging

        self.label = ttk.Label(master, text="Enter the server search term:")
        self.label.grid(row=0, column=0, rowspan=1, padx=15, pady=10, sticky='w')

        self.search_entry = ttk.Entry(master, font=('Helvetica', 10))
        self.search_entry.grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky='ew')
        self.search_entry.bind("<Return>", self.search)  # Bind Enter key press to search function

        self.search_button = ttk.Button(master, text="Search", command=self.search)
        self.search_button.grid(row=0, column=0, rowspan=3, padx=15, pady=10, sticky='ew')

        self.log_checkbox = ttk.Checkbutton(master, text="Log results to FMCS-output.log instead of console", variable=self.log_var)
        self.log_checkbox.grid(row=0, column=0, rowspan=4, padx=15, pady=10, sticky='w')

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=100, height=33, font=('Helvetica', 10), bg='#34495e', fg='#ffffff')
        self.output_text.grid(row=0, column=4, rowspan=5, padx=15, pady=20, sticky='nsew')

        # Add a new entry for API key
        self.api_key_entry = ttk.Entry(master, show='*')  # Mask the API key with '*'
        self.api_key_entry.grid(row=3, column=0, padx=15, pady=10, sticky='ew')
        ttk.Label(master, text="API Key:").grid(row=3, column=0, padx=15, pady=10, sticky='w')

        # Dropdown menu for selecting search API
        self.api_options = [
            "https://findmcserver.com/api/servers?pageNumber=0&pageSize=15000&sortBy=random&keywords=",
            "^ | - ^ Default Sort ^ - | ^",
            "https://findmcserver.com/api/servers?pageNumber=0&pageSize=150000&sortBy=players_desc&keywords=",
            "^ | - ^ Players High to Low Sort ^ - | ^",
            "https://findmcserver.com/api/servers?pageNumber=0&pageSize=150000&sortBy=players_asc&keywords=",
            "^ | - ^ Players Low to High Sort ^ - | ^",
            "https://findmcserver.com/api/servers?pageNumber=0&pageSize=15&sortBy=name_desc&keywords=",
            "^ | - ^ A-Z Sort ^ - | ^",
            "https://findmcserver.com/api/servers?pageNumber=0&pageSize=15&sortBy=name_asc&keywords=",
            "^ | - ^ Z-A Sort ^ - | ^",
        ]
        self.api_var = tk.StringVar()
        self.api_var.set(self.api_options[0])
        self.api_dropdown = ttk.Combobox(master, textvariable=self.api_var, values=self.api_options)
        self.api_dropdown.grid(row=4, column=0, padx=15, pady=10, sticky='ew')

        # Configure grid weights to make the console expand with the window
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1)
        master.grid_columnconfigure(3, weight=1)

    def search(self, event=None):
        search_term = self.search_entry.get()
        log_enabled = self.log_var.get()

        # Retrieve the API key from the entry
        api_key = self.api_key_entry.get()

        # Retrieve the selected API from the dropdown
        api_url = self.api_var.get()

        self.output_text.delete(1.0, tk.END)  # Clear previous output
        search_servers(search_term, log_enabled, api_key, api_url, self.output_text)

def print_server_info(server, log_enabled, output_widget):
    output = []
    output.append("===================================")
    output.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    output.append("===================================")
    output.append(f"| - Server ID - | : {server.get('id', 'N/A')}")
    output.append(f"| - Server Name - | : {server.get('name', 'N/A')}")
    output.append("-----------------------------------")
    output.append(f"| - Default IP Address - | : {server.get('javaAddress', 'N/A')}")
    output.append(f"| - Java Port - | : {server.get('javaPort', 'N/A')}")
    output.append(f"| - Java Address - | : {server.get('javaAddress', 'N/A')}")
    output.append("-----------------------------------")
    output.append(f"| - Bedrock Port - | : {server.get('bedrockPort', 'N/A')}")
    output.append(f"| - Bedrock Address - | : {server.get('bedrockAddress', 'N/A')}")
    output.append("-----------------------------------")
    output.append(f"| - Max Players - | : {server.get('currentMaxPlayers', 'N/A')}")
    output.append(f"| - Online Players - | : {server.get('currentOnlinePlayers', 'N/A')}")
    output.append(f"| - Is Featured - | : {server.get('isFeatured', 'N/A')}")
    output.append(f"| - Short Description - | : {server.get('shortDescription', 'N/A')}")
    output.append(f"| - Total Votes - | : {server.get('votes', 'N/A')}")
    output.append(f"| - Votes Last 30 Days - | : {server.get('votesLast30Days', 'N/A')}")
    output.append(f"| - Gamer Safer Service - | : {server.get('gamerSaferService', 'N/A')}")
    output.append(f"| - Minecraft Version - | : {server.get('version', 'N/A')}")
    output.append(f"| - Server Rules - | : {server.get('rulesUrl', 'N/A')}")
    output.append("-----------------------------------")

    icon_image = server.get('iconImage', {})
    output.append(f"| - Icon Image Link - | : {icon_image.get('url', 'N/A')}" if icon_image else 'N/A')

    background_image = server.get('backgroundImage', {})
    output.append(f"| - Background Image Link - | : {background_image.get('url', 'N/A')}" if background_image else 'N/A')

    featured_image = server.get('featuredImage', {})
    output.append(f"| - Featured Image Link - | : {featured_image.get('url', 'N/A')}" if featured_image else 'N/A')

    output.append("-----------------------------------")

    locations = server.get('serverLocation', [])
    output.append(f"| - Location - | : {', '.join([location.get('name', 'N/A') for location in locations])}" if locations else 'N/A')

    badges = server.get('serverBadges', [])
    output.append(f"| - Badges - | : {', '.join([badge.get('name', 'N/A') for badge in badges])}" if badges else 'N/A')

    languages = server.get('serverLanguage', [])
    output.append(f"| - Language - | : {', '.join([language.get('name', 'N/A') for language in languages])}" if languages else 'N/A')

    keywords = server.get('serverTags', [])
    output.append(f"| - Keywords - | : {', '.join([keyword.get('name', 'N/A') for keyword in keywords])}" if keywords else 'N/A')

    for line in output:
        if log_enabled:
            logging.info(line)
        else:
            output_widget.insert(tk.END, line + '\n')

def search_servers(search_term, log_enabled, api_key, api_url, output_widget):
    try:
        url = api_url + search_term

        hdr = {
            'Cache-Control': 'no-cache',
            'Api-Version': 'v1',
            'Ocp-Apim-Subscription-Key': api_key,
        }

        req = urllib.request.Request(url, headers=hdr)
        req.get_method = lambda: 'GET'
        response = urllib.request.urlopen(req)

        if response.getcode() == 200:
            data = json.loads(response.read())

            if isinstance(data.get('data'), list):
                for server in data['data']:
                    print_server_info(server, log_enabled, output_widget)
            else:
                print("Unexpected response format.")
        else:
            print(f"Error: {response.getcode()} - {response.read().decode('utf-8')}")
    except Exception as e:
        print(e)

root = tk.Tk()
app = App(root)
root.mainloop()
