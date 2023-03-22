from bs4 import BeautifulSoup
import requests
import re
import csv
from prettytable import PrettyTable

# Prompt the user for the URL
url = input("Enter a URL: ")

# Fetch the web page with requests
response = requests.get(url)

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links in the HTML
links = []
for link in soup.find_all('a'):
    link_data = {}
    link_data['tag'] = 'a'
    link_data['text'] = link.get_text()
    link_data['href'] = link.get('href')
    links.append(link_data)

# Find all images in the HTML
for img in soup.find_all('img'):
    img_data = {}
    img_data['tag'] = 'img'
    img_data['text'] = img.get('alt')
    img_data['href'] = img.get('src')
    links.append(img_data)

# Save the links to a file named after the website's domain
filename = re.search('https?://([^/]+)/', url).group(1) + ".csv"
with open(filename, "w", newline='') as outfile:
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerow(["Tag", "Text", "URL"])
    for link in links:
        writer.writerow([link['tag'], link['text'], link['href']])

# Display the links in a table
table = PrettyTable()
table.field_names = ["Tag", "Text", "URL"]
for link in links:
    table.add_row([link['tag'], link['text'], link['href']])
print(f"{len(links)} links have been collected:")
print(table)
print(f"The links have been saved to {filename}.")
