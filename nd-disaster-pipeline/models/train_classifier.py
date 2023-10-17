import sys
import pandas as pd
from sqlalchemy import create_engine
import pickle



import nltk
nltk.download(['punkt', 'wordnet'])
import re
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin


def load_data(database_filepath):
    """
    fetch data loaded in sqlite DB
    param: db filepath
    return: Features variable (X)
    return: Target variables (Y)
    """

    # load data from database
    engine = create_engine(f'sqlite:///{database_filepath}')

    df = pd.read_sql_table(database_filepath, engine)

    # remove empty row values in dataset
    df = df.dropna()

    X = df.message.values
    Y = df.drop(['id', 'message', 'original', 'genre'], axis=1).values.astype('int')
    labels = df.drop(['id', 'message', 'original', 'genre'], axis=1).columns.tolist()

    return X, Y, labels


def tokenize(text):
    """
    tokenize and lemmanize text input.
    param: text messages
    return: list of tokens
    """

    clean_tokens = []

    # remove non-text characters
    text_clean = re.sub(r'[^a-zA-Z]', " ", text)

    tokens = word_tokenize(text_clean)
    lemmatizer = WordNetLemmatizer()

    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    """
    Train model using hyper param tuning (gridsearch)
    return: tuned model (classifier)
     """

    # initiate pipeline
    rfc = RandomForestClassifier()

    pipeline = Pipeline([

        ('vec', CountVectorizer(tokenizer=tokenize)),

        ('tfidf', TfidfTransformer()),

        ('rfc', MultiOutputClassifier(rfc, n_jobs=-1))

    ])

    # hyper params used for tuning
    parameters = {
        'rfc__estimator__n_estimators': [100, 200]
    }

    # tuned model using gridsearch
    model = GridSearchCV(pipeline, param_grid=parameters)

    return model


def evaluate_model(model, X_test, Y_test, labels):
    """"
    evaluate model performance in terms of precision,recall and f1 for each label
    param: tuned model
    param: X variables from test dataset
    param: Y variables from test dataset
    return: classification report
    """

    y_pred = model.predict(X_test)

    for i, category in enumerate(labels):
        print(f"evaluation report for: {category}")
        evaluation_report = classification_report(Y_test[:, i], y_pred[:, i])
        accuracy = (y_pred[:, i] == Y_test[:, i]).mean()

        print(evaluation_report)
        print("accuracy_score:{}".format(accuracy))


def save_model(model, model_filepath):
    """
    save tuned model in a pickle file
    param: tuned model instance
    param: pickle filepath
    """

    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()