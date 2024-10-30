import pandas
import regex as re

from pypinyin import pinyin, lazy_pinyin, Style
import keyboard
import json

#读字频
fre = pandas.read_csv("./字频.txt")
fre = fre.to_dict("list")
字频 = fre["字"]

#读拆分字典
df = pandas.read_csv("./拆分字典.txt",sep="\t")#读为DataFrame
拆分字典 = df.set_index('字')['拆'].to_dict()#转换为字典
拆分字典 = {key: re.findall(r'〔(.*?)〕', value) for key, value in 拆分字典.items()}#音str拆成list

#读字词频
df = pandas.read_csv("字词频.txt", sep="\t")
字词频 = df.to_dict("records")


#分析2：有多少多音字有歧义（拆分数据里的声母对应这个字的两个音的声母都相同，不知取哪个）
n = 0
m = 0
global_dict = {}

# def 去声调(pinyin_list):
#     # 去声调字典，用于替换带调的韵母
#     声调映射 = {
#         'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a',
#         'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e',
#         'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
#         'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
#         'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
#         'ǖ': 'Ü', 'ǘ': 'Ü', 'ǚ': 'Ü', 'ǜ': 'Ü',
#         # 如果需要处理其他带调的拼音，可以继续添加
#     }
#
#     # 初始化一个空列表，用于存储处理后的拼音
#     processed_pinyin = []
#
#     # 遍历输入的拼音列表
#     for sublist in pinyin_list:
#         # 遍历子列表中的每个拼音
#         for pinyin in sublist:
#             # 去除声调
#             for tone, no_tone in 声调映射.items():
#                 pinyin = pinyin.replace(tone, no_tone)
#                 # 添加到处理后的列表中
#             processed_pinyin.append(pinyin)
#
#             # 去除重复项
#     unique_pinyin = list(set(processed_pinyin))
#
#     # 返回处理后的拼音列表，转换成列表的列表形式
#     return [list(unique_pinyin)]
# 分析 = 0
# def 计算剩余():
#     global n
#     n += 1
# def func(字, 部, 辅, 音列表,哪个部):
#     global n,m,分析
#     n = 0
#     m += 1
#     分析 = 1
#     Main()
#     分析 = 0
#     print(f"总共{n}字，第{m}字：",字, 部, 辅, 音列表, 哪个部, end="")
#
#     输入音 = input("\t选择音:")
#     if 输入音[:3]=="ds ":
#         输入音 = 输入音[3:]
#         with open("ds.json", 'r') as f:
#             data_dict = json.load(f)  # 读取JSON文件内容到字典
#         data_dict[部] = 输入音
#         with open("ds.json", 'w') as f:
#             json.dump(data_dict, f)
#     with open('a.txt', 'a', encoding='utf-8') as file:
#         line_to_append = 字 + '\t' + 哪个部 + '\t' + 输入音 + '\n'
#         file.write(line_to_append)
#
def 情景取音(拼音,辅):
    if 辅 == "v":
        if 拼音[:2] != "zh":
            return "【错误】zh不匹配"
        else:
            return 拼音
    if 辅 == "u":
        if 拼音[:2] != "sh":
            return "【错误】sh不匹配"
        else:
            return 拼音
    if 辅 == "i":
        if 拼音[:2] != "ch":
            return "【错误】zh不匹配"
        else:
            return 拼音
    if 辅 == "a":
        if 拼音 in["heng","shu","zhe"]:
            return 拼音
    if 辅 == "f":
        if 拼音 == "shou":
            return 拼音
    if 辅 == "d":
        if 拼音 in ["shui","huo"]:
            return 拼音
    if 辅 == "o":
        if 拼音 in ["ri","yue","mu"]:
            return 拼音
    if 辅 != 拼音[0]:
        return "【错误】声母不匹配"
    else:
        return 拼音

