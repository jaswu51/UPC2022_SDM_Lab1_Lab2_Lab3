import os

import pandas as pd


def load_csv_to_data_frame(filename, header_filename=None, NUM_ROWS=10000):
    assert isinstance(filename, str)
    assert '.csv' in filename
    print(filename)
    assert os.path.exists(filename)
    assert header_filename is None or '.csv' in header_filename

    header = None
    if header_filename is not None:
        header = pd.read_csv(header_filename, sep=';').columns.values

    # Read the csv file into the pandas dataframe
    if header is not None:
        header = [x.split(":")[0] for x in header]
        df = pd.read_csv(filename, sep=';', names=header, on_bad_lines='skip', nrows=NUM_ROWS)
    else:
        df = pd.read_csv(filename, sep=';', on_bad_lines='skip', nrows=NUM_ROWS, low_memory= False)

    # df = df.loc[:, df.isnull().mean() < NULL_RATIO]
    df.dropna(axis=0, how='all', inplace=True)
    return df


def filter_columns(df, column_names):
    assert isinstance(df, pd.core.frame.DataFrame)
    assert isinstance(column_names, list)

    df = df[column_names]
    df = df.drop_duplicates().dropna()
    return df


def df_to_csv(df, save_path):
    assert isinstance(df, pd.core.frame.DataFrame)
    assert isinstance(save_path, str)
    assert '.csv' in save_path

    df.to_csv(save_path, index=False, sep=';')
