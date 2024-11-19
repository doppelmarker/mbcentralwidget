import widgets as wd
import requests
from bs4 import BeautifulSoup
from datetime import timedelta


def fetch_server_data():
    url = "http://www.mnbcentral.net/"
    response = requests.get(url)

    server_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'example'})

        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            server_info = {
                'Server Name': cells[0].text.strip(),
                'Module': cells[1].text.strip(),
                'Game Type': cells[2].text.strip(),
                'Map': cells[3].text.strip(),
                'Region': cells[4].text.strip(),
                'Current Players': int(cells[5].text.strip()),
                'Max Players': int(cells[6].text.strip()),
                'Password': cells[7].text.strip(),
            }
            server_data.append(server_info)

    server_data.sort(key=lambda s: s["Current Players"], reverse=True)
    return server_data


widget = wd.Widget()
layout = widget.large_layout

for server in fetch_server_data()[:12]:
    server_text = wd.Text(
        text=f"{server['Server Name']} - {server['Current Players']}",
        font=wd.Font("AmericanTypewriter", 20),
        color=wd.Color.rgb(0, 0, 0)
    )
    layout.add_row([server_text])

layout.set_background_color(wd.Color.rgb(1, 1, 1))

wd.schedule_next_reload(timedelta(seconds=1))

wd.show_widget(widget)
