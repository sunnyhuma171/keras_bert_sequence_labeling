# -*- coding: utf-8 -*-
# @Time : 2020/12/24 13:26
# @Author : Jclian91
# @File : util.py
# @Place : Yangpu, Shanghai

# 数据相关的配置
event_type = "example"

train_file_path = "./data/%s.train" % event_type
dev_file_path = "./data/%s.dev" % event_type
test_file_path = "./data/%s.test" % event_type

# 模型相关的配置
MAX_SEQ_LEN = 128   # 输入的文本最大长度