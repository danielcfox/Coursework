
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 3
# 
# In this assignment you will explore text message data and create models to predict if a message is spam or not. 

# In[1]:

import pandas as pd
import numpy as np

spam_data = pd.read_csv('spam.csv')

spam_data['target'] = np.where(spam_data['target']=='spam',1,0)
spam_data.head(10)


# In[2]:

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(spam_data['text'], 
                                                    spam_data['target'], 
                                                    random_state=0)


# ### Question 1
# What percentage of the documents in `spam_data` are spam?
# 
# *This function should return a float, the percent value (i.e. $ratio * 100$).*

# In[9]:

def answer_one():
    
    return np.mean(spam_data['target']) * 100 #Your answer here


# In[10]:

answer_one()


# ### Question 2
# 
# Fit the training data `X_train` using a Count Vectorizer with default parameters.
# 
# What is the longest token in the vocabulary?
# 
# *This function should return a string.*

# In[15]:

from sklearn.feature_extraction.text import CountVectorizer

def answer_two():
    
    maxtok = ""
    vect = CountVectorizer().fit(X_train)
    for tok in vect.get_feature_names():
        if len(tok) > len(maxtok):
            maxtok = tok
    
    return maxtok #Your answer here


# In[16]:

answer_two()


# ### Question 3
# 
# Fit and transform the training data `X_train` using a Count Vectorizer with default parameters.
# 
# Next, fit a fit a multinomial Naive Bayes classifier model with smoothing `alpha=0.1`. Find the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[17]:

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score

def answer_three():
    
    vect = CountVectorizer().fit(X_train)
    X_train_vect = vect.transform(X_train)
    
    clf = MultinomialNB(alpha=0.1).fit(X_train_vect, y_train)
    pred = clf.predict(vect.transform(X_test))
    
    return roc_auc_score(y_test, pred) #Your answer here


# In[18]:

answer_three()


# ### Question 4
# 
# Fit and transform the training data `X_train` using a Tfidf Vectorizer with default parameters.
# 
# What 20 features have the smallest tf-idf and what 20 have the largest tf-idf?
# 
# Put these features in a two series where each series is sorted by tf-idf value and then alphabetically by feature name. The index of the series should be the feature name, and the data should be the tf-idf.
# 
# The series of 20 features with smallest tf-idfs should be sorted smallest tfidf first, the list of 20 features with largest tf-idfs should be sorted largest first. 
# 
# *This function should return a tuple of two series
# `(smallest tf-idfs series, largest tf-idfs series)`.*

# In[66]:

from sklearn.feature_extraction.text import TfidfVectorizer

def answer_four():
    
    vect_tf = TfidfVectorizer().fit(X_train)
    X_train_vect = vect_tf.transform(X_train)
    feature_names = np.array(vect_tf.get_feature_names())
    sorted_tfidf_index = X_train_vect.max(0).toarray()[0].argsort()
    
    swords = feature_names[sorted_tfidf_index[:20]]
    svals = X_train_vect.max(0).toarray()[0][sorted_tfidf_index[:20]]
    
    small_df = pd.DataFrame({'words' : swords, 'vals' : svals})
    small_df.sort_values(['vals', 'words'], ascending=True, inplace=True)
    small_series = pd.Series(small_df['vals'].values, index=small_df['words'], name=None)
    
    lwords = feature_names[sorted_tfidf_index[-20:]]
    lvals = X_train_vect.max(0).toarray()[0][sorted_tfidf_index[-20:]]
    
    large_df = pd.DataFrame({'words' : lwords, 'vals' : lvals})
    large_df.sort_values(['vals', 'words'], ascending=[False, True], inplace=True)
    large_series = pd.Series(large_df['vals'].values, index=large_df['words'], name=None)

    return small_series, large_series #Your answer here


# In[67]:

answer_four()


# ### Question 5
# 
# Fit and transform the training data `X_train` using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than **3**.
# 
# Then fit a multinomial Naive Bayes classifier model with smoothing `alpha=0.1` and compute the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[69]:

