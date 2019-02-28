
# coding: utf-8

# # Extract articles from ESPN.com
# 
# Requirements:
# 
# * beautifulsoup4  (4.6.0)

# In[2]:


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


# In[1]:


page_link = 'http://www.espn.com/nfl/story/_/id/25824920/angry-new-orleans-saints-fans-file-lawsuits-put-billboards'

page_response = requests.get(page_link, timeout = 5)

page_content = BeautifulSoup(page_response.content, "html.parser")

textContent = []
for i in range(0, 26):
    paragraphs = page_content.find_all("p")[i].text
    textContent.append(paragraphs)
    
for i in textContent:
    print (i)


# In[4]:


def pprint(soup):# pretty print
    print(soup.prettify())


# In[5]:


html_page =  requests.get("http://www.espn.com/nfl/team/_/name/mia/miami-dolphins")
soup = BeautifulSoup(html_page.content, "lxml")


# In[6]:


# we know that all article links are in the 'article' tag
articles = [art for art in soup.find_all('article') if 'data-id' in art.attrs.keys()] # remove extraneous articles
print(len(articles))


# In[7]:


for art in articles:
    print('---'*30)
    print(art['class'])
    print(art.a['class'])


# In[8]:


article = articles[0]
for child in article.children:
    print(child.name)
print()
pprint(article)


# In[9]:


article_info = {}

#if article['class'] = ['news-feed-item', 'news-feed-story-package']:
    
for child in article.children:
    if child.name == 'a':
        article_info['class'] = child['class'][0]
        article_info['data-id'] = child['data-id']
        article_info['url'] = child['data-popup-href']
        article_info['sport'] = child['data-sport']
    if child.name == 'div':
        for span in child.div.div.children: # should be a timestap and author span tag
            if 'timestamp' in span['class']: # Beautiful soup always makes the class a list (NOT a string)
                article_info['timestamp'] = span.string
            elif 'author' in span['class']:
                article_info['author'] = span.string

article_info


# In[10]:


def extract_articles(soup, teamname): 
    articles = [art for art in soup.find_all('article') if 'data-id' in art.attrs.keys()]

    articles_list = []
    for idx, article in enumerate(articles):
        try:
            if 'story-link' in article.a['class']: # should be ['news-feed-item', 'news-feed-story-package']
                article_info = {}
                article_info['teamname'] = teamname
                for child in article.children:
                    if child.name == 'a':
                        article_info['class'] = child['class'][0]
                        article_info['data-id'] = child['data-id']
                        article_info['url'] = child['data-popup-href']
                        article_info['sport'] = child['data-sport']
                    if child.name == 'div':
                        for span in child.div.div.children: # should be a timestap and author span tag
                            if 'timestamp' in span['class']: # Beautiful soup always makes the class a list (NOT a string)
                                article_info['timestamp'] = span.string
                            elif 'author' in span['class']:
                                article_info['author'] = span.string
                                articles_list.append(article_info)
                    
        except e:
            print('*** {}: {}'.format(idx, e))
                            
      
    
    # convert list of dictionaries into dataframe
    df = pd.DataFrame(articles_list)
    return df

def get_df_from_teamname_link(link):
    teamname = link.split('/')[-1] # grab top link (ex 'buffalo-bills')
    html_page =  requests.get(link)
    soup = BeautifulSoup(html_page.content, 'lxml')
    df = extract_articles(soup, teamname)
    return df

def get_df_from_teamname_links(link_list):
    list_of_dfs = []
    for link in link_list:
        print('Teampage: {}'.format(link))
        teamname = link.split('/')[-1] # grab top link (ex 'buffalo-bills')
        html_page =  requests.get(link)
        soup = BeautifulSoup(html_page.content, 'lxml')
        df = extract_articles(soup, teamname)
        list_of_dfs.append(df)
        
    dfs = pd.concat(list_of_dfs)
    print("Dropping NaN and duplicates")
    dfs = dfs.drop("NaN")
    dfs.drop_duplicates('data-id')
    
    return dfs


# In[11]:


links= ["http://www.espn.com/nfl/team/_/name/buf/buffalo-bills",
        "http://www.espn.com/nfl/team/_/name/mia/miami-dolphins",
        "http://www.espn.com/nfl/team/_/name/cle/cleveland-browns",
        "http://www.espn.com/nfl/team/_/name/ne/new-england-patriots",
        "http://www.espn.com/nfl/team/_/name/nyj/new-york-jets",
        "http://www.espn.com/nfl/team/_/name/dal/dallas-cowboys",
        "http://www.espn.com/nfl/team/_/name/nyg/new-york-giants",
        "http://www.espn.com/nfl/team/_/name/phi/philadelphia-eagles",
        "http://www.espn.com/nfl/team/_/name/wsh/washington-redskins",
        "http://www.espn.com/nfl/team/_/name/bal/baltimore-ravens",
        "http://www.espn.com/nfl/team/_/name/cin/cincinnati-bengals",
        "http://www.espn.com/nfl/team/_/name/cle/cleveland-browns",
        "http://www.espn.com/nfl/team/_/name/pit/pittsburgh-steelers",
        "http://www.espn.com/nfl/team/_/name/chi/chicago-bears",
        "http://www.espn.com/nfl/team/_/name/det/detroit-lions",
        "http://www.espn.com/nfl/team/_/name/gb/green-bay-packers",
        "http://www.espn.com/nfl/team/_/name/min/minnesota-vikings",
        "http://www.espn.com/nfl/team/_/name/hou/houston-texans",
        "http://www.espn.com/nfl/team/_/name/ind/indianapolis-colts",
        "http://www.espn.com/nfl/team/_/name/jax/jacksonville-jaguars",
        "http://www.espn.com/nfl/team/_/name/ten/tennessee-titans",
        "http://www.espn.com/nfl/team/_/name/atl/atlanta-falcons",
        "http://www.espn.com/nfl/team/_/name/car/carolina-panthers",
        "http://www.espn.com/nfl/team/_/name/no/new-orleans-saints",
        "http://www.espn.com/nfl/team/_/name/tb/tampa-bay-buccaneers",
        "http://www.espn.com/nfl/team/_/name/den/denver-broncos",
        "http://www.espn.com/nfl/team/_/name/kc/kansas-city-chiefs",
        "http://www.espn.com/nfl/team/_/name/lac/los-angeles-chargers",
        "http://www.espn.com/nfl/team/_/name/oak/oakland-raiders",
        "http://www.espn.com/nfl/team/_/name/ari/arizona-cardinals",
        "http://www.espn.com/nfl/team/_/name/lar/los-angeles-rams",
        "http://www.espn.com/nfl/team/_/name/sf/san-francisco-49ers",
        "http://www.espn.com/nfl/team/_/name/sea/seattle-seahawks",
        ]

dfs = get_df_from_teamname_links(links)

dfs


# In[14]:


export_csv = dfs.to_csv(r'C:\Users\atenk\Documents\ISM\HeadlineGeneration\ESPN_football.csv', index=False)

