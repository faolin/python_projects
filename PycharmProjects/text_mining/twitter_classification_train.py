'''entraine un modele SVM avec bigram ou unigram + tfidf et le test'''

def remove_stopwords(sentence, stopwords):
    sentencewords = sentence.split()
    resultwords = [word for word in sentencewords if word.lower() not in stopwords]
    result = ' '.join(resultwords)
    return result


def unigram_process(data):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    vectorizer = vectorizer.fit(data)
    return vectorizer


def bigram_process(data):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    vectorizer = vectorizer.fit(data)
    return vectorizer

'''
Example d'utilisation: la data en entrée est déja vectorisée (mono- ou bi-gram)
Xtrain_uni = vectorizer.transform(Xtrain_text)
uni_tfidf_transformer = tfidf_process(Xtrain_uni)
Xtrain_tf_uni = uni_tfidf_transformer.transform(Xtrain_uni)
'''
def tfidf_process(data):
    from sklearn.feature_extraction.text import TfidfTransformer
    transformer = TfidfTransformer()
    transformer = transformer.fit(data)
    return transformer

SOURCE = "/home/francois/Téléchargements/imdb.csv"
ENCODING = "ISO-8859-1"

#SOURCE = "pvcp.csv"
#ENCODING = "UTF-8"

def retrieve_data(source_name=SOURCE):
    import pandas as pd
    import numpy as np
    import json
    frac = 0.9

    infile_name = 'Base_tweets_finale.json'
    all_tweets = []
    all_notation = []

    with open(infile_name, 'r') as infile:
        '''contents = urllib.request.urlopen("https://mds-dev.sinay.fr/api/tweet").read()
        contents = contents.decode('utf-8')
        json_load = json.loads(contents)
        '''
        raw_text = infile.read()
        json_load = json.loads(raw_text, 'utf-8')

        for i in range(len(json_load)):
            if json_load[i]['interessant'] != None:
                if json_load[i]['nom_nettoye'] != None:
                    all_tweets.append(json_load[i]['nom_nettoye'])
                    all_notation.append(json_load[i]['interessant'])

        df = pd.DataFrame({'tweet': all_tweets, 'interessant': all_notation})
        df['split'] = np.random.randn(df.shape[0], 1)
        msk = np.random.rand(len(df)) <= frac
        train = df[msk]
        print(train)

        test = df[~msk]

    return train['tweet'], train['interessant'], test['tweet'], test['interessant']



def train_sgd(Xtrain, Ytrain):
    from sklearn.linear_model import SGDClassifier
    classifier = SGDClassifier(loss="hinge", penalty="elasticnet", n_iter=20) # 'hinge' loss = linear Support Vector Machine (SVM)
    print ("SGD Fitting")
    classifier.fit(Xtrain, Ytrain)
    return classifier


def accuracy(Ytrain, Ytest):
    assert (len(Ytrain) == len(Ytest))
    num = sum([1 for i, word in enumerate(Ytrain) if Ytest[i] == word])
    n = len(Ytrain)
    return (num * 100) / n


def write_txt(data, name):
    data = ''.join(str(word) for word in data)
    file = open(name, 'w')
    file.write(data)
    file.close()
    pass

def train_and_test(vectorizer, training_function):
    print ("-----------------------TRAINING THE MODEL---------------------------")
    # avec TF-IDF
    '''Xtrain_uni = vectorizer.transform(Xtrain_text)
    uni_tfidf_transformer = tfidf_process(Xtrain_uni)
    Xtrain_tf_uni = uni_tfidf_transformer.transform(Xtrain_uni)
    classifier = training_function(Xtrain_tf_uni, Ytrain)
    Ytrain_uni = classifier.predict(Xtrain_tf_uni)'''

    # sans TF-IDF
    Xtrain_uni = vectorizer.transform(Xtrain_text)
    classifier = training_function(Xtrain_uni, Ytrain)
    Ytrain_uni = classifier.predict(Xtrain_uni)


    print ("Train accuracy: ", accuracy(Ytrain, Ytrain_uni))
    print ("\n")

    print ("-----------------------TESTING THE MODEL -----------------------")
    Xtest_uni = vectorizer.transform(Xtest_text)
    Ytest_uni = classifier.predict(Xtest_uni)

    from sklearn.metrics import precision_recall_fscore_support
    print("-----------------precision, recall, f1_score pour les 5 catégories----------------------")
    print(precision_recall_fscore_support(Ytest, Ytest_uni))
    print ("Test accuracy: ", accuracy(Ytest, Ytest_uni))
    print ("\n")
    return Ytest_uni, classifier



if __name__ == "__main__":
    import time
    from sklearn.metrics import confusion_matrix
    import argparse
    from sklearn.externals import joblib

    MODEL_PATH = 'model.pkl'

    parser = argparse.ArgumentParser(description='Train and test a semantic classifier.')
    parser.add_argument('action', metavar='action', type=str, nargs='+',
                        help='train | infer')

    args = parser.parse_args()

    action = args.action[0]


    if action == 'train':
        Xtrain_text, Ytrain, Xtest_text, Ytest = retrieve_data()
        print("========================BIGRAM + SGD================================")
        start = time.time()
        vectorizer = bigram_process(Xtrain_text) # on choisi bigrame ou unigram ici
        y_true, classifier=train_and_test(vectorizer, train_sgd)
        #y_true_bigram=train_and_test(bigram_process(Xtrain_text), train_sgd)
        print("total de tweets testés:", len(y_true))
        print ("Time taken: ", time.time() - start, " seconds")
        Matrice_confusion=confusion_matrix(Ytest,y_true)
        print("matrice_confusion: \n ",Matrice_confusion)
        #Matrice_confusion_bigram=confusion_matrix(Ytest,y_true_bigram)
        #print("matrice_confusion_bigram",Matrice_confusion_bigram)

        print ("-----------------------SAVING THE MODEL-----------------------------")
        joblib.dump(classifier, MODEL_PATH)
        joblib.dump(vectorizer, 'vectorizer.pkl')
        print("Model saved.")
    else:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load('vectorizer.pkl')
        test_text = "RT @DukeU: A strategy for making 'no-mining zones' in the deep sea. https://t.co/EQpWNMsS62 https://t.co/vaRRZMx7MJ"
        test_vector = vectorizer.transform([test_text])
        prediction = model.predict(test_vector)
        print("prediction", prediction)