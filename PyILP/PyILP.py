import numpy as np
import shutil
from texttable import Texttable
import time
import os
import random
import janus_swi as janus


def read_example(file_name):
    file_1 = open(file_name, 'r')
    lines = file_1.readlines()
    list_1 = []
    for eachline in lines:
        line_1 = eachline.strip()
        if line_1 and line_1[0] != "%":
            list_1.append(line_1)
    file_1.close()
    return list_1


class Aleph:
    def __init__(self, H_2, acc_test, Test_Precision, Test_Recall, Test_Specificty, Test_F1, aleph_learn_time):
        self.hypothesis = H_2
        self.accuracy = acc_test
        self.precision = Test_Precision
        self.sensitivity = Test_Recall
        self.specificity = Test_Specificty
        self.fscore = Test_F1
        self.time_learn = aleph_learn_time

class MIL:
    def __init__(self, H_2, acc_test,Test_Precision, Test_Recall, Test_Specificty, Test_F1,aleph_learn_time):
        self.hypothesis = H_2
        self.accuracy = acc_test
        self.precision = Test_Precision
        self.sensitivity=Test_Recall
        self.specificity=Test_Specificty
        self.fscore=Test_F1
        self.time_learn=aleph_learn_time


def metrics(TP,TN,FP,FN):
    try:
        accuracy = round((TP+TN)/(TP+TN+FP+FN),3)
    except ZeroDivisionError:
        accuracy=None
    try:
        precision = round(TP/(TP+FP),3)
    except ZeroDivisionError:
        precision=None
    try:
        sensitivity = round(TP / (TP+FN),3)
    except ZeroDivisionError:
        sensitivity=None
    try:
        specificity = round(TN / (TN+FP),3)
    except ZeroDivisionError:
        specificity= None
    try :
        fscore =  round(2*TP / ( (2*TP)+FP+FN ),3)
    except ZeroDivisionError:
        fscore=None
    return accuracy, precision, sensitivity, specificity, fscore


def learn_theory_aleph(file_name):
    #prolog = Prolog()
    program_name = file_name[:-3]
    janus.consult(file_name)
    a = list(janus.query("induce(program_name)"))
    b = list(janus.query("aleph:write_rules('theory.txt',program_name)"))


def generate_theory_metagol(file_name):
    theory = []
    if os.path.isfile("theory.txt"):
        # print("hai")
        f = open("theory.txt")

        for line in f.read().splitlines():
            theory.append(line)

    return theory

def generate_theory_aleph(file_name):
    f = open("theory.txt")
    theory = []
    for line in f.read().splitlines():
        theory.append(line)
    flag_1 = "true"
    string = ""
    hypo = []
    for i in theory:
        if flag_1 == "true":
            if i[-1] == ".":
                string = string + i
                hypo.append(string)
                # print(hypo)
                string = ""
            else:
                string = string + i
    return hypo


def evaluate_theory_prolog(theory, file_1, pos, neg):
    file_2 = "copy_bk.pl"
    shutil.copyfile(file_1, file_2)
    file_object = open(file_2, 'a')

    for j in theory:
        j = j.replace("&", ",")
        if j[-1] != ".":
            file_object.write(j + ".")
            file_object.write("\n")
    file_object.close()
    
    janus.consult(file_2)
    pos_ex = pos  # file_3.read().splitlines()

    neg_ex = neg  # file_4.read().splitlines()

    pos_count = 0
    neg_count = 0
    for k in pos_ex:
        if janus.query_once(k)['truth']:
            pos_count = pos_count + 1
    for l in neg_ex:
        if not janus.query_once(l)['truth']:
            neg_count = neg_count + 1
    # print(pos_count, neg_count)
    acc = (pos_count + neg_count) / (len(pos_ex) + len(neg_ex))
    # print("accuracy :-",round(acc*100,2))

    rec = [['n = ' + str(len(pos_ex) + (len(neg_ex))), 'Positive(Actual)', 'Negative(Actual)'],
           ["Positive(Predicted)", pos_count, len(neg_ex) - neg_count],
           ["Negative(Predicted)", len(pos_ex) - pos_count, neg_count]]

    table = Texttable()
    table.add_rows(rec)
    print(table.draw())
    # close(
    os.remove(file_2)

    accuracy, precision, sensitivity, specificity, fscore = metrics(pos_count, neg_count, len(neg_ex) - neg_count,
                                                                    len(pos_ex) - pos_count)
    rec = [["Metric", "#"], ["Accuracy", accuracy], ["Precision", precision], ["Sensitivity", sensitivity],
           ["Specificity", specificity], ["F1 Score", fscore]]
    table = Texttable()
    table.add_rows(rec)
    print(table.draw())
    return Aleph([], accuracy, precision, sensitivity, specificity, fscore, [])



