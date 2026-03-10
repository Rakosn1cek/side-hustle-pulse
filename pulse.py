import sqlite3
import requests
import time

HEADERS = {'User-Agent': 'linux:side-hustle-pulse-v2:0.1 (by /u/yourusername)'}

def init_db():
    conn = sqlite3.connect('pulse.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subreddit TEXT,
            keyword TEXT,
            title TEXT,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def scrape_and_save(subreddit, keyword):
    conn = init_db()
    cursor = conn.cursor()
    
    # We target the specific subreddit and the keyword
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&restrict_sr=on&sort=new"
    
    print(f"[{subreddit}] Searching for: {keyword}...")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                p_data = post['data']
                title = p_data['title']
                permalink = f"https://reddit.com{p_data['permalink']}"
                
                cursor.execute('''
                    INSERT INTO trends (subreddit, keyword, title, url) 
                    VALUES (?, ?, ?, ?)
                ''', (subreddit, keyword, title, permalink))
            
            conn.commit()
            print(f"  -> Found {len(posts)} items.")
        else:
            print(f"  -> Error {response.status_code}")
    except Exception as e:
        print(f"  -> Connection error: {e}")
    
    conn.close()
    time.sleep(2) # Be kind to the API

if __name__ == "__main__":
    # Subreddits where people spend money or have problems
    subs = ["smallbusiness", "entrepreneur", "ecommerce", "logistics"]
    
    # Keywords that indicate "I need a solution"
    keys = ["too expensive", "tedious", "hiring someone", "recommendation", "software for"]
    
    for s in subs:
        for k in keys:
            scrape_and_save(s, k)
