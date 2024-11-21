import requests
from bs4 import BeautifulSoup

def get_html_table(url):
  """Get and return html for the table from the google docs url"""
  response = requests.get(url)
  html = response.content
  html_soup = BeautifulSoup(html, 'html.parser')
  return html_soup.find('table')

def get_print_table(html_table):
  """Convert the html table into the organized list"""
  data = [] # used to hold all of the unicode characters and their x and y values
  highest_x = 0 # used to keep track of the highest x value found
  highest_y = 0 # used to keep track of the highest y value found
  for row in html_table.find_all("tr"):
    row_data = [] # used to hold the data for each unicode character and its x and y values
    for cell in row.find_all(["th", "td"]):
      row_data.append(cell.text.strip())
      if (row_data[0] == "x-coordinate"):
        continue # we skip the first row entirely since it is just headers.  This row is removed below
      if int(row_data[0]) > highest_x:
        highest_x = int(row_data[0])
      if len(row_data) == 3:
        if int(row_data[2]) > highest_y:
          highest_y = int(row_data[2])
    data.append(row_data)
  data.remove(data[0]) # this is the header row.  It is not needed
  highest_x = highest_x + 1 # adding one since list indexes start at 0
  highest_y = highest_y + 1 # adding one since list indexes start at 0
  print_table = [[' ' for space in range (highest_x)] for space in range (highest_y)]
  for row in data: 
    print_table[highest_y - 1 - int(row[2])][int(row[0])] = row[1] # the y column is inverted (requiring a -1) to get the higher y's first
  return print_table

def print_message(url):
  html_table = get_html_table(url)
  print_table = get_print_table(html_table)
  for row in print_table: # finish printing each row to the console
    for element in row:
      print(element, end="")
    print()
  
print_message("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")