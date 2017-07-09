from bs4 import BeautifulSoup
import requests, time


url = 'http://downloads.oneplus.net/devices/oneplus-5/'
webhook_url = YOUR_MAKER_WEBHOOK_URL
default_version = ''


def filter_name_from_heading(content):
    heading = content.find('div', {'id': 'heading0'})
    name = heading.findAll('a')[0].string
    return name

def filter_url_from_collapse(content):
    heading = content.find('div', {'id': 'collapse0'})
    link = heading.find('a')
    link = link.get('href')
    return link
def filter_changelog(heading):
    line = heading.find('div', {'class': 'entry'}).text
    return line


while True:
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'lxml')
    panel_content = soup.find('div', {'class': 'panel'})
    check = filter_name_from_heading(panel_content)

    if check != default_version:
        json_dict = {'value1': check, \
                     'value2': filter_url_from_collapse(panel_content), \
                     'value3': filter_changelog(panel_content).replace( \
                         '\n\n', '<br>*****************<br \>').replace(\
                         '\n', '<br>')\
                    }

        print (json_dict)
        requests.post(webhook_url, data=json_dict)

        default_version = check
        print ('Version Change!!')
        print ('Now is {}'.format(default_version))
    else:
        print ('No-Update')

    time.sleep(5)
