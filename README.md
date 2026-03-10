# Side-Hustle Pulse

A lightweight, data-driven market research engine. This tool mines high-intent signals from business communities to identify current market "pain points," helping developers build products that solve real problems.

> **Goal:** This project generates affiliate revenue to fund my independent open-source projects for the Linux community.

## How it Works
1. **Scrape:** `pulse.py` uses the Reddit JSON API to find recent discussions in `r/smallbusiness`, `r/ecommerce`, and `r/entrepreneur`.
2. **Analyze:** `analyze.py` filters common noise using an aggressive stop-word list to reveal specific business niches (e.g., Logistics, Marketing, SaaS).
3. **Deploy:** The analyzer automatically generates a dark-mode `index.html` report ready for hosting on GitHub Pages.

## Tech Stack
- **Language:** Python 3
- **Database:** SQLite3 (local file-based storage)
- **Deployment:** GitHub Pages (Static HTML)
- **OS:** Optimized for Arch Linux

## Quick Start
```bash
# Clone the repo
git clone [https://github.com/Rakosn1cek/side-hustle-pulse.git](https://github.com/Rakosn1cek/side-hustle-pulse.git)
cd side-hustle-pulse

# Set up environment
python -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4

# Run the engine
python3 pulse.py
python3 analyze.py
