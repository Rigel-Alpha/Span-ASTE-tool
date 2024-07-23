# @title Data Exploration

import sys
import torch
import json
from pathlib import Path
from aste.data_utils import Data, Sentence, SplitEnum
from aste.wrapper import SpanModel
import argparse

# 解析参数
parser = argparse.ArgumentParser(description="Train the model.")
parser.add_argument('--random_seed', type=int, required=True, help='Random seed')
parser.add_argument('--model_name', type=str, required=True, help='Model name')
args = parser.parse_args()

random_seed = args.random_seed
data_name = args.model_name  # 所用的数据集名称，也是outputs目录中保存的模型文件夹名称

assert torch.cuda.is_available()

sys.path.append("")
path = f"aste/data/triplet_data/{data_name}/train.txt"
data = Data.load_from_full_path(path)

template = "https://github.com/chiayewken/Span-ASTE/releases/download/v1.0.0/{}.tar"
url = template.format(data_name)
model_tar = Path(url).name
model_dir = Path(url).stem


path_train = f"aste/data/triplet_data/{data_name}/train.txt"
path_dev = f"aste/data/triplet_data/{data_name}/dev.txt"
save_dir = f"outputs/{data_name}/seed_{random_seed}"

model = SpanModel(save_dir=save_dir, random_seed=random_seed)
model.fit(path_train, path_dev)

print("####################################")