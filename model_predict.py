# -*- coding: utf-8 -*-
# @Time : 2020/12/24 13:28
# @Author : Jclian91
# @File : model_predict.py
# @Place : Yangpu, Shanghai
import numpy as np
from pprint import pprint
from keras.models import load_model
from keras_bert import get_custom_objects
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_accuracy

from util import event_type
from model_train import PreProcessInputData, id_label_dict


# 将BIO标签转化为方便阅读的json格式
def bio_to_json(string, tags):
    item = {"string": string, "entities": []}
    entity_name = ""
    entity_start = 0
    iCount = 0
    entity_tag = ""

    for c_idx in range(min(len(string), len(tags))):
        c, tag = string[c_idx], tags[c_idx]
        if c_idx < len(tags)-1:
            tag_next = tags[c_idx+1]
        else:
            tag_next = ''

        if tag[0] == 'B':
            entity_tag = tag[2:]
            entity_name = c
            entity_start = iCount
            if tag_next[2:] != entity_tag:
                item["entities"].append({"word": c, "start": iCount, "end": iCount + 1, "type": tag[2:]})
        elif tag[0] == "I":
            if tag[2:] != tags[c_idx-1][2:] or tags[c_idx-1][2:] == 'O':
                tags[c_idx] = 'O'
                pass
            else:
                entity_name = entity_name + c
                if tag_next[2:] != entity_tag:
                    item["entities"].append({"word": entity_name, "start": entity_start, "end": iCount + 1, "type": entity_tag})
                    entity_name = ''
        iCount += 1
    return item


# 加载训练好的模型
custom_objects = get_custom_objects()
for key, value in {'CRF': CRF, 'crf_loss': crf_loss, 'crf_accuracy': crf_accuracy}.items():
    custom_objects[key] = value
model = load_model("%s_ner.h5" % event_type, custom_objects=custom_objects)

# 测试句子
text = "最近一段时间，印度政府在南海问题上接连发声。在近期印度、越南两国举行的线上总理峰会上，印度总理莫迪声称南海行为准则“不应损害该地区其他" \
       "国家或第三方的利益”，两国总理还强调了所谓南海“航行自由”的重要性。"
word_labels, seq_types = PreProcessInputData([text])

# 模型预测
predicted = model.predict([word_labels, seq_types])
y = np.argmax(predicted[0], axis=1)
tag = [id_label_dict[_] for _ in y]

# 输出预测结果
result = bio_to_json(text, tag[1:-1])
pprint(result)
