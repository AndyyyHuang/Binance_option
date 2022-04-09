import pandas as pd
import numpy as np

def drop_outliers(data):
    """
    12小时的价格数据理论应该是连续的，且1小时内应该会有足够多的价格数据来判断异常值
    :param data:
    :return:
    """
    median = data['price'].quantile(0.5)
    return data.loc[[abs(x - median)/min(x, median) < 0.5 for x in data['price']]]


def process_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values('timestamp', inplace=True)
    df = df.set_index('timestamp')
    df_ = df.copy()
    df_ = df_.drop_duplicates(subset='transaction_id', keep='last')
    # 去除离群点
    df_ = df_.resample('6h').apply(drop_outliers)
    df_.index = [x[1] for x in df_.index]

    df_ = df_.dropna()
    position_lis = [1 if x == 'buy' else -1 for x in df_.side]
    df_['position'] = position_lis * df_.amount
    return df_


def deal_with_arbitrage_bot(df_, threshold=500):
    transaction_amount = df_.groupby('address').transaction_id.count().sort_values(ascending=False)
    del_lis = transaction_amount[transaction_amount >= threshold].index
    df_ = df_.loc[~df_['address'].isin(del_lis)]
    return df_


def MaxDrawdown(equity):
    '''最大回撤率'''
    i = np.argmax((np.maximum.accumulate(equity) - equity) / np.maximum.accumulate(equity))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(equity[:i])  # 开始位置
    return (equity[j] - equity[i]) / (equity[j])