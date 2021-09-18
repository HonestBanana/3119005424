import jieba.analyse
import jieba  # 汉语文本分析包（jieba）
import html  # html的包
import re  # 正则表达式的包
import sys



class JaccardSimilarity(object):
    # 使用jaccard算法，其中的相似度
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取文本中的关键词
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)  # 正则过滤html标签
        content = html.unescape(content)  # 将html转义符实体化
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']  # 切割
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)  # 提取关键词
        return keywords

    def main(self):
        keywords_x = self.extract_keyword(self.s1)
        keywords_y = self.extract_keyword(self.s2)  # 分词与关键词提取
        intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
        union = len(list(set(keywords_x).union(set(keywords_y))))  # jaccard相似度计算
        sim = float(intersection) / union if union != 0 else 0  # 除零处理
        return sim
  
def openfile():
    flag1 = True
    while flag1:
        try:
            text1 = input('Please input original file:\n')
            text3 = input('The location you want to storage:\n')  #打开文件对比操作
            f = open(text1, 'r', encoding='utf-8')
            answer = open(text3, 'a+', encoding='utf-8')
            f1 = f.read()
            flag1 = False
            flag2 = True
            i = 1
        except FileNotFoundError:
            print('文件路径错误！')
            judge = input('结束了吗？(input Y or y to quit/press any key to continue)\n')
            if judge == 'Y' or judge == 'y':
                sys.exit()
            else:
                flag1 = True
    while flag2:
        try:
            text2 = input(f'Please input file {i+1}:\n')
            g = open(text2, 'r', encoding='utf-8')
            g1 = g.read()
            similarity = JaccardSimilarity(f1, g1)
            similarity = similarity.main()
            strings = f'原文件和文件{i+1}相似度: %.2f%%' % (similarity * 100) + "\n"
            answer.writelines(strings)
            print(strings)
            f.close()
            g.close()
            i+=1
            judge = input('结束了吗？(input Y or y to quit/press any key to continue)\n')
            if judge == 'Y' or judge == 'y':
                flag2 = False
                answer.close()
        except FileNotFoundError:
            print('文件路径错误！')
            judge = input('结束了吗？(input Y or y to quit/press any key to continue)\n')
            if judge == 'Y' or judge == 'y':
                flag2 = False
                answer.close()





if __name__ == '__main__':
    openfile()