def answer_five():
    
    vect = TfidfVectorizer(min_df=3).fit(X_train)
    
    X_train_vect = vect.transform(X_train)
    X_test_vect = vect.transform(X_test)
    
    clf = MultinomialNB(alpha=0.1).fit(X_train_vect, y_train)
    pred = clf.predict(X_test_vect)
    
    return roc_auc_score(y_test, pred) #Your answer here


# In[70]:

answer_five()


# ### Question 6
# 
# What is the average length of documents (number of characters) for not spam and spam documents?
# 
# *This function should return a tuple (average length not spam, average length spam).*

# In[81]:

def answer_six():
    spam_data['textlen'] = spam_data['text'].str.len()
    spam_df = spam_data[spam_data['target'] == 1]
    nospam_df =  spam_data[spam_data['target'] == 0]
    
    return np.mean(nospam_df['textlen']), np.mean(spam_df['textlen']) #Your answer here


# In[82]:

answer_six()


# <br>
# <br>
# The following function has been provided to help you combine new features into the training data:

# In[83]:

def add_feature(X, feature_to_add):
    """
    Returns sparse feature matrix with added feature.
    feature_to_add can also be a list of features.
    """
    from scipy.sparse import csr_matrix, hstack
    return hstack([X, csr_matrix(feature_to_add).T], 'csr')


# ### Question 7
# 
# Fit and transform the training data X_train using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than **5**.
# 
# Using this document-term matrix and an additional feature, **the length of document (number of characters)**, fit a Support Vector Classification model with regularization `C=10000`. Then compute the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[88]:

from sklearn.svm import SVC

def answer_seven():
    
    vect = TfidfVectorizer(min_df=5).fit(X_train)
    
    X_train_vect = vect.transform(X_train)
    X_test_vect = vect.transform(X_test)
    
    X_train_vect = add_feature(X_train_vect, X_train.str.len())
    X_test_vect = add_feature(X_test_vect, X_test.str.len())
    
    clf = SVC(C=10000).fit(X_train_vect, y_train)
    pred = clf.predict(X_test_vect)
    
    return roc_auc_score(y_test, pred) #Your answer here


# In[89]:

answer_seven()


# ### Question 8
# 
# What is the average number of digits per document for not spam and spam documents?
# 
# *This function should return a tuple (average # digits not spam, average # digits spam).*

# In[101]:

def countdigits(x):
    return(sum(int(c.isdigit()) for c in x))

def answer_eight():
    for index, row in spam_data.iterrows():
        spam_data.at[index, 'numdigits'] = countdigits(spam_data.at[index, 'text'])
    spam_df = spam_data[spam_data['target'] == 1]
    nospam_df =  spam_data[spam_data['target'] == 0]

    
    return np.mean(nospam_df['numdigits']), np.mean(spam_df['numdigits']) #Your answer here


# In[102]:

answer_eight()


# ### Question 9
# 
# Fit and transform the training data `X_train` using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than **5** and using **word n-grams from n=1 to n=3** (unigrams, bigrams, and trigrams).
# 
# Using this document-term matrix and the following additional features:
# * the length of document (number of characters)
# * **number of digits per document**
# 
# fit a Logistic Regression model with regularization `C=100`. Then compute the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[107]:

from sklearn.linear_model import LogisticRegression

def countdigits(x):
    return(sum(int(c.isdigit()) for c in x))

def answer_nine():
    
    X_train_digitlen = list(map(countdigits, X_train))
    X_test_digitlen = list(map(countdigits, X_test))

    vect = TfidfVectorizer(min_df=5, ngram_range=(1,3)).fit(X_train)
    
    X_train_vect = vect.transform(X_train)
    X_test_vect = vect.transform(X_test)
    
    X_train_vect = add_feature(X_train_vect, X_train.str.len())
    X_test_vect = add_feature(X_test_vect, X_test.str.len())
    
    X_train_vect = add_feature(X_train_vect, X_train_digitlen)
    X_test_vect = add_feature(X_test_vect, X_test_digitlen)
    
    clf = LogisticRegression(C=100).fit(X_train_vect, y_train)
    pred = clf.predict(X_test_vect)
    return roc_auc_score(y_test, pred) #Your answer here


