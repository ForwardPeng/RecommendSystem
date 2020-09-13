# -*- encoding: utf-8 -*-
'''
@File    :   utilS.PY
@Time    :   2020/09/13 11:50:49
@Author  :   Peng He
@Version :   1.0
@Contact :   penghe6666@gmail.com
@IDE     :   Visual Studio Code
@License :   (C)Copyright 2020, CUG
@Desc    :   None
'''

# here put the import lib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split


def sparseFeature(feat, feat_num, embed_dim=4):
    """
    :param feat: feature name
    :param feat_num:the total number of sparse features that do not repeat
    :param embed_dim:embedding dimension
    """
    return {'feat': feat, 'feat_num': feat_num, 'embed_dim': embed_dim}


def denseFeature(feat):
    """
    :param feat: dense feature name
    """
    return {'feat': feat}


def create_criteo_dataset(file,
                          embed_dim=8,
                          read_part=True,
                          sample_num=100000,
                          test_size=0.2):
    """
    :param file: dataset path
    :param embed_dim: the embedding dimension of sparse featuers
    :param read_part: whether to read part of it
    """
    names = [
        'label', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10',
        'I11', 'I12', 'I13', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
        'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18',
        'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26'
    ]
    if read_part:
        data_df = pd.read_csv(file,
                              sep='\t',
                              iterator=True,
                              header=None,
                              names=names)
        data_df = data_df.get_chunk(sample_num)
    else:
        data_df = pd.read_csv(file, sep='\t', header=None, names=names)

    sparse_features = ['C' + str(i) for i in range(1, 27)]
    dense_features = ['I' + str(i) for i in range(1, 14)]

    data_df[sparse_features] = data_df[sparse_features].fillna('-1')
    data_df[dense_features] = data_df[dense_features].fillna(0)

    for feat in sparse_features:
        le = LabelEncoder()
        data_df[feat] = le.fit_transform(data_df[feat])

    # ----------------------Feature Engineering-------------------------
    dense_features = [
        feat for feat in data_df.columns
        if feat not in sparse_features + ['label']
    ]
    mms = MinMaxScaler(feature_range=(0, 1))
    data_df[dense_features] = mms.fit_transform(data_df[dense_features])

    feature_columns = [[denseFeature(feat) for feat in dense_features]] + [[
        sparseFeature(feat, len(data_df[feat].unique()), embed_dim=embed_dim)
        for feat in sparse_features
    ]]
    train, test = train_test_split(data_df, test_size=test_size)
    train_X = [
        train[dense_features].values,
        train[sparse_features].values.astype('int32')
    ]
    train_Y = train['label'].values.astype('int32')
    test_X = [
        test[dense_features].values,
        test[sparse_features].values.astype('int32')
    ]
    test_Y = test['label'].values.astype('int32')

    return feature_columns, (train_X, train_Y), (test_X, test_Y)
