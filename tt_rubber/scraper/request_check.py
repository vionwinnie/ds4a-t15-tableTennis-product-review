import requests

#url = "https://stackoverflow.com/questions/24297257/save-html-of-some-website-in-a-txt-file-with-python"
url = "https://www.tabletennisdaily.com/forum/showthread.php?10953-Tenergy-25-compared-to-Tenergy-05"

r = requests.get(url)
with open('../rawData/file.txt', 'w') as file:
    file.write(r.text)
