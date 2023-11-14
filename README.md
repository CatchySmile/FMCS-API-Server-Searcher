
# FMCS-API-Server-Searcher
A simple Python Script for querying information about Minecraft servers from the findmcserver.com API.

## Table of Contents

- [Download](#Downloads)
- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Installation](#installation)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Downloads
GUI Version (**RECCOMENDED**) --> [FMCS-Searcher.GUI.v2.1.zip](https://github.com/CatchySmile/FMCS-API-Server-Searcher/files/13345030/FMCS-Searcher.GUI.v2.1.zip) <--

NOGUI Version --> [FMCS-Searcher.NO.GUI.v1.5.zip](https://github.com/CatchySmile/FMCS-API-Server-Searcher/files/13345041/FMCS-Searcher.NO.GUI.v1.5.zip) <--

GUI + NOGUI Version --> [FMCS-Searcher.NOGUI+GUI.v2.1.zip](https://github.com/CatchySmile/FMCS-API-Server-Searcher/files/13345029/FMCS-Searcher.NOGUI%2BGUI.v2.1.zip) <--

## Introduction

This Python script retrieves information about Minecraft servers using the findmcserver.com API. It provides detailed information about each server, including server ID, name, IP address, port, description and more.

## Features

Query Minecraft server information based on a search terms & Sorting.

Print detailed information about each server, including the following :

- Server ID
- Server Name
- IP Address
- Java Port
- Java Ip
- Bedrock Port
- Bedrock Ip
- Max Players
- Online Players
- If its Featured
- Short Description
- Logo/Icon link
- Featured Image link
- Background Image link
- Server Location
- Server Badges
- Server Language
- Servers Keywords
- If its a Gamer Safe Service
- Total Votes
- Total Votes in Last 30 days
## Usage

Download & Run the release file OR do the following :

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/CatchySmile/FMCS-API-Server-Searcher/
   cd minecraft-server-api-client
   ```
**Install Dependencies:**
```py
pip install -r requirements.txt
```
**Run the script**
```py
python minecraft_server_client.py
```
## Installation
- Install python 3.9.10 or newer.

```bash
  git clone https://github.com/CatchySmile/FMCS-API-Server-Searcher/
cd minecraft-server-api-client
pip install -r requirements.txt
```

## Configuration
Please Note : Only configure the NOGUI Version if necessary, Aswell as that, the GUI Version has a API Key input, so do not worry about configuration.

- Open FMCS-Searcher v1.5 in a text editor. **ONLY IF NEEDED**
- Replace the empty string in hdr['Ocp-Apim-Subscription-Key'] with your API key. **ONLY IF NEEDED**
A Subscription-Key isnt needed currently, but that may change one day.

## Contributing
If you would like to contribute to the project, feel free to open issues or submit pull requests. Your contributions are welcome!
