from bs4 import BeautifulSoup
import pandas as pd
import requests

anime_name = []
anime_year = []
anime_description = []
test = []
anime_genre = []
anime_views = []
number_of_episodes = []
number_of_episodes1 = []
anime_url = []
image = []
anime_comments = []
novelty = []
MAX_NUM_PAGES = 57
GOOD_RESPONSE_STATUS = 200

for page_num in range(1, MAX_NUM_PAGES):
    url = f'https://animestars.org/page/{page_num}/'
    try:
        response = requests.get(url, timeout=20)
    except:
        break
    if response.status_code != GOOD_RESPONSE_STATUS:
        break
    soup = BeautifulSoup(response.content, 'html.parser')
    anime_test = soup.find_all('div', 'short-c')
    anime_name_onpage = soup.find_all('div', 'short-text')
    anime_name1 = [cousine.a.text for cousine in anime_name_onpage]
    anime_name1 = anime_name1[:-1]

    anime_r = [cousine.text for cousine in anime_test]
    anime_year1 = [int(a[:4]) for a in anime_r]

    anime_genre1 = [list(map(str.strip, (a[6:].split(",")))) for a in anime_r]

    anime_test7 = soup.find_all('div', 'short-i img-box')
    novelty1 = [1 if
                str((cousine.find_all('div',
                                      'short\
                                      -ong'))) == '[<div class\
                ="short-ong">Новинка</div>]'
                else 0 for
                cousine in anime_test7]
    novelty1 = novelty1[:-1]

    anime_test1 = soup.find_all('div', 'm-views flex-col ps-link')
    anime_views1 = [int(cousine.div.text.replace(' ', '')) for
                    cousine in anime_test1]
    anime_views1 = anime_views1[:-1]

    anime_test2 = soup.find_all('div', 'short-series')
    number_of_episodes1 = [(cousine.text.split()[0])
                           if cousine.text[-1] == 'я'
                           else (cousine.text[2:].split()[0][1:])
                           for cousine in anime_test2]
    number_of_episodes1 = number_of_episodes1[:-1]

    anime_test4 = soup.find_all('div', 'm-meta ic-l')
    anime_comments1 = [int(cousine.text.replace('\n', ''))
                       for cousine
                       in anime_test4]
    anime_comments1 = anime_comments1[:-1]

    anime_test5 = soup.find_all('div', 'short-d')
    anime_description1 = [cousine.text for cousine in anime_test5]
    anime_description1 = anime_description1[:-1]

    anime_test6 = soup.find_all('div', 'short-i img-box')
    image1 = ["https://animestars.org" + cousine.img['data-src']
              for cousine
              in anime_test6]
    image1 = image1[:-1]

    anime_test3 = soup.find_all('div', 'ps-link ic-l')
    anime_url1 = [cousine.a['href'] for cousine in anime_name_onpage]
    anime_url1 = anime_url1[:-1]
    anime_name += anime_name1
    novelty += novelty1
    anime_year += anime_year1
    anime_genre += anime_genre1
    anime_views += anime_views1
    anime_description += anime_description1
    anime_comments += anime_comments1
    number_of_episodes += number_of_episodes1
    anime_url += anime_url1
    image += image1
df_anime = pd.DataFrame(
    {
        'anime_name': anime_name,
        'anime_year': anime_year,
        'anime_genre': anime_genre,
        'anime_views': anime_views,
        'number_of_episodes': number_of_episodes,
        'anime_url': anime_url,
        'anime_comments': anime_comments,
        'anime_description': anime_description,
        'image': image,
        'ongoing': novelty
    }
)
df_anime = df_anime.drop(df_anime[df_anime["n\
umber_of_episodes"] == 'льм'].index).reset_index(drop=True)
df_anime = df_anime.drop(df_anime[df_anime["n\
umber_of_episodes"] == 'xx'].index).reset_index(drop=True)
indexes_match_queries = df_anime.apply(lambda row: 'По\
лнометражный фильм' not in row['anime_genre'], axis=1, )
df_anime = df_anime[indexes_match_queries].reset_index(drop=True)
df_anime["number_of_episodes"] = pd.to_numeric(df_anime["number_of_episodes"])
df_anime.to_csv('anime.csv', index=False)

print(df_anime)
