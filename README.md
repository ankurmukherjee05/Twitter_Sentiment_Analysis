# Twitter Sentiment Analysis

Twitter Sentiment Analysis is a tool which streams tweets on any chosen topic, and performs a positive/negative sentiment analysis on the results. The sentiment analysis is performed using the supervised machine learning model of Naive Bayes and a training set of 10,000 tweets. 

## Getting Started
Twitter Sentiment Analysis consists of two Python files. "Tweet_Stream.py" and "NB_Classifier.py". To run these Python 3 will need to installed and configured. A Twitter developer account will also need to be created as the tokens provided will will need to be added into the code as instructed in the comments. 

### Prerequisites
1. Twitter developer account - This can be created at the following link: https://developer.twitter.com/en/apply-for-access
Some basic questions will need to be answered which will influence the length of time it will take for Twitter to respond to a users access request.

2. Python 3.0 - Python 3.0 (or greater) will need to be installed and configured on your machine. The programs provided in this repository can be run through both the command line or a GUI such as Spyder.

3. Various libraries will need to be imported as well.

## Deployment
Once a user ha both the prerequisites above, deployment of this tool can be done in 2 steps:

#### Step 1:
  First the tweets to be analyzed will need to be collected. This can be done with the file "Tweet_Stream.py". Open the file and enter the access and consumer keys that were provided by Twitter after approval of the developer account. Once this is complete go to line 15-17 to the variables "tweet_limit" and "tracklist". These values will set the number of tweets desired and the topic respectively. tweet_limit will need to be a num, and tracklist can be both a single string or a list of strings. Please reference the Tweepy documentation on streaming to for any inquiries. The print statement on line 35 can be commented out when pulling large exports as it will slow down the program. It has been added as a useful tool for troubelshooting issues that may arise and verification that the program is working as expected. Aftet running the program the results will be stored in file "stream_data.csv" which will be created in the current working directory. The name of this file can be modified on line 58.

#### Step 2:
  Now that the tweets have been collected the Naive Bayes model needs to be trained and used. No modifications need to be made to this file. The only prerequisites needed for this is to verify that the "stream_data.csv" is in the working directory. If the file which contains the streamed tweets has a different name this can be changed on line 89. Once the classification is complete the count of positive and negative tweets are displayed in the console.
