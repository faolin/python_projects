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
    frac = 0.9

    df = pd.read_csv(source_name, header=0, encoding=ENCODING)
    df = df[df.text.notnull()]
    print(df.text == '')

    df['split'] = np.random.randn(df.shape[0], 1)

    msk = np.random.rand(len(df)) <= frac

    train = df[msk]
    test = df[~msk]

    return train['text'], train['polarity'], test['text'], test['polarity']



def train_sgd(Xtrain, Ytrain):
    from sklearn.linear_model import SGDClassifier
    classifier = SGDClassifier(loss="hinge", penalty="l1", n_iter=20) # 'hinge' loss = linear Support Vector Machine (SVM)
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
    Xtrain_uni = vectorizer.transform(Xtrain_text)
    classifier = training_function(Xtrain_uni, Ytrain)
    Ytrain_uni = classifier.predict(Xtrain_uni)
    print ("Train accuracy: ", accuracy(Ytrain, Ytrain_uni))
    print ("\n")

    print ("-----------------------TESTING THE MODEL -----------------------")
    Xtest_uni = vectorizer.transform(Xtest_text)
    Ytest_uni = classifier.predict(Xtest_uni)
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
        print("========================UNIGRAM + SGD================================")
        start = time.time()
        vectorizer = bigram_process(Xtrain_text)
        y_true, classifier=train_and_test(vectorizer, train_sgd)
        #y_true_bigram=train_and_test(bigram_process(Xtrain_text), train_sgd)
        print ("Time taken: ", time.time() - start, " seconds")
        print ("test",Ytest)
        Matrice_confusion=confusion_matrix(Ytest,y_true)
        print("matrice_confusion_unigram",Matrice_confusion)
        #Matrice_confusion_bigram=confusion_matrix(Ytest,y_true_bigram)
        #print("matrice_confusion_bigram",Matrice_confusion_bigram)

        print ("-----------------------SAVING THE MODEL-----------------------------")
        joblib.dump(classifier, MODEL_PATH)
        joblib.dump(vectorizer, 'vectorizer.pkl')
        print("Model saved.")
    else:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load('vectorizer.pkl')
        test_text = "this is a terrible movie, i hate it"
        test_vector = vectorizer.transform([test_text])
        prediction = model.predict(test_vector)
        print("prediction", prediction)