def prepare_bk(bkk_file, settings, file_name="BKK_Temp.pl"):
    file_1=open(file_name,"w")
    file_1.close()
    file_1=open(file_name,"a")
    file_2=open(settings,"r")
    file_1.write(":- use_module('metagol').\n")
    file_1.write(":- multifile body_pred/1.\n")
    file_1.write(":- multifile head_pred/1.\n")
    for line in file_2.readlines():
        file_1.write(line)
    file_2.close()
    file_3=open(bkk_file,"r")
    for line in file_3.readlines():
        file_1.write(line)
    file_3.close()
    file_1.close()
    return file_name

def aleph(aleph_bk, pos_fold_ex, neg_fold_ex, settings):
    aleph_swipl = [":- use_module(aleph).", ":- if(current_predicate(use_rendering/1)).",
                   ":- use_rendering(prolog).", ":- endif.", ":- aleph.",
                   ":-style_check(-discontiguous)."]

    temp_file = "aleph_bk_1.pl"
    if type(settings) == list:
        file_1 = open(temp_file, 'w')
        file_2 = open(aleph_bk, 'r')
        for line in file_2.readlines():
            file_1.write(line)
            # file_1.write("\n")
        file_1.write("\n:-begin_in_pos.\n")
        for i in pos_fold_ex:
            file_1.write("\n" + str(i))
        file_1.write("\n:-end_in_pos.\n")
        file_1.write("\n:-begin_in_neg.\n")
        for i in neg_fold_ex:
            file_1.write("\n" + str(i))
        file_1.write("\n:-end_in_neg.")
        file_1.close()
        file_2.close()
    else:
        file_1 = open(temp_file, 'w')
        for i in aleph_swipl:
            file_1.write(i + "\n")

        file_2 = open(settings, 'r')
        for line in file_2.readlines():
            file_1.write(line)
            # file_1.write("\n")
        file_2.close()

        file_1.write("\n:-begin_bg.\n")
        file_3 = open(aleph_bk, 'r')
        for line in file_3.readlines():
            file_1.write(line)
            # file_1.write("\n")
        file_1.write("\n:-end_bg.\n")
        file_3.close()
        file_1.write("\n:-begin_in_pos.\n")
        for i in pos_fold_ex:
            file_1.write("\n" + str(i))
        file_1.write("\n:-end_in_pos.\n")
        file_1.write("\n:-begin_in_neg.\n")
        for i in neg_fold_ex:
            file_1.write("\n" + str(i))
        file_1.write("\n:-end_in_neg.\n")
        file_1.close()

    learn_theory_aleph(temp_file)
    theory = generate_theory_aleph(temp_file)
    os.remove(temp_file)
    return theory


def aleph_cross_validation(file="BK.pl", CV=2, positive_example="pos_example.f",
                           negative_example="neg_example.n", shuffle=False, settings=[]):
    aleph_cv_accuracy, aleph_cv_precision, aleph_cv_sensitivity, aleph_cv_specificity, aleph_cv_fscore = [], [], [], [], []

    if type(positive_example) == list:
        positive_example_ids = positive_example
    else:
        positive_example_ids = read_example(positive_example)
    if type(negative_example) == list:
        negative_example_ids = negative_example
    else:
        negative_example_ids = read_example(negative_example)
    if shuffle == True:
        random.shuffle(positive_example_ids)
        random.shuffle(negative_example_ids)
    # pos=read_example("pos_example.f")
    # neg=read_example("neg_example.n")
    folds_pos = list(np.array_split(positive_example_ids, CV))
    folds_neg = list(np.array_split(negative_example_ids, CV))
    # random.shuffle(folds_pos)
    # random.shuffle(folds_neg)
    start_time = time.time()
    for i in range(CV):
        pos_train_fold = []
        pos_test_fold = []
        neg_train_fold = []
        neg_test_fold = []
        for j in range(CV):
            if j != i:
                fold = j % CV
                pos_train_fold = pos_train_fold + list(folds_pos[fold])
                neg_train_fold = neg_train_fold + list(folds_neg[fold])
            else:
                fold = j % CV
                pos_test_fold = pos_test_fold + list(folds_pos[fold])
                neg_test_fold = neg_test_fold + list(folds_neg[fold])
        H_2 = aleph(file, pos_train_fold, neg_train_fold, settings)
        print(H_2)
        if H_2:
            print("+----------+ Testing +----------+")
            test = evaluate_theory_prolog(H_2, file, pos_test_fold, neg_test_fold)
            os.remove("theory.txt")
            aleph_cv_accuracy.append(test.accuracy)
            aleph_cv_precision.append(test.precision)
            aleph_cv_sensitivity.append(test.sensitivity)
            aleph_cv_specificity.append(test.specificity)
            aleph_cv_fscore.append(test.fscore)
        else:
            print("Couldnt Learn Hypothesis")
            aleph_cv_accuracy.append(0)
            aleph_cv_precision.append(0)
            aleph_cv_sensitivity.append(0)
            aleph_cv_specificity.append(0)
            aleph_cv_fscore.append(0)

    end_time = time.time() - start_time
    # time_list_aleph.append(end_time)
    return Aleph([], aleph_cv_accuracy, aleph_cv_precision, aleph_cv_sensitivity, aleph_cv_specificity, aleph_cv_fscore,
                 end_time)


