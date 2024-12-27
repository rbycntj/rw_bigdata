import pickle
import numpy as np
from text2vec import SentenceModel
import json

def cosine_similarity(embedding1, embedding2):
    # 计算余弦相似度
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    cosine_sim = dot_product / (norm1 * norm2)
    return cosine_sim

def find_top5_similar_schools(model_name,embedding_path, input_name):
    """
    找到与输入embedding最相似的5个学校及其匹配分数
    :param input_embedding: 输入的embedding向量
    :param dic_school: 包含学校名称和embedding的字典，格式为 dic_school[school_name] = embedding
    :return: 前5个匹配学校及其匹配分数
    """
    # 从文件中读取字典
    with open(embedding_path, 'rb') as file:
        dic_school = pickle.load(file)

    model = SentenceModel(model_name)
    input_embedding = model.encode(input_name)

    # 计算每个学校与输入embedding的相似度
    similarities = {}
    for school_name, embedding in dic_school.items():
        similarity = cosine_similarity(input_embedding, embedding)
        similarities[school_name] = similarity

    # 按相似度排序，并取前5个
    top5_schools = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:5]

    i=0
    result_json={}
    for school, score in top5_schools:
        i=i+1
        print(f"School: {school}, Similarity Score: {score:.4f}")
        result_json[i]={"school":school,"score":float(score)}

    # 使用json.dumps并设置ensure_ascii为False
    response_json = json.dumps(result_json, ensure_ascii=False)

    return response_json

    print(result_json)
    return result_json


