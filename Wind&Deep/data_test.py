# -*- encoding: utf-8 -*-
'''
@File    :   data_test.py
@Time    :   2020/09/13 16:34:13
@Author  :   Peng He
@Version :   1.0
@Contact :   penghe6666@gmail.com
@IDE     :   Visual Studio Code
@License :   (C)Copyright 2020, CUG
@Desc    :   None
'''
from utils import create_criteo_dataset
# here put the import lib
if __name__ == "__main__":
    feature_columns, (train_X, train_Y), (
        test_X, test_Y
    ) = create_criteo_dataset(
        'D:/data/Chrome-Download/198459_438654_bundle_archive/train_1m.txt')
    print(feature_columns)
