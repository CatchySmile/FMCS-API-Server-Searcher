import urllib.request
import json
import logging

# Configure logging
logging.basicConfig(filename='FMCS-output.log', level=logging.INFO)

def print_server_info(server, log_enabled):
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

    if log_enabled:
        for line in output:
            logging.info(line)
    else:
        for line in output:
            print(line)

try:
    log_results = input("Log results to FMCS-output.log instead of console? (.log allows unlimited results) (Y/N): ").upper() == 'Y'
    
    if log_results:
        logging.info("Logging enabled.")
    
    search = input("Enter the server search term: ")

    url = f"https://findmcserver.com/api/servers?pageNumber=0&pageSize=15000&sortBy=random&keywords={search}"

    hdr = {
        # Request headers
        'Cache-Control': 'no-cache',
        'Api-Version': 'v1',
        'Ocp-Apim-Subscription-Key': '',  # Only if needed
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)

    if response.getcode() == 200:
        data = json.loads(response.read())
        
        # Check if the response is a list
        if isinstance(data.get('data'), list):
            for server in data['data']:
                print_server_info(server, log_results)
        else:
            print("Unexpected response format.")
    else:
        print(f"Error: {response.getcode()} - {response.read().decode('utf-8')}")
except Exception as e:
    print(e)
