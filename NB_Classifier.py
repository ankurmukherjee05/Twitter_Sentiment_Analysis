from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import NaiveBayesClassifier
import csv
import re, string, random

#Function to remove punctuation, stop words, and unnecessary charachters
def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

#Function to create generator for cleaned token list
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

#Function to create generator for dictionary of token list
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":

    #Save tweet samples to train and test model
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    #Stop words used to clean token list
    stop_words = stopwords.words('english')

    #Tokenize positive and negative tweets
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    #Clean positive tweet token list
    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    #Clean negative tweet token list
    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    #Create positive and negative datasets
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    #Create train dataset
    train_data = dataset

    classifier = NaiveBayesClassifier.train(train_data)

    #Read csv file of streamted tweets
    custom_tweets = []
    with open('stream_data.csv') as csvFile:
        rd = csv.reader(csvFile)
        for row in rd:
            custom_tweets.append(str(row))
    
    tokenized_custom_tweets = []
    cleaned_custom_token_list = []
    classifications = []
    
    for tweet in custom_tweets:
        tokenized_custom_tweets.append(word_tokenize(tweet))

    for token in tokenized_custom_tweets:
        cleaned_custom_token_list.append(remove_noise(token, stop_words))
    #custom_tokens = remove_noise(word_tokenize(custom_tweets))

    #print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))
    custom_tokens_for_model = get_tweets_for_model(cleaned_custom_token_list)
    
    for tokenizedTweet in cleaned_custom_token_list:
       classifications.append(classifier.classify(dict([token, True] for token in tokenizedTweet)))
 
  
    #View classification results
    pos_count = 0
    neg_count = 0
    
    for result in classifications:
        if (result == 'Positive'):
            pos_count += 1
        else:
            neg_count += 1
            
    print("Total Tweet Count: ", len(custom_tweets))
    print("Positive Tweets: ", pos_count)
    print("Negative Tweets: ", neg_count)