def 获取辅码(字词):
    try:
        for 字 in 字词:
            拆分字典[字]
    except KeyError:
        return ["【错误】字典缺字"]
    if len(字词) == 1:
        字 = 字词
        # if not 拆分字典[字]:
        #     return ["【错误】查不到这个字的拆分数据"]
        单字全辅 = []
        for 拆分 in 拆分字典[字]:
            if re.fullmatch(r'^\p{Han}{2}[a-z]{2}$', 拆分):
                部首 = 拆分[0]
                部首辅 = 拆分[2]
                余部 = 拆分[1]
                余部辅 = 拆分[3]

                部首拼音 = lazy_pinyin(部首,errors="ignore")
                余部拼音 = lazy_pinyin(余部, errors="ignore")
                if len(部首拼音) == 0 or len(余部拼音) == 0:
                    return ["【错误】有部件查不到音"]

                部首全辅 = 情景取音(部首拼音[0],部首辅)
                余部全辅 = 情景取音(余部拼音[0],余部辅)
                单字全辅.append(部首全辅)
                单字全辅.append(部首全辅 + 余部全辅)
            else:
                return ["【错误】有拆分数据不是“字字aa”格式"]
        单字全辅 = list(set(单字全辅))  # 去重
        return 单字全辅
    else:
        词辅 = []
        if not 拆分字典[字词[0]] or not 拆分字典[字词[1]]:
            return ["【错误】有字查不到拆分数据"]
        for 首字拆分 in 拆分字典[字词[0]]:
            for 次字拆分 in 拆分字典[字词[1]]:
                if not re.fullmatch(r'^\p{Han}{2}[a-z]{2}$', 首字拆分):
                    return ["【错误】首字拆分数据不是“字字aa”格式"]
                if not re.fullmatch(r'^\p{Han}{2}[a-z]{2}$', 次字拆分):
                    return ["【错误】次字拆分数据不是“字字aa”格式"]
                首字 = 首字拆分[0]
                首字辅 = 首字拆分[2]
                次字 = 次字拆分[0]
                次字辅 = 次字拆分[2]

                首字拼音 = lazy_pinyin(首字,errors="ignore")
                次字拼音 = lazy_pinyin(次字, errors="ignore")
                if len(首字拼音) == 0 or len(次字拼音) == 0:
                    return ["【错误】这个词有字查不到拆分"]

                首字全辅 = 情景取音(首字拼音[0],首字辅)
                次字全辅 = 情景取音(次字拼音[0],次字辅)
                词辅.append(首字全辅 + 次字全辅)
                词辅.append(首字全辅)
        词辅 = list(set(词辅))#去重
        return 词辅
def 转数字(字符串):
    替换表 = str.maketrans("abcdefghijklmnopqrstuvwxyz","22233344455566677778889999")
    return str(字符串).translate(替换表)
计数簿 = {}
def 计算序号(码):
    global 计数字典
    if 码 not in 计数簿:
        计数簿[码] = 1
        return 1
    else:
        计数簿[码] += 1
        if 计数簿[码] > 64:
            计数簿[码] = 64
        return 计数簿[码]
def Main():
    表 = []
    for 字词行 in 字词频:
        辅码列表 = 获取辅码(字词行["字词"])
        for 辅码 in 辅码列表:
            行 = {}
            行["字词"] = 字词行["字词"]
            行["拼音"] = str(字词行["拼音"]).replace(" ","")
            行["频率"] = 字词行["词频"]
            行["辅码"] = 辅码
            行["全码"] =  行["拼音"] + "1" + 行["辅码"]
            行["数字全码"] = 转数字(行["全码"])
            行["序号"] = 计算序号(行["数字全码"])
            行["手心格式"] = 行["全码"] + "=" + str(行["序号"]) + "," + 行["字词"]
            表.append(行)



    df = pandas.DataFrame(表)
    df.to_csv("码表.csv", index=False)
    df["手心格式"].to_csv("手心码表.txt",quoting=csv.QUOTE_NONE,index=False,header=False)
Main()