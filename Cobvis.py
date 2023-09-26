from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def print_banner():
    banner = r"""
 ██████╗ ██████╗ ██████╗ ██╗   ██╗██╗███████╗
██╔════╝██╔═══██╗██╔══██╗██║   ██║██║██╔════╝
██║     ██║   ██║██████╔╝██║   ██║██║███████╗
██║     ██║   ██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚██████╗╚██████╔╝██████╔╝ ╚████╔╝ ██║███████║
 ╚═════╝ ╚═════╝ ╚═════╝   ╚═══╝  ╚═╝╚══════╝
    """
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "Author: OFD5, Please use this tool for Security Purposes." + Style.RESET_ALL)



def main():
    print_banner()

    user_url = str(input('[+] Enter Target URL To Scan: '))
    urls = deque([user_url])

    scraped_urls = set()
    emails = set()

    count = 0
    try:
        while len(urls):
            count += 1
            if count == 100:
                break
            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)

            path = url[:url.rfind('/') + 1] if '/' in parts.path else url

            print('[%d] Processing %s' % (count, url))
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", response.text, re.I))
            emails.update(new_emails)

            soup = BeautifulSoup(response.text, features="lxml")

            for anchor in soup.find_all("a"):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if link not in urls and link not in scraped_urls:
                    urls.append(link)
    except KeyboardInterrupt:
        print('[-] Closing!')

    for mail in emails:
        print(mail)

if __name__ == "__main__":
    main()

    

