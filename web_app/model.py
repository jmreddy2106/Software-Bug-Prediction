import pandas as pd
# import numpy as np
from sklearn.model_selection import train_test_split

# packages for plot
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
# import seaborn as sns

# packages for metrics
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

# packages for AdaBoost
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
# from sklearn.preprocessing import LabelEncoder

# Package for Logistic Regression
from sklearn.linear_model import LogisticRegression

# Package for RandomForest
from sklearn.ensemble import RandomForestClassifier

import warnings

warnings.filterwarnings("ignore")


# read the data
# data = pd.read_csv("D:\\project\\FinalFlask\\static\\Final Sets\\ScikitLearnFinalSet12.csv")
# data = pd.read_csv("Example.csv")
# data = pd.read_csv("Final Sets/SparkFinalSet.csv")
# data = pd.read_csv("Final Sets/KafkaFinalSet.csv")
# Renaming unnamed column
# df = data.rename({'Unnamed: 0': 'File'}, axis=1)


# model
# accepts parameters label and classifier int(opt) and img_loc specifies image location
def model(st, opt, img_loc, name):
    data = pd.read_csv("D:\\project\\FinalFlask\\static\\Final Sets\\ScikitLearnFinalSet12.csv")
    df = data.rename({'Unnamed: 0': 'File'}, axis=1)

    res_dict = {}
    fdf = ""
    classifier = ""

    if st == "BugLabelLevel":
        fdf = df.drop(df.columns[[0, 1, 2, 22, 23, 24]], axis=1)
        res_dict['Label Counts'] = {'0': df[st].value_counts()[0], '1': df[st].value_counts()[1],
                                    '2': df[st].value_counts()[2]}
    elif st == "CommitBug":
        fdf = df.drop(df.columns[[0, 1, 2, 21, 23, 24]], axis=1)
        res_dict['Label Counts'] = {'0': df[st].value_counts()[0], '1': df[st].value_counts()[1]}
    elif st == "AddRemoved":
        fdf = df.drop(df.columns[[0, 1, 2, 21, 22, 24]], axis=1)
        res_dict['Label Counts'] = {'0': df[st].value_counts()[0], '1': df[st].value_counts()[1]}
    elif st == "CommitAddRemoved":
        fdf = df.drop(df.columns[[0, 1, 2, 21, 22, 23]], axis=1)
        res_dict['Label Counts'] = {'0': df[st].value_counts()[0], '1': df[st].value_counts()[1]}

    print("Label", st, sep="\n")
    print(st, "Value Counts")
    print(df[st].value_counts())



    x = fdf.loc[:, fdf.columns != st]
    y = fdf.loc[:, fdf.columns == st]

    if opt == 1:
        train_X, test_X, train_y, test_y = train_test_split(x, y, random_state=1)
        classifier = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=200)
    elif opt == 2:
        train_X, test_X, train_y, test_y = train_test_split(x, y, random_state=4)
        classifier = LogisticRegression()
    elif opt == 3:
        train_X, test_X, train_y, test_y = train_test_split(x, y, test_size=0.70)
        classifier = RandomForestClassifier(n_estimators=100)

        # print("Classifier \n",classifier,end="\n\n")
    classifier.fit(train_X, train_y)

    predictions = classifier.predict(test_X)

    print("Confusion matrix")
    con_mat = confusion_matrix(test_y, predictions)
    print(con_mat)

    res_dict['Confusion matrix'] = con_mat

    accuracy = accuracy_score(test_y, predictions)
    accuracy_percentage = 100 * accuracy

    print("Accuracy Percentage:", accuracy_percentage)

    res_dict['Accuracy'] = accuracy_percentage

    print("Classification Report", end="\n\n")
    clf_report = classification_report(test_y, predictions)
    print(clf_report)

    res_dict['Classification_report'] = clf_report.split("\n")

    class_count = len(df[st].value_counts())
    print(class_count)

    if class_count == 2:
        logit_roc_auc = roc_auc_score(test_y, classifier.predict(test_X))
        fpr, tpr, thresholds = roc_curve(test_y, classifier.predict_proba(test_X)[:, 1])
        print("ROC AUC SCORE:", logit_roc_auc)
        res_dict['ROC AUC Score'] = logit_roc_auc
        print()
        plt.figure()
        plt.plot(fpr, tpr, label='Adaboost (area = %0.2f)' % logit_roc_auc)
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.savefig('static/' + img_loc)
        plt.show()
    elif class_count == 3:
        fpr = {}
        tpr = {}
        thresh = {}
        for i in range(3):
            fpr[i], tpr[i], thresh[i] = roc_curve(test_y, classifier.predict_proba(test_X)[:, i], pos_label=i)
            print("Roc auc score for", i, "Vs rest:", auc(fpr[i], tpr[i]))
        logit_roc_auc = roc_auc_score(test_y, classifier.predict_proba(test_X), multi_class='ovr')
        print("Average roc auc score:", logit_roc_auc)
        res_dict['ROC AUC Score'] = logit_roc_auc
        print()
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.plot(fpr[0], tpr[0], label='class 0 vs Rest', color='orange')
        plt.plot(fpr[1], tpr[1], label='class 1 vs Rest', color='green')
        plt.plot(fpr[2], tpr[2], label='class 2 vs Rest', color='blue')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.savefig('static/' + img_loc)
        plt.show()
    else:
        print("Insufficient Data")
    return classifier, res_dict


def predict_user_file(clf, name, st):
    data = pd.read_csv(name+".csv")
    df = data.rename({'Unnamed: 0': 'File'}, axis=1)
    file_names = df.iloc[:, 0]
    fdf = df.drop(df.columns[[0, 1, 2, 22, 23, 24]], axis=1)

    if st == "BugLabelLevel":
        fdf = df.drop(df.columns[[0, 1, 2, 22, 23, 24]], axis=1)
    elif st == "CommitBug":
        fdf = df.drop(df.columns[[0, 1, 2, 21, 23, 24]], axis=1)
    elif st == "AddRemoved":
        fdf = df.drop(df.columns[[0, 1, 2, 21, 22, 24]], axis=1)
    elif st == "CommitAddRemoved":
        fdf = df.drop(df.columns[[0, 1, 2, 21, 22, 23]], axis=1)

    x = fdf.loc[:, fdf.columns != st]
    res = clf.predict(x)
    return file_names, res

# labelDict = {1: "BugLabelLevel", 2: "CommitBug", 3: "AddRemoved", 4: "CommitAddRemoved"}
# print("Labels:", "1.BugLabelLevel(multi labels)", "2.CommitBug", "3.AddRemoved", "4.CommitAddRemoved", sep="\n")
# labelopt = int(input("Choose Label Option "))
# label = labelDict[labelopt]
#
# print("Labels:", "1.Adaboost", "2.Logistic Regression", "3.RandomForestClassifier")
# option = int(input("Choose Classifier Option "))
#
# model(label, option)
