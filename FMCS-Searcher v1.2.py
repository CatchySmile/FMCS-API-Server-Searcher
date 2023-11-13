import urllib.request, json

def print_server_info(server):
    print(f"Server ID: {server.get('id', 'N/A')}")
    print(f"Server Name: {server.get('name', 'N/A')}")
    print(f"IP Address: {server.get('javaAddress', 'N/A')}")
    print(f"Java Port: {server.get('javaPort', 'N/A')}")
    print(f"Bedrock Port: {server.get('bedrockPort', 'N/A')}")
    print(f"Max Players: {server.get('currentMaxPlayers', 'N/A')}")
    print(f"Online Players: {server.get('currentOnlinePlayers', 'N/A')}")
    print(f"Is Featured: {server.get('isFeatured', 'N/A')}")
    print(f"Short Description: {server.get('shortDescription', 'N/A')}")
    
    icon_image = server.get('iconImage', {})
    print(f"Icon Image Link: {icon_image.get('url', 'N/A') if icon_image else 'N/A'}")
    
    locations = server.get('serverLocation', [])
    print(f"Location: {', '.join([location.get('name', 'N/A') for location in locations]) if locations else 'N/A'}")
    
    badges = server.get('serverBadges', [])
    print(f"Badges: {', '.join([badge.get('name', 'N/A') for badge in badges]) if badges else 'N/A'}")
    
    languages = server.get('serverLanguage', [])
    print(f"Language: {', '.join([language.get('name', 'N/A') for language in languages]) if languages else 'N/A'}")
    
    keywords = server.get('serverTags', [])
    print(f"Keywords: {', '.join([keyword.get('name', 'N/A') for keyword in keywords]) if keywords else 'N/A'}")

    print("------")

try:
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
                print_server_info(server)
        else:
            print("Unexpected response format.")
    else:
        print(f"Error: {response.getcode()} - {response.read().decode('utf-8')}")
except Exception as e:
    print(e)