def aleph_learn(file="BK.pl", test_size=0.33, positive_example="pos_example.f",
                negative_example="neg_example.n", shuffle=False, settings=[]):
    start_time = time.time()
    accuracy_list_aleph = []
    time_list_aleph = []
    if type(positive_example) == list:
        positive_example_ids = positive_example
    else:
        positive_example_ids = read_example(positive_example)
    if type(negative_example) == list:
        negative_example_ids = negative_example
    else:
        negative_example_ids = read_example(negative_example)
    if shuffle == True:
        random.shuffle(positive_example_ids)
        random.shuffle(negative_example_ids)
    length_positive_examples = len(positive_example_ids)
    length_negative_examples = len(negative_example_ids)

    positive_example_training_size = int(((1 - test_size) * length_positive_examples))
    negative_example_training_size = int(((1 - test_size) * length_negative_examples))

    positive_example_ids_training = positive_example_ids[0:positive_example_training_size]
    negative_example_ids_training = negative_example_ids[0:negative_example_training_size]

    positive_example_ids_test = positive_example_ids[positive_example_training_size:]
    negative_example_ids_test = negative_example_ids[negative_example_training_size:]
    H_2 = aleph(file, positive_example_ids_training, negative_example_ids_training, settings)
    aleph_learn_time = time.time() - start_time
    if test_size != 0:
        if H_2:
            print(H_2)
            print("+----------+ Testing +----------+")
            test = evaluate_theory_prolog(H_2, file, positive_example_ids_test, negative_example_ids_test)
            os.remove("theory.txt")
            # rint(test)
            return Aleph(H_2, test.accuracy, test.precision, test.sensitivity, test.specificity, test.fscore,
                         aleph_learn_time)
    else:
        print(H_2)
        print("+----------+ Learning +----------+")
        test = evaluate_theory_prolog(H_2, file, positive_example_ids_training, negative_example_ids_training)
        os.remove("theory.txt")
        return Aleph(H_2, test.accuracy, test.precision, test.sensitivity, test.specificity, test.fscore,
                     aleph_learn_time)


def metagol(file_name, pos, neg):
    if pos and neg:
        pos_ex_list = [i[0:-1] for i in pos]
        neg_ex_list = [i[0:-1] for i in neg]

        string_1 = ":- Pos=[" + ",".join(pos_ex_list) + "],Neg =[" + ",".join(neg_ex_list) + "], learn(Pos,Neg)."
        file_1 = "processed_bk.pl"
        shutil.copyfile(file_name, file_1)
        file_object = open(file_1, 'a')
        file_object.write(string_1)
        file_object.close()
        #prolog = Prolog()
        janus.consult(file_1)
        theory = generate_theory_metagol(file_1)

        os.remove(file_1)

        return theory
    else:
        #prolog = Prolog()
        janus.consult(file_name)
        theory = generate_theory_metagol(file_name)
        return theory


