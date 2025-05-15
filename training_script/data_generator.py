
import random
import pandas as pd

positive_words = ["good", "great", "excellent", "amazing", "fantastic", "wonderful", "happy", "satisfied", "love", "best", "perfect", "highly recommend", "top-notch", "pleased", "fast", "easy", "works", "quality", "value", "service", "on time", "reliable", "efficient", "delightful", "enjoyable", "awesome", "incredible", "outstanding", "superb", "terrific", "positive", "promising", "favorable", "fortuitous", "successful", "thriving", "flourishing", "booming", "leading", "winning", "acclaimed", "admirable", "commendable", "meritorious", "praiseworthy", "remarkable", "spectacular", "splendid", "stellar", "triumphant", "unbeatable"]
negative_words = ["bad", "poor", "terrible", "awful", "horrible", "disappointing", "unsatisfied", "hate", "worst", "broken", "damaged", "late", "slow", "expensive", "useless", "waste", "defective", "faulty", "cheap", "flimsy", "inadequate", "subpar", "inferior", "deficient", "lacking", "limited", "minimal", "scarce", "insufficient", "meager", "paltry", "negligible", "trivial", "unfortunate", "unfavorable", "adverse", "dire", "dreadful", "awful", "terrible", "horrific", "atrocious", "abysmal", "lousy", "crummy", "shoddy", "mediocre", "rotten", "substandard", "wretched", "miserable", "deplorable", "pathetic", "tragic"]
neutral_words = ["okay", "average", "fine", "decent", "acceptable", "so-so", "alright", "normal", "usual", "ordinary", "standard", "typical", "common", "regular", "medium", "moderate", "fair", "passable", "tolerable", "unremarkable", "plain", "simple", "basic", "neutral", "indifferent", "ambivalent", "undecided", "unclear", "vague", "general", "generic", "noncommittal", "impartial", "objective", "unbiased", "unemotional", "apathetic", "detached", "aloof", "reserved", "reticent", "taciturn", "silent", "quiet", "still", "calm", "composed", "collected", "serene", "tranquil"]

def generate_sentence(sentiment: str) -> str:
    length = random.randint(5, 15)
    sentence = []
    for _ in range(length):
        if sentiment == "Positive":
            word = random.choice(positive_words) if random.random() < 0.8 else random.choice(neutral_words)
        elif sentiment == "Negative":
            word = random.choice(negative_words) if random.random() < 0.8 else random.choice(neutral_words)
        else:
            word = random.choice(neutral_words)
        sentence.append(word)
    return " ".join(sentence)

def generate_synthetic_feedback(num_samples=2000) -> pd.DataFrame:
    data = []
    sentiments = ["Positive", "Negative", "Neutral"]
    for _ in range(num_samples):
        sentiment = random.choice(sentiments)
        num_sentences = random.randint(1, 3)
        sentences = [generate_sentence(sentiment) for _ in range(num_sentences)]
        text = " ".join(sentences)
        data.append({"text": text, "sentiment": sentiment})
    return pd.DataFrame(data)
