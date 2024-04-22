import os
import nltk
import pandas as pd
from textblob import TextBlob
from nltk.corpus import cmudict

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')

# Load CMU Pronouncing Dictionary for syllable count
cmu_dict = cmudict.dict()

def calculate_metrics(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Calculate polarity and subjectivity scores
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    
    # Calculate average sentence length
    avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)
    
    # Calculate percentage of complex words (words with 3 or more syllables)
    complex_word_count = 0
    syllable_count = 0
    for word in words:
        syllable_count += syllable_count_word(word.lower())
        if syllable_count_word(word.lower()) >= 3:
            complex_word_count += 1
    percentage_complex_words = (complex_word_count / len(words)) * 100
    
    # Calculate Fog Index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    # Calculate average number of words per sentence
    avg_words_per_sentence = len(words) / len(sentences)
    
    # Calculate number of personal pronouns (first and second person pronouns)
    personal_pronouns = sum(tag.startswith('PRP') for (_, tag) in nltk.pos_tag(words))
    
    # Calculate average word length
    avg_word_length = sum(len(word) for word in words) / len(words)
    
    # Return the calculated metrics
    return polarity_score, subjectivity_score, avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, personal_pronouns, avg_word_length

def syllable_count_word(word):
    if word.lower() in cmu_dict:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]])
    else:
        # If word not found in CMU dictionary, estimate syllable count based on length
        return max(1, len(word) / 3)

# Directory where the extracted articles are saved
articles_directory = "article_texts/"

# Create lists to store the computed metrics
data = []

# Iterate over each text file and perform textual analysis
for filename in os.listdir(articles_directory):
    if filename.endswith(".txt"):
        filepath = os.path.join(articles_directory, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            # Calculate metrics for the article text
            polarity_score, subjectivity_score, avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, personal_pronouns, avg_word_length = calculate_metrics(text)
            
            # Store the computed metrics in a dictionary
            row = {
                'URL_ID': filename.split('.')[0],
                # 'URL': '',  # URL can be added if available
                'POSITIVE SCORE': polarity_score,
                'NEGATIVE SCORE': -polarity_score,
                'POLARITY SCORE': polarity_score,
                'SUBJECTIVITY SCORE': subjectivity_score,
                'AVG SENTENCE LENGTH': avg_sentence_length,
                'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
                'FOG INDEX': fog_index,
                'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
                'COMPLEX WORD COUNT': percentage_complex_words,
                'WORD COUNT': len(nltk.word_tokenize(text)),
                'SYLLABLE PER WORD': sum(syllable_count_word(word.lower()) for word in nltk.word_tokenize(text)) / len(nltk.word_tokenize(text)),
                'PERSONAL PRONOUNS': personal_pronouns,
                'AVG WORD LENGTH': avg_word_length
            }
            data.append(row)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)
urls = pd.read_excel('./URL.xlsx')

final_data = pd.merge(df, urls, on='URL_ID')

# Reorder the columns
final_data = final_data[['URL_ID', 'URL'] + [col for col in final_data.columns if col not in ['URL_ID', 'URL']]]

# Save the DataFrame to an Excel file
output_file = "textual_analysis_output.xlsx"
final_data.to_excel(output_file, index=False)
print("Textual analysis output saved to:", output_file)


