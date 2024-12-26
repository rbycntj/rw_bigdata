from text2vec import SentenceModel
import numpy as np
import time

def cosine_similarity(embedding1, embedding2):
    # 开始计时
    start_time = time.time()
    
    # 计算余弦相似度
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    cosine_sim = dot_product / (norm1 * norm2)
    
    # 结束计时并计算持续时间
    end_time = time.time()
    duration = end_time - start_time
    
    return cosine_sim, duration

sentences = ['如何更换花呗绑定银行卡', '花呗更改绑定银行卡']

model = SentenceModel('shibing624/text2vec-base-chinese')
embeddings = model.encode(sentences)
print(embeddings)


cos_sim, duration = cosine_similarity(embeddings[0], embeddings[1])
print(f"Cosine Similarity: {cos_sim}")


# # 示例
# embedding1 = np.random.rand(300)
# embedding2 = np.random.rand(300)


# print(f"Computation Time: {duration} seconds")
