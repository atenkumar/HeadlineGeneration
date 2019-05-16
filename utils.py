import pandas as pd

def read_txt(path):
    """Read new line seperated text file into list"""
    with open(path, 'r') as f:
        return f.read().splitlines()
        
def write_txt(path, _list):
    """Write list into new line seperated text file"""
    with open(path, 'w') as f:
        for line in _list:
            f.write('{}\n'.format(line))
            

def save_text_helper(list):
        text_holder = ""
        for sent in list:
            text_holder = text_holder + sent + "|"             
        text_holder = text_holder[0:len(text_holder)-1]
        return text_holder

def save_clean_helper(list):
    text_holder = ""
    for sent in list:
        text_holder = text_holder + sent + "|"             
    text_holder = text_holder[0:len(text_holder)-1]
    return text_holder
    
def save_espn(df, path, sep='|'):
    df['text'] = df['text'].apply(lambda x: save_text_helper(x))
    df['cleanText'] = df['cleanText'].apply(lambda x: save_clean_helper(x))
    df.to_csv(path, index = False)
        
def load_espn(path, tokenize_cols=['text', 'cleanText'], sep='|'):
    df = pd.read_csv(path)
    for col in tokenize_cols:
        df[col] = df[col].apply(lambda x: x.split(sep))
    return df