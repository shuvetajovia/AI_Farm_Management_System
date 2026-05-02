import codecs
import json
import os

def run():
    try:
        with codecs.open('fixtures.json', 'r', encoding='utf-16') as f:
            data = f.read()
        
        # Verify it's actually valid JSON by parsing it
        json_data = json.loads(data)
        
        with codecs.open('fixtures_utf8.json', 'w', encoding='utf-8') as f:
            f.write(data)
        print("Success: fixtures_utf8.json created.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
