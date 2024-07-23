import argparse

parser = argparse.ArgumentParser(description="Predict using the model.")
parser.add_argument('--dataset', type=str, required=True, help='Dataset name')
parser.add_argument('--random_seed', type=int, required=True, help='Random seed')
args = parser.parse_args()
dataset = args.dataset
seed = args.random_seed

with open(f'pred/{dataset}/{dataset}_pred_seed{seed}.csv', 'r', encoding='utf-8') as file:
    # 所有语句的内容
    newlines = []
    # 所有标签的内容
    all_tags = []
    for line in file:
        # 找到分析结果开始的位置
        start_index = line.find('#### #### ####')
        if start_index != -1:
            analysis_result = line[start_index + len('#### #### ####'):].strip()
            parsed_result = eval(analysis_result)
            assert isinstance(parsed_result, list)
            # 每一行的标签
            pairs = []
            if not parsed_result:
                pairs.append([])
            for aos in parsed_result:
                a = aos[0]
                o = aos[1]
                s = aos[2]
                words = line.split()
                aspect = []
                opinion = []
                if len(a) == 2:
                    aspect = words[a[0]: a[1]+1]
                else:
                    aspect = words[a[0]]
                if len(o) == 2:
                    opinion = words[o[0]: o[1]+1]
                else:
                    opinion = words[o[0]]
                pair = [aspect, opinion, s]
                pairs.append(pair)

            newline = line.split(' .#### #### ####')[0].strip()
            for pair in pairs:
                for i, item in enumerate(pair):
                    if isinstance(item, list):
                        pair[i] = ' '.join(item)
            all_tags.append(pairs)
            newlines.append(newline)

import csv

save_path = f'pred/{dataset}/{dataset}_pred_seed{seed}_formatted.csv'

# 将 newlines 和 all_tags 写入到 CSV 文件中
with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    headers = ['Sentences'] + ['[Aspect, Opinion, Sentiment]']
    writer.writerow(headers)

    for i in range(max(len(newlines), len(all_tags))):
        row = []
        if i < len(newlines):
            row.append(newlines[i])
        else:
            row.append('')

        if i < len(all_tags):
            row.extend(all_tags[i])
        else:
            row.extend([''] * len(all_tags))

        writer.writerow(row)

print(f'结果保存成功。')
