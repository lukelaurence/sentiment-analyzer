# sentiment-analyzer

** This repository currently consists of 3 parts:

## fullarchivesample
A program that uses Twitter's API to randomly sample Tweets from 2006 to the current day. (Technically 2 days before the current day.)

## sentimentpreprocessing
A program that contains various scripts to facilitate preprocessing of the raw Twitter data into a format optimal for parsing by the Word2vec model, most notably by substituting in instances of multiword vector keys. (Such as substituting in United_States for United States, which would otherwise be parsed as two seperate words.)

## sentimentanalyzer
A program that, given a list of sentiment vectors, (one representing disapproval of Congress, for example, perhaps being represented as as "USA" + "Congress" + "deadlocked" + "wasteful",) parses each Tweet to find how much each aligns with each sentiment, then aggregates this over a certain timeframe to produce human-readable data.

Together, they are able to determine how different sentiments change in relation to each other over time.
