from flask import Flask, request, jsonify, render_template
from text2vec import SentenceModel
from tools.sim_match import find_top5_similar_schools



app = Flask(__name__)
model = SentenceModel('shibing624/text2vec-base-chinese')
model_name='shibing624/text2vec-base-chinese'
embedding_data = './embedding_result/embedding_all.pkl'
# embedding_data ="/home/xyh/0_name_match/embedding_data/DJ_person_dic_0_10w.jsonl"

# 增加超时时间（以秒为单位）
app.config['SERVER_TIMEOUT'] = 3000  

@app.route('/')
def home():
    return render_template('index.html')  # 渲染 index.html 页面


@app.route('/predict', methods=['POST'])
def predict():
    try:
        real_name_json = request.get_json()
        real_name = real_name_json["name"]
        print('Real name is: {}'.format(real_name))
        candidate_name=find_top5_similar_schools(model_name,embedding_data, real_name)

    except Exception as e:
        print('The error is: ',e)

    return (candidate_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)
    # curl -H "Content-Type: application/json" -X POST -d '{"name": "谢维芬"}' "http://127.0.0.1:82/predict"
    # curl -H "Content-Type: application/json" -X POST -d '{"name": "谢维芬"}' "http://127.0.0.1:8080/predict"
    # curl -H "Content-Type: application/json" -X POST -d '{"name": "谢维芬"}' "http://172.17.0.2:8080/predict"
    # sh run.sh
    # curl -H "Content-Type: application/json" -X POST -d '{"name": "谢维芬"}' "http://172.17.0.2:8080/predict"
     # curl -H "Content-Type: application/json" -X POST -d '{"name": "北京大学"}' "http://172.0.0.1:8081/predict"