import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('requirements.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# remove style and script blocks completely
html = re.sub(r'<style.*?>.*?</style>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r'<script.*?>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)

# very simple regex to remove tags
text = re.sub('<[^>]+>', ' ', html)
# remove multiple spaces/newlines
text = re.sub(r'\s+', ' ', text).strip()
print(text[:3000]) # just print first 3000 chars