# In[108]:

answer_nine()


# ### Question 10
# 
# What is the average number of non-word characters (anything other than a letter, digit or underscore) per document for not spam and spam documents?
# 
# *Hint: Use `\w` and `\W` character classes*
# 
# *This function should return a tuple (average # non-word characters not spam, average # non-word characters spam).*

# In[111]:

def countnonwordchars(x):
    return(sum(int(not c.isalnum() and not c == '_') for c in x))

def answer_ten():
    
    for index, row in spam_data.iterrows():
        spam_data.at[index, 'numnonwordchars'] = countnonwordchars(spam_data.at[index, 'text'])
    spam_df = spam_data[spam_data['target'] == 1]
    nospam_df =  spam_data[spam_data['target'] == 0]
    
    return np.mean(nospam_df['numnonwordchars']), np.mean(spam_df['numnonwordchars']) #Your answer here


# In[112]:

answer_ten()


# ### Question 11
# 
# Fit and transform the training data X_train using a Count Vectorizer ignoring terms that have a document frequency strictly lower than **5** and using **character n-grams from n=2 to n=5.**
# 
# To tell Count Vectorizer to use character n-grams pass in `analyzer='char_wb'` which creates character n-grams only from text inside word boundaries. This should make the model more robust to spelling mistakes.
# 
# Using this document-term matrix and the following additional features:
# * the length of document (number of characters)
# * number of digits per document
# * **number of non-word characters (anything other than a letter, digit or underscore.)**
# 
# fit a Logistic Regression model with regularization C=100. Then compute the area under the curve (AUC) score using the transformed test data.
# 
# Also **find the 10 smallest and 10 largest coefficients from the model** and return them along with the AUC score in a tuple.
# 
# The list of 10 smallest coefficients should be sorted smallest first, the list of 10 largest coefficients should be sorted largest first.
# 
# The three features that were added to the document term matrix should have the following names should they appear in the list of coefficients:
# ['length_of_doc', 'digit_count', 'non_word_char_count']
# 
# *This function should return a tuple `(AUC score as a float, smallest coefs list, largest coefs list)`.*

# In[131]:

def countdigits(x):
    return(sum(int(c.isdigit()) for c in x))

def countnonwordchars(x):
    return(sum(int(not c.isalnum() and not c == '_') for c in x))

def answer_eleven():
   
    X_train_digitlen = list(map(countdigits, X_train))
    X_test_digitlen = list(map(countdigits, X_test))
    
    X_train_nwclen = list(map(countnonwordchars, X_train))
    X_test_nwclen = list(map(countnonwordchars, X_test))

    vect = CountVectorizer(min_df=5, ngram_range=(2,5), analyzer='char_wb').fit(X_train)
    
    X_train_vect = vect.transform(X_train)
    X_test_vect = vect.transform(X_test)
    
    X_train_vect = add_feature(X_train_vect, X_train.str.len())
    X_test_vect = add_feature(X_test_vect, X_test.str.len())
    
    X_train_vect = add_feature(X_train_vect, X_train_digitlen)
    X_test_vect = add_feature(X_test_vect, X_test_digitlen)
    
    X_train_vect = add_feature(X_train_vect, X_train_nwclen)
    X_test_vect = add_feature(X_test_vect, X_test_nwclen)
    
    clf = LogisticRegression(C=100).fit(X_train_vect, y_train)
    pred = clf.predict(X_test_vect)
    
    fn = np.array(vect.get_feature_names())
    fn_added = np.array(['length_of_doc', 'digit_count', 'non_word_char_count'])
    fn_all = np.concatenate((fn, fn_added))
    
    sorted_coef = clf.coef_[0].argsort()
    smallest_coef = list(fn_all[sorted_coef[:10]])
    largest_coef = list(fn_all[sorted_coef[:-11:-1]])

    aucscore = roc_auc_score(y_test, pred)
    
    return aucscore, smallest_coef, largest_coef #Your answer here


# In[132]:

answer_eleven()


# In[ ]:



