"""
    这是入口脚本。

    数据格式:
        参考dataset中的示例数据集。

    参数说明:
        dataset:放在dataset目录下的待预测的csv文件名称，默认为14lap中划分的测试集。
        using_train: 是否要重新训练数据，还是直接使用pretrain_weight中的权重
        model_name:采用这个数据集进行训练，日志和权重保存在outputs/{model_name}目录中。
        random_seed:采用这个种子进行训练。

    结果保存:
        在pred目录下对应数据集的文件夹中。

"""

import argparse
import subprocess
import os

dataset = "14lap"
using_train = False
model_name = "14lap"  # 可选值有"14lap" "14res" "15res" "16res"
random_seed = 18


def main():
    parser = argparse.ArgumentParser(description="Main script for running the project.")

    parser.add_argument('--dataset', type=str, default=dataset, help='Dataset name')
    parser.add_argument('--model_name', type=str, default=model_name, help='Model name')
    parser.add_argument('--random_seed', type=int, default=random_seed, help='Random seed')
    parser.add_argument('--using_train', type=bool, default=using_train, help='Using train')
    args = parser.parse_args()

    # 训练模型，得到的权重保存在outputs中
    if not os.path.exists(f'outputs/{dataset}/seed{random_seed}') and using_train:
        print("Training...")
        subprocess.run(['python', 'train.py',
                        '--random_seed', str(args.random_seed),
                        '--model_name', args.model_name])

    # 使用outputs中对应种子和名称的模型，执行预测
    print("Predicting...")
    using_train_str = "" if not using_train else "True"
    subprocess.run(['python', 'pred.py',
                    '--dataset', args.dataset,
                    '--model_name', args.model_name,
                    '--random_seed', str(args.random_seed),
                    '--using_train', using_train_str])

    # 处理数据格式，保存到pred文件夹中
    subprocess.run(['python', 'format_output.py',
                    '--dataset', args.dataset,
                    '--random_seed', str(args.random_seed)])


if __name__ == "__main__":
    main()