def metagol_learn(file="BK.pl", test_size=0.33, positive_example="pos_example.f",
                  negative_example="neg_example.n", shuffle=False, settings=[]):
    start_time = time.time()

    if not positive_example and not negative_example:
        H_2 = metagol(file, [], [])
    else:
        if type(settings)!=list:
            final_bk_file = prepare_bk(file, settings)
        else:
            final_bk_file=file
        accuracy_list_aleph = []
        time_list_aleph = []
        if type(positive_example) == list:
            positive_example_ids = positive_example
        else:
            positive_example_ids = read_example(positive_example)
        if type(negative_example) == list:
            negative_example_ids = negative_example
        else:
            negative_example_ids = read_example(negative_example)
        if shuffle == True:
            random.shuffle(positive_example_ids)
            random.shuffle(negative_example_ids)
        length_positive_examples = len(positive_example_ids)
        length_negative_examples = len(negative_example_ids)

        positive_example_training_size = int(((1 - test_size) * length_positive_examples))
        negative_example_training_size = int(((1 - test_size) * length_negative_examples))

        positive_example_ids_training = positive_example_ids[0:positive_example_training_size]
        negative_example_ids_training = negative_example_ids[0:negative_example_training_size]

        positive_example_ids_test = positive_example_ids[positive_example_training_size:]
        negative_example_ids_test = negative_example_ids[negative_example_training_size:]
        H_2 = metagol(final_bk_file, positive_example_ids_training, negative_example_ids_training)
    end_time = time.time() - start_time
    if test_size != 0:
        if H_2:
            print(H_2)
            print("+----------+ Testing +----------+")
            test = evaluate_theory_prolog(H_2, file, positive_example_ids_test, negative_example_ids_test)
            os.remove("theory.txt")
            # rint(test)
            return MIL(H_2, test.accuracy, test.precision, test.sensitivity, test.specificity, test.fscore, end_time)
    else:
        print(H_2)
        if positive_example and negative_example:
            print("+----------+ Learning +----------+")
            test = evaluate_theory_prolog(H_2, file, positive_example_ids_training, negative_example_ids_training)
            os.remove("theory.txt")
            return MIL(H_2, test.accuracy, test.precision, test.sensitivity, test.specificity, test.fscore, end_time)
        else:
            os.remove("theory.txt")
            return MIL(H_2, 0, 0, 0, 0, 0, end_time)


def metagol_cross_validation(file="BK.pl", CV=2, positive_example="pos_example.f",
                             negative_example="neg_example.n", shuffle=False, settings=[]):
    mil_cv_accuracy, mil_cv_precision, mil_cv_sensitivity, mil_cv_specificity, mil_cv_fscore = [], [], [], [], []

    if settings:
        final_bk_file = prepare_bk(file, settings)

    if type(positive_example) == list:
        positive_example_ids = positive_example
    else:
        positive_example_ids = read_example(positive_example)
    if type(negative_example) == list:
        negative_example_ids = negative_example
    else:
        negative_example_ids = read_example(negative_example)
    if shuffle == True:
        random.shuffle(positive_example_ids)
        random.shuffle(negative_example_ids)
    # pos=read_example("pos_example.f")
    # neg=read_example("neg_example.n")
    folds_pos = list(np.array_split(positive_example_ids, CV))
    folds_neg = list(np.array_split(negative_example_ids, CV))
    # random.shuffle(folds_pos)
    # random.shuffle(folds_neg)
    start_time = time.time()
    for i in range(CV):
        pos_train_fold = []
        pos_test_fold = []
        neg_train_fold = []
        neg_test_fold = []
        for j in range(CV):
            if j != i:
                fold = j % CV
                pos_train_fold = pos_train_fold + list(folds_pos[fold])
                neg_train_fold = neg_train_fold + list(folds_neg[fold])
            else:
                fold = j % CV
                pos_test_fold = pos_test_fold + list(folds_pos[fold])
                neg_test_fold = neg_test_fold + list(folds_neg[fold])
        H_2 = metagol(final_bk_file, pos_train_fold, neg_train_fold)
        # H_2=H[0]
        print(H_2)
        if H_2:
            print("+----------+ Testing +----------+")
            test = evaluate_theory_prolog(H_2, file, pos_test_fold, neg_test_fold)
            os.remove("theory.txt")
            mil_cv_accuracy.append(test.accuracy)
            mil_cv_precision.append(test.precision)
            mil_cv_sensitivity.append(test.sensitivity)
            mil_cv_specificity.append(test.specificity)
            mil_cv_fscore.append(test.fscore)
        else:
            print("Couldnt Learn Hypothesis")
            mil_cv_accuracy.append(0)
            mil_cv_precision.append(0)
            mil_cv_sensitivity.append(0)
            mil_cv_specificity.append(0)
            aleph_cv_fscore.append(0)

    os.remove("BKK_Temp.pl")
    end_time = time.time() - start_time
    return MIL([], mil_cv_accuracy, mil_cv_precision, mil_cv_sensitivity, mil_cv_specificity, mil_cv_fscore, end_time)
