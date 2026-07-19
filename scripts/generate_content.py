import pandas as pd
import json

# ==============================================================================
# Instructions:
# 1. Install required packages: pip install pandas openpyxl google-generativeai
# 2. Get a Gemini API Key from https://aistudio.google.com/
# 3. Set the API key below or as an environment variable
# 4. Run this script to generate `data.js` for the web app!
# ==============================================================================

import google.generativeai as genai

# TODO: Set your API key here
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# Use the pro model for better creative writing and accuracy
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def process_excel():
    excel_path = "../Morice_Trafford_Vocabulary_V2_8Week_351.xlsx"
    df = pd.read_excel(excel_path)
    
    # Group by Learn Day
    days = df.groupby('Learn Day')
    
    vocabulary_data = {}
    
    for day, group in days:
        print(f"Processing Day {day}...")
        
        words = group['Word'].tolist()
        meanings = group['Simple meaning'].tolist()
        
        # We need yesterday's words for the story constraint
        yesterday_words = []
        if day > 1 and (day - 1) in vocabulary_data:
            yesterday_words = [w['word'] for w in vocabulary_data[day - 1]['words']]
        
        prompt = f"""
        You are an expert English teacher for Year 5 students preparing for the 11+ Exam.
        
        Today's vocabulary words: {words}
        Their meanings: {meanings}
        Yesterday's words to optionally include: {yesterday_words[:5]}
        
        Task 1: Write a funny, engaging short story (about 50-80 words) that a Year 5 student can read in 5 minutes.
        - MUST include all of today's vocabulary words.
        - If possible, include a few of yesterday's words.
        - Wrap the vocabulary words in **bold** like **this**.
        - Keep the surrounding text simple and easy to understand.
        
        Task 2: Provide details for each of today's words.
        For each word, provide:
        - pronunciation (e.g. /əˈbʌndənt/)
        - simpleMeaning (use the provided meaning or similar)
        - emoji (a single emoji that best represents the word)
        - synonyms (list of 3 synonyms)
        - antonyms (list of 3 antonyms)
        - sentences (list of 3 example sentences using the word)
        
        Format the output as a strictly valid JSON object matching this structure:
        {{
            "story": "...",
            "words": [
                {{
                    "word": "word1",
                    "pronunciation": "...",
                    "simpleMeaning": "...",
                    "emoji": "🌟",
                    "synonyms": ["...", "...", "..."],
                    "antonyms": ["...", "...", "..."],
                    "sentences": ["...", "...", "..."]
                }}
            ]
        }}
        """
        
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        
        try:
            day_data = json.loads(response.text)
            vocabulary_data[int(day)] = day_data
        except Exception as e:
            print(f"Error parsing JSON for Day {day}: {e}")
            print("Response was:", response.text)
            
        # Optional: Break early if you only want to test a few days
        # if day == 3: break
            
    # Output to data.js
    output_path = "../data/data.js"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("const vocabularyData = ")
        json.dump(vocabulary_data, f, indent=2, ensure_ascii=False)
        f.write(";")
        
    print(f"Success! Generated data.js at {output_path}")

if __name__ == "__main__":
    process_excel()
