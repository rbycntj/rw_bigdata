import pandas as pd
from text2vec import SentenceModel
import numpy as np
import pickle

# 读取Excel文件中的数据
file_path = './data/comment.xlsx'  # 将文件路径替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 初始化一个集合用于存储school_name
school_names = set(df['school_name'])
print(len(school_names))

dic_school={}
i=0
# 遍历集合并输出
for name in school_names:
    # i=i+1
    model = SentenceModel('shibing624/text2vec-base-chinese')
    embeddings = model.encode(name)   # 将name换为关键词即可
    dic_school[name]=embeddings   # 此处不用动
    print(name)
    # if i>100:
    #     break

# 将字典存储到文件中
with open('./embedding_result/embedding_all.pkl', 'wb') as file:
    pickle.dump(dic_school, file)