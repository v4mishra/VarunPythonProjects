from bs4 import BeautifulSoup
import urllib
import requests





html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())
head_tag = soup.head
print("soup.head = ")
print(head_tag)
print("soup.head.string = ")
print(head_tag.string)
for child in head_tag.descendants:
    print(child)
    

print("********************")



print("soup. title = ")
print(soup.title)
print("printing soup.p tag: ")
print(soup.p)
soup.p.contents
soup.p.getText()

print("printing soup.p's class attribute:")
print(soup.p['class'])

print("lenght of soup.find_all('a') = ")
print(len(soup.find_all('a')))

print("extract links from all href:")
for link in soup.find_all('a'):
    print(link.get('href'))

print("***********finding methods*************")
