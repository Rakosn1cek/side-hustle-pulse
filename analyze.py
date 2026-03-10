import sqlite3
from collections import Counter
import re

def generate_report(common_niches):
    # Mapping your EXACT results to the best 2026 programs
    AFFILIATE_LINKS = {
        "ECOMMERCE": "https://www.shopify.com/affiliates", 
        "MARKETING": "https://www.hubspot.com/partners/affiliates",
        "PRODUCT": "https://printify.com/affiliates/",
        "BUILD": "https://partnerstack.com/", # General tools for builders
        "COMPANY": "https://www.freshbooks.com/affiliates", # Accounting for new companies
    }
    DEFAULT_LINK = "https://partnerstack.com/"

    with open("index.html", "w") as f:
        # Adding a dark-mode 'terminal' style to the site
        f.write("""
        <html><head><style>
            body { font-family: 'Courier New', monospace; background: #1a1b26; color: #a9b1d6; padding: 40px; }
            .card { background: #24283b; padding: 20px; margin: 15px 0; border-radius: 4px; border: 1px solid #414868; }
            .niche-title { color: #7aa2f7; font-size: 1.2em; font-weight: bold; }
            .count { color: #bb9af7; }
            a { color: #73daca; text-decoration: none; border: 1px solid #73daca; padding: 5px 10px; border-radius: 3px; }
            a:hover { background: #73daca; color: #1a1b26; }
        </style></head><body>
        """)
        
        f.write("<h1>[SIDE-HUSTLE PULSE: MARKET ANALYSIS]</h1>")
        f.write("<p style='color: #9ece6a;'>Status: Data mined from r/smallbusiness, r/ecommerce, r/entrepreneur</p>")
        f.write("<p>I built this tool to help me decide which free Linux projects to fund next based on market demand.</p>")
        
        for niche, count in common_niches:
            link = AFFILIATE_LINKS.get(niche.upper(), DEFAULT_LINK)
            f.write(f"<div class='card'>")
            f.write(f"<div class='niche-title'>TARGET: {niche.upper()}</div>")
            f.write(f"<p>Activity Level: <span class='count'>{count} signals</span> detected.</p>")
            f.write(f"<a href='{link}' target='_blank'>ACCESS RECOMMENDED TOOLS</a>")
            f.write(f"</div>")
            
        f.write("</body></html>")

def analyze_trends():
    conn = sqlite3.connect('pulse.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM trends')
    rows = cursor.fetchall()
    
    # Aggressive filtering to remove "meta" talk and common verbs
    STOP_WORDS = {
        'side', 'hustle', 'with', 'that', 'make', 'looking', 'ideas', 'online',
        'money', 'need', 'some', 'from', 'help', 'what', 'have', 'this', 'your',
        'want', 'doing', 'extra', 'start', 'best', 'anyone', 'know', 'hustles',
        'work', 'time', 'actually', 'months', 'would', 'part', 'years', 'most',
        'month', 'advice', 'income', 'automated', 'tedious', 'find', 'take',
        'good', 'free', 'into', 'just', 'more', 'they', 'than', 'them', 'their',
        'hiring', 'someone', 'recommendation', 'software', 'expensive', 'business',
        'small', 'week', 'industry', '2026', 'news', 'recap', 'about', 'should',
        'businesses', 'when', 'here', 'getting', 'built', 'there', 'first', 
        'happened', 'build', 'about', 'being', 'could', 'their', 'very', 'which'
    }

    all_text = " ".join([row[0].lower() for row in rows])
    words = re.findall(r'\b\w{4,}\b', all_text)
    filtered_words = [w for w in words if w not in STOP_WORDS]
    
    # ONLY show the top 5 targets for a cleaner website
    common = Counter(filtered_words).most_common(5)
    
    if common:
        print("\n--- CLEANED NICHES ---")
        for niche, count in common:
            print(f"{niche.upper()}: {count} mentions")
        generate_report(common)
    else:
        print("❌ No keywords left. Try adjusting STOP_WORDS.")

    conn.close()

if __name__ == "__main__":
    analyze_trends()
