import collections
import pandas as pd

danmu_lists = open('./message/ailurus_danmu.txt', 'r', encoding='utf-8').read().split('\n')
danmu_lists = collections.Counter(danmu_lists)
df = pd.DataFrame(danmu_lists.items(), columns=['key', 'cnt'])
df = df.sort_values(by=['cnt'], ascending=False)
# print(df)
df.to_csv('ailurus_danmuount.csv')