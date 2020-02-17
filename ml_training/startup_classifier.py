import pandas as pd
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


top_df = pd.read_csv('/home/igor/ml/result_top_1500_cleaned.csv')
bot_df = pd.read_csv('/home/igor/ml/result_bottom_1500_cleaned.csv')
med_df = pd.read_csv('/home/igor/ml/result_medium_1500_cleaned.csv')

test_top = top_df.drop(['country'], axis=1).fillna('')
test_bot = bot_df.drop(['country'], axis=1).fillna('')
med_test = med_df.drop(['country'], axis=1).fillna('')

labels = pd.Series(['fast'] * test_top.shape[0] + ['slow'] * test_bot.shape[0])


#  MODEL 1: DECISION TREE AND CountVectorizer
combo_df = test_top.append(test_bot)
vectorizer = CountVectorizer(stop_words='english')


# all_text = pd.Series().append([test[i] for i in test.T])
# print(all_text)
# print(all_text.head(10))

# a = 1
# for i in combo_df.T:
#     if a < 6:
#         print(combo_df.T[i])
#         # print(type(test.T[i]))
#         for j in combo_df.T[i]:
#             print(j)
#             print(type(j))
#         a += 1
#     else:
#         break

vectorizer.fit(combo_df.description)
# print(vectorizer.vocabulary_)

training_vectors = vectorizer.transform(combo_df.description)

testing_vectors = vectorizer.transform(med_test.description)

# MODEL 2: DECISION TREE AND CountVectorizer + TfidfTransformer
tfidf_transformer = TfidfTransformer()
trans_train = tfidf_transformer.fit_transform(training_vectors)
trans_test = tfidf_transformer.fit_transform(testing_vectors)

classifier = tree.DecisionTreeClassifier()
classifier.fit(trans_train, labels)
predictions = classifier.predict(trans_test)

with open('result_tfid.txt', 'w') as f:
    for pred in enumerate(predictions):
        f.write('{}: {}\n'.format(med_test.hash[pred[0]], pred[1]))



