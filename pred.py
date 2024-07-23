import argparse
import pandas as pd

# 加载参数
parser = argparse.ArgumentParser(description="Predict using the model.")
parser.add_argument('--dataset', type=str, required=True, help='Dataset name')
parser.add_argument('--model_name', type=str, required=True, help='Model name')
parser.add_argument('--random_seed', type=int, required=True, help='Random seed')
parser.add_argument('--using_train', type=bool, required=True, help='Using train')

args = parser.parse_args()
dataset = args.dataset
model_name = args.model_name
random_seed = args.random_seed
using_train = args.using_train

# 在数据后添加标签使其符合格式要求，并保存到aste/temp_data中
df = pd.read_csv("dataset/"+dataset+".csv", header=None)

selected_sentences = []
selected_sentences = df.iloc[:, 0].tolist()

tag = " .#### #### ####[]\n"
tagged_sentences = [f"{sentence}{tag}" for sentence in selected_sentences]

import re
for line in tagged_sentences:
    # 检查分隔符
    if not re.search(r"#### ####", line):
        print(line)

with open('aste/temp_data/'+dataset+'.csv', 'w', encoding='utf-8') as file:
    file.writelines(tagged_sentences)

###################################################

# 使用训练好的模型进行预测，结果保存到目录pred中
from aste.wrapper import SpanModel

save_dir = "pred"

if using_train:
    model_dir = f"outputs/{model_name}/seed_{random_seed}"
else:
    model_dir = f"pretrained_weight/{model_name}"

model = SpanModel(save_dir=model_dir, random_seed=random_seed)
output_dir = f"{save_dir}/{dataset}/{dataset}_pred_seed{random_seed}.csv"
test_data_path = f"aste/temp_data/{dataset}.csv"

model.predict(path_in=test_data_path, path_out=output_dir)
