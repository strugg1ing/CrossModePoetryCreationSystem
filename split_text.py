import jieba.analyse

def extract_keywords_from_file(input_file_path, output_file_path, top=20, with_weight=False, allowPOS=[]):
    """
    从输入的文本文件中提取关键词，并将结果写入到输出文件。
    """
    # 读取输入文件中的文本内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 使用jieba的关键词提取功能
    keywords = jieba.analyse.extract_tags(text, withWeight=with_weight, allowPOS=allowPOS)

    # 将关键词写入到输出文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        if with_weight:
            # 如果提取时包含了权重，则写入"词:权重"格式
            file.write('\n'.join([f'{word}: {weight}' for word, weight in keywords]))
        else:
            # 如果没有包含权重，则只写入关键词
            file.write('\n'.join(word for word in keywords))

# 输入输出文件路径
input_file_path = 'output_temp.txt'  # 替换为你的输入文件路径
output_file_path = 'output_key.txt'  # 替换为你想要输出的文件路径

# 提取关键词并写入到文件
extract_keywords_from_file(input_file_path, output_file_path)