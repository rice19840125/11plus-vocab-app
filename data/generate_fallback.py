import pandas as pd
import json
import math

def process_excel():
    excel_path = "../../Morice_Trafford_Vocabulary_V2_8Week_351.xlsx"
    df = pd.read_excel(excel_path)
    
    # Clean NaN values
    df = df.fillna("")
    
    # Group by Learn Day
    days = df.groupby('Learn Day')
    
    vocabulary_data = {}
    
    for day, group in days:
        try:
            day = int(day)
        except ValueError:
            continue
            
        words_list = []
        word_names = []
        for _, row in group.iterrows():
            word = str(row.get('Word', '')).strip()
            if not word:
                continue
                
            meaning = str(row.get('Simple meaning', '')).strip()
            syn = str(row.get('Synonym', '')).strip()
            ant = str(row.get('Antonym', '')).strip()
            sentence = str(row.get('Example sentence', '')).strip()
            
            words_list.append({
                "word": word,
                "pronunciation": "/.../",
                "simpleMeaning": meaning,
                "emoji": "✨",
                "synonyms": [syn] if syn else [],
                "antonyms": [ant] if ant else [],
                "sentences": [sentence] if sentence else []
            })
            word_names.append(f"**{word}**")
            
        if not words_list:
            continue
            
        # Create a generic story containing the words
        story = f"Today's amazing vocabulary adventure includes learning about {', '.join(word_names)}. Let's discover what they mean!"
        
        vocabulary_data[day] = {
            "story": story,
            "words": words_list
        }

    # Output to data.js
    output_path = "data.js"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("const vocabularyData = ")
        json.dump(vocabulary_data, f, indent=2, ensure_ascii=False)
        f.write(";")
        
    print(f"Success! Generated data.js with {len(vocabulary_data)} days.")

if __name__ == "__main__":
    process_excel()
