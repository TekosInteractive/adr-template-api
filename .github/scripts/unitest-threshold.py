from bs4 import BeautifulSoup
import sys

report_file=sys.argv[1]

with open(report_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

report_content = BeautifulSoup(html_content, 'html.parser')

ratio = report_content.find('span', {'class': 'sr-only'})

if ratio:
    value = ratio.text.split('%')[0]
    print(value)
