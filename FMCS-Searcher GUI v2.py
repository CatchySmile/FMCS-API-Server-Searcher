import tkinter as tk
from tkinter import scrolledtext, ttk
import urllib.request
import json
import logging

# Configure logging
logging.basicConfig(filename='FMCS-output.log', level=logging.INFO)

def print_server_info(server, log_enabled, output_widget):
    output = []
    output.append("-----------------------------------")
    output.append("===================================")
    output.append(f"Server ID: {server.get('id', 'N/A')}")
    output.append(f"Server Name: {server.get('name', 'N/A')}")
    output.append("-----------------------------------")
    output.append(f"Default IP Address: {server.get('javaAddress', 'N/A')}")
    output.append(f"Java Port: {server.get('javaPort', 'N/A')}")
    output.append(f"Java Address: {server.get('javaAddress', 'N/A')}")
    output.append("-----------------------------------")
    output.append(f"Bedrock Port: {server.get('bedrockPort', 'N/A')}")
    output.append(f"Bedrock Address: {server.get('bedrockAddress', 'N/A')}")
    output.append("-----------------------------------")
    output.append(f"Max Players: {server.get('currentMaxPlayers', 'N/A')}")
    output.append(f"Online Players: {server.get('currentOnlinePlayers', 'N/A')}")
    output.append(f"Is Featured: {server.get('isFeatured', 'N/A')}")
    output.append(f"Short Description: {server.get('shortDescription', 'N/A')}")
    output.append(f"Total Votes: {server.get('votes', 'N/A')}")
    output.append(f"Votes Last 30 Days: {server.get('votesLast30Days', 'N/A')}")
    output.append(f"Gamer Safer Service: {server.get('gamerSaferService', 'N/A')}")
    output.append("-----------------------------------")

    icon_image = server.get('iconImage', {})
    output.append(f"Icon Image Link: {icon_image.get('url', 'N/A')}" if icon_image else 'N/A')

    background_image = server.get('backgroundImage', {})
    output.append(f"Background Image Link: {background_image.get('url', 'N/A')}" if background_image else 'N/A')

    featured_image = server.get('featuredImage', {})
    output.append(f"Featured Image Link: {featured_image.get('url', 'N/A')}" if featured_image else 'N/A')
    
    output.append("-----------------------------------")

    locations = server.get('serverLocation', [])
    output.append(f"Location: {', '.join([location.get('name', 'N/A') for location in locations])}" if locations else 'N/A')

    badges = server.get('serverBadges', [])
    output.append(f"Badges: {', '.join([badge.get('name', 'N/A') for badge in badges])}" if badges else 'N/A')

    languages = server.get('serverLanguage', [])
    output.append(f"Language: {', '.join([language.get('name', 'N/A') for language in languages])}" if languages else 'N/A')

    keywords = server.get('serverTags', [])
    output.append(f"Keywords: {', '.join([keyword.get('name', 'N/A') for keyword in keywords])}" if keywords else 'N/A')

    output.append("===================================")

    for line in output:
        if log_enabled:
            logging.info(line)
        else:
            output_widget.insert(tk.END, line + '\n')

def search_servers(search_term, log_enabled, output_widget):
    try:
        url = f"https://findmcserver.com/api/servers?pageNumber=0&pageSize=15000&sortBy=random&keywords={search_term}"

        hdr = {
            'Cache-Control': 'no-cache',
            'Api-Version': 'v1',
            'Ocp-Apim-Subscription-Key': '',  # Only if needed
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

class App:
    def __init__(self, master):
        self.master = master
        master.title("FindMcServers GUI")
        master.configure(bg='#333333')

        style = ttk.Style()
        style.configure('TButton', foreground='#333333', background='#555555')
        style.configure('TLabel', foreground='#ffffff', background='#333333')
        style.configure('TCheckbutton', foreground='#ffffff', background='#333333')
        style.configure('Horizontal.TProgressbar', troughcolor='#333333', background='#aaaaaa')

        self.log_var = tk.BooleanVar()
        self.log_var.set(False)  # Default to not logging

        self.label = ttk.Label(master, text="Enter the server search term:")
        self.label.pack(pady=10)

        self.search_entry = ttk.Entry(master)
        self.search_entry.pack(pady=10)

        self.log_checkbox = ttk.Checkbutton(master, text="Log results to FMCS-output.log instead of console", variable=self.log_var)
        self.log_checkbox.pack(pady=10)

        self.search_button = ttk.Button(master, text="Search", command=self.search)
        self.search_button.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=33, font=('Helvetica', 8), bg='#333333', fg='#ffffff')
        self.output_text.pack(pady=20)

    def search(self):
        search_term = self.search_entry.get()
        log_enabled = self.log_var.get()
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        search_servers(search_term, log_enabled, self.output_text)

root = tk.Tk()
app = App(root)
root.mainloop()
