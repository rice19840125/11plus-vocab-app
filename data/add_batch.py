import json
import re

def update_data(new_days):
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON part
    json_str = content.replace('const vocabularyData = ', '')
    json_str = json_str.rsplit(';', 1)[0]
    
    data = json.loads(json_str)
    
    # Update with new days
    for k, v in new_days.items():
        data[str(k)] = v
        
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write('const vocabularyData = ')
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write(';')
    print("Updated data.js with new days.")

new_batch = {
  3: {
    "story": "The explorer felt a **slight** shiver as he stood before the **vast** desert. Water was **scarce**, which made him feel **anxious** and **apprehensive**. Suddenly, he was **astonished** to see a hidden oasis. His mood became **cheerful** as he found a **substantial** amount of fruit!",
    "words": [
      {
        "word": "scarce", "pronunciation": "/skɛəs/", "simpleMeaning": "hard to find or available in small amounts", "emoji": "🏜️",
        "synonyms": ["rare", "infrequent", "lacking"], "antonyms": ["plentiful", "abundant", "common"],
        "sentences": ["Food was scarce during the winter.", "Water is scarce in the desert.", "Tickets for the concert were scarce."]
      },
      {
        "word": "slight", "pronunciation": "/slaɪt/", "simpleMeaning": "small in degree", "emoji": "🤏",
        "synonyms": ["small", "minor", "tiny"], "antonyms": ["major", "significant", "huge"],
        "sentences": ["I have a slight headache.", "There is a slight chance of rain.", "She noticed a slight movement in the bushes."]
      },
      {
        "word": "substantial", "pronunciation": "/səbˈstænʃəl/", "simpleMeaning": "large in amount or importance", "emoji": "💰",
        "synonyms": ["considerable", "significant", "sizable"], "antonyms": ["insignificant", "minor", "small"],
        "sentences": ["They won a substantial amount of money.", "There was a substantial increase in sales.", "The house suffered substantial damage."]
      },
      {
        "word": "vast", "pronunciation": "/vɑːst/", "simpleMeaning": "extremely large", "emoji": "🌌",
        "synonyms": ["huge", "immense", "enormous"], "antonyms": ["tiny", "small", "minute"],
        "sentences": ["The universe is a vast empty space.", "They own a vast estate.", "A vast crowd gathered for the event."]
      },
      {
        "word": "anxious", "pronunciation": "/ˈæŋkʃəs/", "simpleMeaning": "worried or nervous", "emoji": "😰",
        "synonyms": ["worried", "nervous", "uneasy"], "antonyms": ["calm", "relaxed", "confident"],
        "sentences": ["She felt anxious about her exams.", "He gave an anxious look.", "They were anxious to hear the results."]
      },
      {
        "word": "apprehensive", "pronunciation": "/ˌæprɪˈhɛnsɪv/", "simpleMeaning": "worried that something bad may happen", "emoji": "😟",
        "synonyms": ["anxious", "nervous", "fearful"], "antonyms": ["confident", "calm", "certain"],
        "sentences": ["I am apprehensive about the interview.", "She was apprehensive of the dark.", "He felt apprehensive before the flight."]
      },
      {
        "word": "astonished", "pronunciation": "/əˈstɒnɪʃt/", "simpleMeaning": "very surprised", "emoji": "😲",
        "synonyms": ["amazed", "surprised", "astounded"], "antonyms": ["unsurprised", "expecting", "unimpressed"],
        "sentences": ["I was astonished by the news.", "She looked at him in astonished silence.", "They were astonished at his speed."]
      },
      {
        "word": "cheerful", "pronunciation": "/ˈtʃɪəfʊl/", "simpleMeaning": "noticeably happy and positive", "emoji": "😄",
        "synonyms": ["happy", "joyful", "merry"], "antonyms": ["sad", "gloomy", "miserable"],
        "sentences": ["He is a cheerful person.", "The room had a cheerful atmosphere.", "She gave a cheerful smile."]
      }
    ]
  },
  4: {
    "story": "The **compassionate** teacher noticed Tim was feeling **dejected** and **envious** of the others. She helped him, and soon he felt **content**. He was **eager** to learn and became **delighted** when he scored perfectly! He was so **elated** that he forgot why he was ever **furious**.",
    "words": [
      {
        "word": "compassionate", "pronunciation": "/kəmˈpæʃənət/", "simpleMeaning": "showing care for someone who is suffering", "emoji": "❤️",
        "synonyms": ["caring", "kind", "sympathetic"], "antonyms": ["cruel", "heartless", "uncaring"],
        "sentences": ["She is a compassionate nurse.", "He showed compassionate understanding.", "The organization provides compassionate care."]
      },
      {
        "word": "content", "pronunciation": "/kənˈtɛnt/", "simpleMeaning": "satisfied and peaceful", "emoji": "😌",
        "synonyms": ["satisfied", "happy", "pleased"], "antonyms": ["dissatisfied", "unhappy", "discontented"],
        "sentences": ["He felt content with his life.", "She gave a content sigh.", "I am content to stay at home."]
      },
      {
        "word": "dejected", "pronunciation": "/dɪˈdʒɛktɪd/", "simpleMeaning": "sad and discouraged", "emoji": "😞",
        "synonyms": ["sad", "depressed", "downhearted"], "antonyms": ["cheerful", "happy", "elated"],
        "sentences": ["She looked dejected after the loss.", "He felt dejected and lonely.", "The team was dejected."]
      },
      {
        "word": "delighted", "pronunciation": "/dɪˈlaɪtɪd/", "simpleMeaning": "very pleased", "emoji": "🥰",
        "synonyms": ["pleased", "happy", "glad"], "antonyms": ["disappointed", "sad", "unhappy"],
        "sentences": ["I am delighted to meet you.", "She was delighted with her present.", "They were delighted by the news."]
      },
      {
        "word": "eager", "pronunciation": "/ˈiːɡə/", "simpleMeaning": "very keen to do something", "emoji": "🤩",
        "synonyms": ["keen", "enthusiastic", "impatient"], "antonyms": ["reluctant", "unwilling", "indifferent"],
        "sentences": ["He is eager to start.", "She was eager for success.", "The eager students waited."]
      },
      {
        "word": "elated", "pronunciation": "/ɪˈleɪtɪd/", "simpleMeaning": "extremely happy", "emoji": "🥳",
        "synonyms": ["overjoyed", "thrilled", "ecstatic"], "antonyms": ["miserable", "sad", "depressed"],
        "sentences": ["She was elated by the victory.", "He felt elated and proud.", "The elated crowd cheered."]
      },
      {
        "word": "envious", "pronunciation": "/ˈɛnviəs/", "simpleMeaning": "wanting what another person has", "emoji": "😒",
        "synonyms": ["jealous", "covetous", "desiring"], "antonyms": ["content", "satisfied", "generous"],
        "sentences": ["He was envious of her success.", "She cast an envious glance.", "They were envious of his wealth."]
      },
      {
        "word": "furious", "pronunciation": "/ˈfjʊəriəs/", "simpleMeaning": "extremely angry", "emoji": "😡",
        "synonyms": ["enraged", "angry", "incensed"], "antonyms": ["calm", "pleased", "happy"],
        "sentences": ["He was furious at the mistake.", "She gave a furious reply.", "The furious storm hit the coast."]
      }
    ]
  },
  5: {
    "story": "It was a **gloomy** day, and the dog was **reluctant** to go for a walk. He was **indifferent** to his toys and seemed **hesitant** to move. However, his owner was **optimistic** and threw a ball. The dog felt **sympathetic** to her efforts, forgot he was **resentful**, and was **grateful** for the fun!",
    "words": [
      {
        "word": "gloomy", "pronunciation": "/ˈɡluːmi/", "simpleMeaning": "sad or without hope", "emoji": "🌧️",
        "synonyms": ["dark", "depressing", "dismal"], "antonyms": ["bright", "cheerful", "sunny"],
        "sentences": ["The weather was gloomy.", "He had a gloomy expression.", "She felt gloomy about the future."]
      },
      {
        "word": "grateful", "pronunciation": "/ˈɡreɪtfʊl/", "simpleMeaning": "thankful", "emoji": "🙏",
        "synonyms": ["thankful", "appreciative", "obliged"], "antonyms": ["ungrateful", "unthankful", "unappreciative"],
        "sentences": ["I am grateful for your help.", "She gave a grateful smile.", "We are grateful to be here."]
      },
      {
        "word": "hesitant", "pronunciation": "/ˈhɛzɪtənt/", "simpleMeaning": "slow to act because of uncertainty", "emoji": "🤔",
        "synonyms": ["uncertain", "unsure", "reluctant"], "antonyms": ["certain", "decisive", "confident"],
        "sentences": ["She was hesitant to speak.", "He gave a hesitant answer.", "They were hesitant about the plan."]
      },
      {
        "word": "indifferent", "pronunciation": "/ɪnˈdɪfrənt/", "simpleMeaning": "not interested or concerned", "emoji": "😐",
        "synonyms": ["uncaring", "uninterested", "apathetic"], "antonyms": ["caring", "interested", "enthusiastic"],
        "sentences": ["He was indifferent to the news.", "She gave an indifferent shrug.", "They seemed indifferent to the cold."]
      },
      {
        "word": "optimistic", "pronunciation": "/ˌɒptɪˈmɪstɪk/", "simpleMeaning": "expecting good things to happen", "emoji": "🌈",
        "synonyms": ["positive", "hopeful", "confident"], "antonyms": ["pessimistic", "negative", "hopeless"],
        "sentences": ["She is optimistic about the future.", "He has an optimistic outlook.", "They remained optimistic despite the setback."]
      },
      {
        "word": "reluctant", "pronunciation": "/rɪˈlʌktənt/", "simpleMeaning": "unwilling or not eager", "emoji": "🙅",
        "synonyms": ["unwilling", "hesitant", "resistant"], "antonyms": ["eager", "willing", "enthusiastic"],
        "sentences": ["He was reluctant to leave.", "She gave a reluctant nod.", "They were reluctant participants."]
      },
      {
        "word": "resentful", "pronunciation": "/rɪˈzɛntfʊl/", "simpleMeaning": "angry because something feels unfair", "emoji": "😤",
        "synonyms": ["bitter", "indignant", "offended"], "antonyms": ["forgiving", "content", "happy"],
        "sentences": ["He felt resentful of the rules.", "She gave a resentful look.", "They were resentful about the decision."]
      },
      {
        "word": "sympathetic", "pronunciation": "/ˌsɪmpəˈθɛtɪk/", "simpleMeaning": "showing understanding of another person’s feelings", "emoji": "🤝",
        "synonyms": ["caring", "compassionate", "understanding"], "antonyms": ["unsympathetic", "uncaring", "indifferent"],
        "sentences": ["She was very sympathetic to his problem.", "He gave a sympathetic ear.", "They were sympathetic towards the victims."]
      }
    ]
  }
}

if __name__ == '__main__':
    update_data(new_batch)
