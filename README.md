## **工具文档**

### 工具功能：

　　提取句子中的(Aspect, Opinion, Sentiment)三元组。

　　例如：

```
It also has lots of other Korean dishes that are affordable and just as yummy .
```

　　对应的三元组为：

```
[(Korean dishes, affordable, POSITIVE), (Korean dishes, yummy, POSITIVE)]
```

　　

### 环境配置：

　　使用python3.7(推荐使用虚拟环境，如conda)。

　　安装依赖

```
bash setup.sh
```

　　下载[bert-base-uncased模型仓库](https://huggingface.co/google-bert/bert-base-uncased/tree/main)中的**pytorch_model.bin**，放到span_model/models/bert目录下（主要为了防止国内一些网络问题导致连接不上HuggingFace）。

　　

### 数据格式：

#### 　　输入（可参考dataset/14lap.csv）：

　　	输入一个csv文件{data}.csv，每行是一个待测语句，存放在dataset目录下。

#### 　　输出（可参考pred/14lap）：

　　	输出为pred/{data}目录下的csv文件。每一行的格式为：


```
sentence#### #### ####[triplet_0, ..., triplet_n]
```

　　其中每个triplet为(span_a, span_b, label)，每个span是一个单词索引的列表，表示起始和结束处的索引。而label有三个可能值：’POS’, ‘NEU’, ‘NEG’，分别表示Sentiment是’Positive’, ‘Neutral’, ‘Negative’。

​	例如：


```
It is a great size and amazing windows 8 included ! .#### #### ####[([4], [3], 'POS'), ([7, 8], [6], 'POS')]
```

　　这个结果中，对于原句提取出的三元组为(size, great, positive), (windows 8, amazing, positive)。

　　

### 运行：

　　1.（可选）修改training_config/config.json中的训练参数

　　2.指定入口脚本main.py中的参数

　　参数说明：

　　**dataset**: 待预测的csv文件名称。
	**using_train**: 选择重新训练数据(using_train=True)，还是直接使用预训练的权重(using_train=False)。如果直接使用预训练权重，你可以从这里[下载预训练权重](https://github.com/chiayewken/Span-ASTE/releases)(例如14lap.tar)，解压后把它放在pretrained_weight目录下。
	**model_name**: 训练采用的数据集名称（或者使用的预训练权重的数据名称）。训练后产生的日志和权重会保存在outputs/{model_name}目录中。model_name目前的可选值有：’14lap’, ‘14res’, ‘15res’, ‘16res’。
	**random_seed**: 随机种子。

　　3.运行

```
python main.py 
```

​	并在pred/{data}目录下查看三元组提取结果。

　　

### 引用：

```
　　@inproceedings{xu-etal-2021-learning,

　　    title = "Learning Span-Level Interactions for Aspect Sentiment Triplet Extraction",

　　    author = "Xu, Lu  and

　　      Chia, Yew Ken  and

　　      Bing, Lidong",

　　    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",

　　    month = aug,

　　    year = "2021",

　　    address = "Online",

　　    publisher = "Association for Computational Linguistics",

　　    url = "https://aclanthology.org/2021.acl-long.367",

　　    doi = "10.18653/v1/2021.acl-long.367",

　　    pages = "4755--4766",

　　    abstract = "Aspect Sentiment Triplet Extraction (ASTE) is the most recent subtask of ABSA which outputs triplets of an aspect target, its associated sentiment, and the corresponding opinion term. Recent models perform the triplet extraction in an end-to-end manner but heavily rely on the interactions between each target word and opinion word. Thereby, they cannot perform well on targets and opinions which contain multiple words. Our proposed span-level approach explicitly considers the interaction between the whole spans of targets and opinions when predicting their sentiment relation. Thus, it can make predictions with the semantics of whole spans, ensuring better sentiment consistency. To ease the high computational cost caused by span enumeration, we propose a dual-channel span pruning strategy by incorporating supervision from the Aspect Term Extraction (ATE) and Opinion Term Extraction (OTE) tasks. This strategy not only improves computational efficiency but also distinguishes the opinion and target spans more properly. Our framework simultaneously achieves strong performance for the ASTE as well as ATE and OTE tasks. In particular, our analysis shows that our span-level approach achieves more significant improvements over the baselines on triplets with multi-word targets or opinions.",

　　}
```

