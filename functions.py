import numpy as np
import pandas as pd


def accuracy(df):
    return df[df.predicted_tag_1 == df.correct_tag_1].shape[0]/df.shape[0]


def accuracy_sent(df, tag):
    n_sent = len(np.unique(df.sent_id))

    if tag is not None:
        df = df[(df.predicted_tag_1 == tag) & (df.correct_tag_1 != tag)]
    else:
        df = df[df.predicted_tag_1 != df.correct_tag_1]
    return 1-len(np.unique(df.sent_id))/n_sent


def average_accuracy(df):
    sent_ids = np.unique(df.sent_id)
    accuracy_list = []
    for sent_id in sent_ids:
        accuracy_list.append(accuracy(df[df.sent_id == sent_id]))
    return np.mean(accuracy_list)


def precision(df, tag):
    df = df[df.predicted_tag_1 == tag]
    return df[df.correct_tag_1 == tag].shape[0]/df.shape[0]


def recall(df, tag):
    df = df[df.correct_tag_1 == tag]
    return df[df.predicted_tag_1 == tag].shape[0]/df.shape[0]


def split_tags(df, column_name):
    l = max([len(x.split('|')) for x in df[column_name]])
    colnames = [column_name+'_'+str(i+1) for i in range(l)]
    df_split = df.drop(column_name, axis=1)
    df_split[colnames] = df[column_name].str.split('|', expand=True)
    for col in colnames:
        df_split[col] = [x.split(')')[0][1:] if x is not None else x for x in df_split[col]]
    return df_split


def read_prediction(prediction_path):
    with open(prediction_path) as f:
        results = f.read()
    lines = results.split('\n')
    annotation_lines = [l for l in lines if not l.startswith('#') and l != '']
    anno_df = pd.DataFrame(columns=['sent_id', 'word_id', 'word', 'predicted_tag'])
    for line in annotation_lines:
        x = line.split('\t')
        anno_df = anno_df.append({'sent_id': int(x[0].split('-')[0]), 'word_id': int(x[0].split('-')[1]), 'word': x[2], 'predicted_tag': x[3]}, ignore_index=True)
    anno_df = split_tags(anno_df, 'predicted_tag')
    return anno_df


def read_goldstandard(goldstandard_path, additional=0):
    with open(goldstandard_path) as f:
        correct = f.read()
    lines_correct = correct.split('\n')
    annotation_lines = [l for l in lines_correct if not l.startswith('#') and l != '']
    goldstandard_df = pd.DataFrame(columns=['word2', 'correct_tag'])
    for line in annotation_lines:
        x = line.split('\t')
        goldstandard_df = goldstandard_df.append({'word2': x[additional], 'correct_tag': x[additional+1]}, ignore_index=True)
    goldstandard_df = split_tags(goldstandard_df, 'correct_tag')
    return goldstandard_df


def map_tags(df, mapping, column):
    df[column] = [mapping[x]if x in mapping.keys() else x for x in df[column]]
    return df
