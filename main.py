import csv
import requests
from bs4 import BeautifulSoup

print('Какой жанр вас интересует? Отвечайте на ангийском, пожалуйста')
tags = input().split(",")
print('Какая минимальная оценка?')
Rating = (input())
print('Какое минимальное количество оценок?')
number_of_votes = (input())
print('Каких предупреждений не должно быть?')
content_warning = input().split(",")
print('Какой тип?')
type_anime = input()
print('Какое минимально количество эпизодов?')
episodes = input()
print('Закончено? Если да то ответье True, если нет то False')
finish = input()
first = []
second = []
a = []

with open('anime.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for i in tags:
            if i in row['Tags']:
                first.append(row)
    for row in first:
        if row['Rating Score'] == 'Unknown':
            continue
        if float(Rating) <= float(row['Rating Score']):
            second.append(row)
    first = []
    for row in second:
        if row['Number Votes'] == 'Unknown':
            continue
        if float(number_of_votes) <= float(row['Number Votes']):
            first.append(row)
    second = []
    for row in first:
        for i in content_warning:
            if i in row['Content Warning']:
                first.remove(row)
                break
    for row in first:
        if row['Type'] == 'Unknown':
            continue
        if row['Type'] == type_anime:
            second.append(row)
    first = []
    for row in second:
        if row['Episodes'] == 'Unknown':
            continue
        if float(episodes) <= float(row['Episodes']):
            first.append(row)
    second = []
    for row in first:
        if row['Finished'] == finish:
            second.append(row)
    first = []
    for row in second:
        a = [float(row['Rating Score']), (row['Name']), (row['Url'])]
        first.append(a)
first.sort()
first.reverse()

f = open('answer.txt', 'w', encoding='utf-8')
for i in range(min(5, len(first))):
    response = requests.get(first[i][2])
    soup = BeautifulSoup(response.text, 'html.parser')
    img = requests.get("https://www.anime-planet.com/" + soup.find('img', class_='screenshots')['src'])
    img_file = open(str(i + 1) + '.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    f.write(first[i][2] + ': ' + first[i][1] + '\n')
for i in range(min(5, len(first)), len(first)):
    f.write(first[i][2] + ': ' + first[i][1] + '\n')
f.close()
