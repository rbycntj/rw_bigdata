import pandas as pd
from text2vec import SentenceModel
import numpy as np
import pickle

# 读取csv文件中的数据
file_path = './data/keyword4match.csv'  # 将文件路径替换为你的Excel文件路径
df = pd.read_csv(file_path)

dic_school_1={}
dic_school_2={}
i=0
# 成对遍历school_name和comment
for school, comment in zip(df['school_name'], df['comment']):
    i=i+1
    model = SentenceModel('shibing624/text2vec-base-chinese')
    embeddings = model.encode(comment)   # 将name换为关键词即可
    dic_school_1[school]=embeddings   # 此处不用动

    school_comment=school+": "+comment;
    dic_school_2[school_comment]=embeddings   # 此处不用动


    print(f"{i},学校名称: {school}, 评论: {comment}")


# 将字典存储到文件中
with open('./embedding_result/embedding_all_school.pkl', 'wb') as file:
    pickle.dump(dic_school_1, file)

# 将字典存储到文件中
with open('./embedding_result/embedding_all_school_comment.pkl', 'wb') as file:
    pickle.dump(dic_school_2, file)