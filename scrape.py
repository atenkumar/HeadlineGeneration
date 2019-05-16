""" Scrape Tools specific to ESPN"""

import requests
import pandas as pd


##### Article URL tools #####

def extract_articles(soup, teamname):
    """Extracts all article urls and other metadata from soup object.
     
    Returns df
    """
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
