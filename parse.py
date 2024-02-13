from bs4 import BeautifulSoup
import csv

# Path to your HTML file within the html folder
html_file_path = 'html/changelist.html'  # Adjust the file name as necessary

# Read the HTML content from the file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Prepare data list
data = []

# Find all panel elements which contain the changelist details
panels = soup.find_all(class_="panel panel-history")

for panel in panels:
    changelist_id = panel.find('a', rel="nofollow").get_text(strip=True).strip('#')
    date_time = panel.find('time')['datetime']
    items = panel.find_all('li')
    
    for item in items:
        change_type = item['class'][0] if item.has_attr('class') else 'Unknown'
        
        # Skip adding the entry if the change type is 'checklist'
        if change_type == 'checklist':
            continue
        
        description = item.get_text(strip=True)
        previous_change_id = None
        current_change_id = None
        change_links = item.find_all('a', class_="history-link")
        if change_links:
            previous_change_id = change_links[0].get_text(strip=True).strip('#')
            current_change_id = change_links[-1].get_text(strip=True).strip('#')
        
        data.append([changelist_id, change_type, description, previous_change_id, current_change_id, date_time])

# Specify the column titles
columns = ['Changelist ID', 'Change Type', 'Description', 'Previous Change ID', 'Current Change ID', 'Date & Time']

# Write data to CSV
csv_file = "changes.csv"
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(data)

print(f"CSV file '{csv_file}' has been created with {len(data)} records.")
