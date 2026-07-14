import re
import glob
from collections import Counter

stop_words = set([
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "their", "our", "mine", "yours", "hers", "theirs", "ours",
    "this", "that", "these", "those",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "done", "doing",
    "have", "has", "had", "having",
    "a", "an", "the", "and", "but", "or", "so", "if", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "than", "too", "very",
    "can", "will", "just", "don", "should", "now", "would", "could", "im", "ill", "dont",
    "cant", "wont", "thats", "its", "youre", "hes", "shes", "weve", "theyre", "ive", "id",
    "get", "take", "make", "go", "come", "put", "set", "bring", "carry",
    "see", "look", "watch", "hear", "listen", "think", "feel", "know", "say", "tell",
    "good", "bad", "big", "small", "time", "day", "night", "man", "woman", "boy", "girl",
    "yes", "yeah", "ok", "okay", "please", "thank", "thanks", "sorry",
    "what", "who", "which", "whom", "whose", "let", "lets",
    "much", "many", "really", "always", "never", "sometimes", "often", "usually"
])

words = []
files = glob.glob('master/data/month*.js')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        # extract sentences
        matches = re.findall(r'"txt":\s*"([^"]+)"', content)
        for sentence in matches:
            # clean punctuation
            sentence = re.sub(r"[.,?!;:()'\"]", "", sentence.lower())
            for word in sentence.split():
                if word not in stop_words and not word.isnumeric() and len(word) > 1:
                    words.append(word)

counter = Counter(words)
for word, count in counter.most_common(200):
    print(f"{word}")
