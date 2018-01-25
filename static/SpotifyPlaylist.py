import requests
import bs4
from fake_useragent import UserAgent
ua = UserAgent()
headers = requests.utils.default_headers()
headers.update({'User-Agent': str(ua.chrome)})


r = requests.get('https://www.bbc.co.uk/schedules/p00fzl8v/2017/12/07', headers).content
soup = bs4.BeautifulSoup(r, "html5lib")
soup = soup.find_all('h4')

for i in soup:
    if i.find("span", property="name").get_text() == 'Bob Harris Country':
        for link in i.find_all('a'):
            bob_link = (link.get('href'))
            print(bob_link)

tracklist = requests.get(bob_link, headers).content
hm = requests.get(bob_link, headers).headers

print()


