#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Aeneas(aeneas.he@gmail.com)
# CreateDate: 2019-2-21

# python main.py 1977 8 11 19 -w


from lunar_python import Lunar, Solar
from colorama import init
from sizi import summarys
from yue import months

from datas import *
from common import *
from gets import *
from inputs import get_mingzao
from dayun import get_yun

# 命造八字基础信息
ming = get_mingzao()

ming.get_shens()


class MingEngine:
    def __init__(self):

        self.direction = None  # 计算大运的方向
        self.dayuns = None  # 大运
        self.scores = None  # 分数
        self.strong = None  # 强弱
        self.weak = None  # 强弱

    #     # 计算五行分数
    #     # http://www.131.com.tw/word/b3_2_14.htm
    #     # self.ming=ming
    #     pass

    def get_base(self):

        # 计算八字中五行和天干（包括地支藏干）的数量
        scores = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}

        gan_scores = {
            "甲": 0,
            "乙": 0,
            "丙": 0,
            "丁": 0,
            "戊": 0,
            "己": 0,
            "庚": 0,
            "辛": 0,
            "壬": 0,
            "癸": 0,
        }

        for item in ming.gans:
            scores[gan5[item]] += 5
            gan_scores[item] += 5

        for item in list(ming.zhis) + [ming.zhis.month]:
            for gan in zhi5[item]:
                scores[gan5[gan]] += zhi5[item][gan]
                gan_scores[gan] += zhi5[item][gan]

        self.scores = scores
        self.gan_scores = gan_scores

        # print(self.scores)
        # print(self.gan_scores)

        # 计算八字强弱（子平真诠的计算方法）
        weak = True
        me_status = []
        for item in ming.zhis:
            me_status.append(ten_deities[ming.me][item])
            if ten_deities[ming.me][item] in ("长", "帝", "建"):
                weak = False

        if weak:
            if ming.shens.count("比") + me_status.count("库") > 2:
                weak = False
        self.weak = weak
        print("\n八字强弱：", self.weak)

        # 计算起运的方向
        seq = Gan.index(ming.gans.year)
        if ming.is_women:
            if seq % 2 == 0:
                direction = -1
            else:
                direction = 1
        else:
            if seq % 2 == 0:
                direction = 1
            else:
                direction = -1

        self.direction = direction

        dayuns = []
        gan_seq = Gan.index(ming.gans.month)
        zhi_seq = Zhi.index(ming.zhis.month)
        for i in range(12):
            gan_seq += direction
            zhi_seq += direction
            dayuns.append(Gan[gan_seq % 10] + Zhi[zhi_seq % 12])

        self.dayuns = dayuns
        # print("大运:", self.dayuns)
        # 网上的计算
        me_attrs_ = ten_deities[ming.me].inverse
        strong = (
            self.gan_scores[me_attrs_["比"]]
            + self.gan_scores[me_attrs_["劫"]]
            + self.gan_scores[me_attrs_["枭"]]
            + self.gan_scores[me_attrs_["印"]]
        )
        self.strong = strong
        print("八字强弱程度：", self.strong)

        print("-" * 120)
        # print(zhi_3hes, "生：寅申巳亥 败：子午卯酉　库：辰戌丑未")
        # print("地支六合:", zhi_6hes)

        # out = ""
        # for item in zhi_3hes:
        #     out = out + "{}:{}  ".format(item, zhi_3hes[item])
        # print(out)

        # 输出八字排盘

        # 主星
        print(" ".join(list(ming.gan_shens)), " " * 5)

        # 天干
        print("\033[1;31;40m" + " ".join(list(ming.gans)) + "\033[0m", " " * 5)

        # 地支
        print("\033[1;31;40m" + " ".join(list(ming.zhis)) + "\033[0m", " " * 5)

        # 副星
        # print(
        #     "\033[1;31;40m" + " ".join(list(ming.zhi_shens2)) + "\033[0m" + "\033[0m",
        #     " " * 5,
        # )

        for cang in ming.zhi_shen3:
            try:
                print(cang[0], end=" ")
            except:
                print(" ", end=" ")
        print()
        for cang in ming.zhi_shen3:
            try:
                print(cang[1], end=" ")
            except:
                print(" ", end=" ")
        print()
        for cang in ming.zhi_shen3:
            try:
                print(cang[2], end=" ")
            except:
                print(" ", end=" ")
        print()

        print("-" * 120)
        print(
            "{1:{0}^15s}{2:{0}^15s}{3:{0}^15s}{4:{0}^15s}".format(
                chr(12288),
                "【年】{}:{}{}{}".format(
                    temps[ming.gans.year],
                    temps[ming.zhis.year],
                    ten_deities[ming.gans.year].inverse["建"],
                    gan_zhi_he(ming.zhus[0]),
                ),
                "【月】{}:{}{}{}".format(
                    temps[ming.gans.month],
                    temps[ming.zhis.month],
                    ten_deities[ming.gans.month].inverse["建"],
                    gan_zhi_he(ming.zhus[1]),
                ),
                "【日】{}:{}{}".format(
                    temps[ming.me], temps[ming.zhis.day], gan_zhi_he(ming.zhus[2])
                ),
                "【时】{}:{}{}{}".format(
                    temps[ming.gans.time],
                    temps[ming.zhis.time],
                    ten_deities[ming.gans.time].inverse["建"],
                    gan_zhi_he(ming.zhus[3]),
                ),
            )
        )
        print("-" * 120)

        # 输出八字排盘详情
        print(
            "\033[1;32;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
                chr(12288),
                "{}{}{}【{}】{}".format(
                    ming.gans.year,
                    yinyang(ming.gans.year),
                    gan5[ming.gans.year],
                    ten_deities[ming.me][ming.gans.year],
                    check_gan(ming.gans.year, ming.gans),
                ),
                "{}{}{}【{}】{}".format(
                    ming.gans.month,
                    yinyang(ming.gans.month),
                    gan5[ming.gans.month],
                    ten_deities[ming.me][ming.gans.month],
                    check_gan(ming.gans.month, ming.gans),
                ),
                "{}{}{}{}".format(
                    ming.me,
                    yinyang(ming.me),
                    gan5[ming.me],
                    check_gan(ming.me, ming.gans),
                ),
                "{}{}{}【{}】{}".format(
                    ming.gans.time,
                    yinyang(ming.gans.time),
                    gan5[ming.gans.time],
                    ten_deities[ming.me][ming.gans.time],
                    check_gan(ming.gans.time, ming.gans),
                ),
            )
        )

        print(
            "\033[1;32;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
                chr(12288),
                "{}{}{}【{}】{}".format(
                    ming.zhis.year,
                    yinyang(ming.zhis.year),
                    ten_deities[ming.me][ming.zhis.year],
                    ten_deities[ming.gans.year][ming.zhis.year],
                    get_empty(ming.zhus[2], ming.zhis.year),
                ),
                "{}{}{}【{}】{}".format(
                    ming.zhis.month,
                    yinyang(ming.zhis.month),
                    ten_deities[ming.me][ming.zhis.month],
                    ten_deities[ming.gans.month][ming.zhis.month],
                    get_empty(ming.zhus[2], ming.zhis.month),
                ),
                "{}{}{}".format(
                    ming.zhis.day,
                    yinyang(ming.zhis.day),
                    ten_deities[ming.me][ming.zhis.day],
                ),
                "{}{}{}【{}】{}".format(
                    ming.zhis.time,
                    yinyang(ming.zhis.time),
                    ten_deities[ming.me][ming.zhis.time],
                    ten_deities[ming.gans.time][ming.zhis.time],
                    get_empty(ming.zhus[2], ming.zhis.time),
                ),
            )
        )

        self.statuses = [ten_deities[ming.me][item] for item in ming.zhis]

        for seq, item in enumerate(ming.zhis):
            out = ""
            multi = 2 if item == ming.zhis.month and seq == 1 else 1

            for gan in zhi5[item]:
                out = out + "{}{}{}　".format(gan, gan5[gan], ten_deities[ming.me][gan])
            print(
                "\033[1;32;40m{1:{0}<15s}\033[0m".format(chr(12288), out.rstrip("　")),
                end="",
            )

        print()
        print("================")

    def get_relationship(self):
        # 基本盘的害破会行

        # 输出地支关系
        for seq, item in enumerate(ming.zhis):

            output = ""
            others = ming.zhis[:seq] + ming.zhis[seq + 1 :]
            for type_ in zhi_atts[item]:
                flag = False
                if type_ in ("害", "破", "会", "刑"):
                    continue
                for zhi in zhi_atts[item][type_]:
                    if zhi in others:
                        if not flag:
                            output = (
                                output + "　" + type_ + "："
                                if type_ not in ("冲", "暗")
                                else output + "　" + type_
                            )
                            flag = True
                        if type_ not in ("冲", "暗"):
                            output += zhi
                output = output.lstrip("　")
            print("\033[1;32;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end="")

        print()

        # 输出地支minor关系
        for seq, item in enumerate(ming.zhis):

            output = ""
            others = ming.zhis[:seq] + ming.zhis[seq + 1 :]
            for type_ in zhi_atts[item]:
                flag = False
                if type_ not in ("害", "会"):
                    continue
                for zhi in zhi_atts[item][type_]:
                    if zhi in others:
                        if not flag:
                            output = output + "　" + type_ + "："
                            flag = True
                        output += zhi
            output = output.lstrip("　")
            print("\033[1;32;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end="")

        print()

        # 输出天干的通根
        for item in ming.gans:
            output = output.lstrip("　")
            print(
                "\033[1;32;40m{1:{0}<15s}\033[0m".format(
                    chr(12288), get_gen(item, ming.zhis)
                ),
                end="",
            )

        print()

        for seq, item in enumerate(ming.zhus):

            # 检查空亡
            result = (
                "{}－{}".format(nayins[item], "亡")
                if ming.zhis[seq] == wangs[ming.zhis[0]]
                else nayins[item]
            )

            # 天干与地支关系
            result = (
                relations[(gan5[ming.gans[seq]], zhi_wuhangs[ming.zhis[seq]])] + result
            )

            # 检查劫杀
            result = (
                "{}－{}".format(result, "劫杀")
                if ming.zhis[seq] == jieshas[ming.zhis[0]]
                else result
            )
            # 检查元辰
            result = (
                "{}－{}".format(result, "元辰")
                if ming.zhis[seq]
                == Zhi[(Zhi.index(ming.zhis[0]) + self.direction * -1 * 5) % 12]
                else result
            )
            print("{1:{0}<15s} ".format(chr(12288), result), end="")

        print()
        # 计算干合:相邻的才算合

        gan_he = [False, False, False, False]
        for i in range(3):
            if (ming.gans[i], ming.gans[i + 1]) in set(gan_hes) or (
                ming.gans[i + 1],
                ming.gans[i],
            ) in set(gan_hes):
                gan_he[i] = gan_he[i + 1] = True
        self.gan_he = gan_he

        # 计算地支六合:相邻的才算合

        zhi_6he = [False, False, False, False]

        for i in range(3):
            if zhi_atts[ming.zhis[i]]["六"] == ming.zhis[i + 1]:
                zhi_6he[i] = zhi_6he[i + 1] = True

        self.zhi_6he = zhi_6he

        # 计算地支六冲:相邻的才算合

        zhi_6chong = [False, False, False, False]

        for i in range(3):
            if zhi_atts[ming.zhis[i]]["冲"] == ming.zhis[i + 1]:
                zhi_6chong[i] = zhi_6chong[i + 1] = True
        self.zhi_6chong = zhi_6chong

        # 计算地支刑:相邻的才算

        zhi_xing = [False, False, False, False]

        for i in range(3):
            if (
                zhi_atts[ming.zhis[i]]["刑"] == ming.zhis[i + 1]
                or zhi_atts[ming.zhis[i + 1]]["刑"] == ming.zhis[i]
            ):
                zhi_xing[i] = zhi_xing[i + 1] = True
        self.zhi_xing = zhi_xing

    # 十神
    def get_shens(self):
        self.all_ges = []

        strs = [
            "",
            "",
            "",
            "",
        ]

        all_shens = set()
        all_shens_list = []

        for item in year_shens:
            for i in (1, 2, 3):
                if ming.zhis[i] in year_shens[item][ming.zhis.year]:
                    strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
                    all_shens.add(item)
                    all_shens_list.append(item)

        for item in month_shens:
            for i in range(4):
                if (
                    ming.gans[i] in month_shens[item][ming.zhis.month]
                    or ming.zhis[i] in month_shens[item][ming.zhis.month]
                ):
                    strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
                    if i == 2 and ming.gans[i] in month_shens[item][ming.zhis.month]:
                        strs[i] = strs[i] + "●"
                    all_shens.add(item)
                    all_shens_list.append(item)

        for item in day_shens:
            for i in (0, 1, 3):
                if ming.zhis[i] in day_shens[item][ming.zhis.day]:
                    strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
                    all_shens.add(item)
                    all_shens_list.append(item)

        for item in g_shens:
            for i in range(4):
                if ming.zhis[i] in g_shens[item][ming.me]:
                    strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
                    all_shens.add(item)
                    all_shens_list.append(item)

        self.all_shens = all_shens
        self.all_shens_list = all_shens_list

        for seq in range(2):
            print("{1:{0}<15s} ".format(chr(12288), strs[seq]), end="")
        for seq in range(2, 4):
            print("{1:{0}<14s} ".format(chr(12288), strs[seq]), end="")

    def get_dayun(self):
        print()
        print("-" * 120)
        print("大运：", end=" ")

        for item in self.dayuns:
            print(item, end=" ")
        print()
        # for item in ming.gans:
        #     print(get_gen(item, ming.zhis), end=" \t")
        # print()
        print("-" * 120)

        self.me_lu = ten_deities[ming.me].inverse["建"]
        self.me_jue = ten_deities[ming.me].inverse["绝"]
        self.me_tai = ten_deities[ming.me].inverse["胎"]
        self.me_di = ten_deities[ming.me].inverse["帝"]

        # 劫
        self.jie = ten_deities[ming.me].inverse["劫"]

        # 伤官
        self.shang = ten_deities[ming.me].inverse["伤"]
        self.shang_lu = ten_deities[self.shang].inverse["建"]
        self.shang_di = ten_deities[self.shang].inverse["帝"]

        # 食
        self.shi = ten_deities[ming.me].inverse["食"]
        self.shi_lu = ten_deities[self.shi].inverse["建"]
        self.shi_di = ten_deities[self.shi].inverse["帝"]

        # 财
        self.cai = ten_deities[ming.me].inverse["财"]
        self.cai_lu = ten_deities[self.cai].inverse["建"]
        self.cai_di = ten_deities[self.cai].inverse["帝"]

        # 偏财
        self.piancai = ten_deities[ming.me].inverse["才"]
        self.piancai_lu = ten_deities[self.piancai].inverse["建"]
        self.piancai_di = ten_deities[self.piancai].inverse["帝"]

        # 官
        self.guan = ten_deities[ming.me].inverse["官"]
        self.guan_lu = ten_deities[self.guan].inverse["建"]
        self.guan_di = ten_deities[self.guan].inverse["帝"]

        # 杀
        self.sha = ten_deities[ming.me].inverse["杀"]
        self.sha_lu = ten_deities[self.sha].inverse["建"]
        self.sha_di = ten_deities[self.sha].inverse["帝"]

        # 印
        self.yin = ten_deities[ming.me].inverse["印"]
        self.yin_lu = ten_deities[self.yin].inverse["建"]

        # 枭
        self.xiao = ten_deities[ming.me].inverse["枭"]
        self.xiao_lu = ten_deities[self.xiao].inverse["建"]

        # 库
        self.me_ku = ten_deities[ming.me]["库"][0]
        self.cai_ku = ten_deities[self.cai]["库"][0]
        self.guan_ku = ten_deities[self.guan]["库"][0]
        self.yin_ku = ten_deities[self.yin]["库"][0]
        self.shi_ku = ten_deities[self.shi]["库"][0]

        print(
            "调候：",
            tiaohous["{}{}".format(ming.me, ming.zhis[1])],
            "\t##金不换大运：",
            jinbuhuan["{}{}".format(ming.me, ming.zhis[1])],
        )
        print("金不换大运：说明：", jins["{}".format(ming.me)])

    def get_geju(self):

        print("格局选用：", ges[ten_deities[ming.me]["本"]][ming.zhis[1]])

        if len(set("寅申巳亥") & set(ming.zhis)) == 0:
            print("缺四生：一生不敢作为")
        if len(set("子午卯酉") & set(ming.zhis)) == 0:
            print("缺四柱地支缺四正，一生避是非")
        if len(set("辰戌丑未") & set(ming.zhis)) == 0:
            print("四柱地支缺四库，一生没有潜伏性凶灾。")
        if (
            "甲",
            "戊",
            "庚",
        ) in (tuple(ming.gans)[:3], tuple(ming.gans)[1:]):
            print("地上三奇：白天生有申佳，需身强四柱有贵人。")
        if (
            "辛",
            "壬",
            "癸",
        ) in (tuple(ming.gans)[:3], tuple(ming.gans)[1:]):
            print("人间三奇，需身强四柱有贵人。")
        if (
            "乙",
            "丙",
            "丁",
        ) in (tuple(ming.gans)[:3], tuple(ming.gans)[1:]):
            print("天上三奇：晚上生有亥佳，需身强四柱有贵人。")

        if ming.zhi_shens2.count("亡神") > 1:
            print("二重亡神，先丧母；")

        if get_empty(ming.zhus[2], ming.zhis.time):
            print("时坐空亡，子息少。 母法P24-41 母法P79-4：损破祖业，后另再成就。")

        if ming.zhis.count(self.me_jue) + ming.zhis.count(self.me_tai) > 2:
            print("胎绝超过3个：夭或穷。母法P24-44 丁未 壬子 丙子 戊子")

        if (
            not_yang(ming.me)
            and zhi_ku(ming.zhis[2], (ming.me, self.jie))
            and zhi_ku(ming.zhis[3], (ming.me, self.jie))
        ):
            print(
                "阴日主时日支入比劫库：性格孤独，难发达。母法P28-112 甲申 辛未 辛丑 己丑 母法P55-11 为人孤独，且有灾疾"
            )

        # print(cai_lu, piancai_lu)
        if (
            ming.zhis[1:].count(self.piancai_lu)
            + ming.zhis[1:].count(self.cai_lu)
            + ming.zhis[1:].count(self.piancai_di)
            + ming.zhis[1:].count(self.cai_di)
            == 0
        ):
            print("月日时支没有财或偏财的禄旺。")

        if ming.zhis[1:].count(self.guan_lu) + ming.zhis[1:].count(self.guan_di) == 0:
            print("月日时支没有官的禄旺。")

        if "辰" in ming.zhis and ("戌" not in ming.zhis) and ming.is_women:
            print("女命有辰无戌：孤。")
        if "戌" in ming.zhis and ("辰" not in ming.zhis) and ming.is_women:
            print("女命有戌无辰：带禄。")

        if emptie4s.get(ming.zhus[2], 0) != 0:
            if self.scores[emptie4s.get(ming.zhus[2], 0)] == 0:
                print("四大空亡：33岁以前身体不佳！")

        for item in self.all_shens:
            print(item, ":", shens_infos[item])

        if ming.is_women:
            print("#" * 20, "女命")
            if self.all_shens_list.count("驿马") > 1:
                print("二逢驿马，母家荒凉。P110 丙申 丙申 甲寅 丁卯")
            if ming.gan_shens[0] == "伤":
                print("年上伤官：带疾生产。P110 戊寅 戊午 丁未 丁未")

        print("-" * 120)

        children = ["食", "伤"] if ming.is_women else ["官", "杀"]
        print("子嗣: ", children)

        liuqins = bidict(
            {
                "才": "父亲",
                "财": "财" if ming.is_women else "妻",
                "印": "母亲",
                "枭": "偏印" if ming.is_women else "祖父",
                "官": "丈夫" if ming.is_women else "女儿",
                "杀": "情夫" if ming.is_women else "儿子",
                "劫": "兄弟" if ming.is_women else "姐妹",
                "比": "姐妹" if ming.is_women else "兄弟",
                "食": "女儿" if ming.is_women else "下属",
                "伤": "儿子" if ming.is_women else "孙女",
            }
        )

        # 六亲分析
        for item in Gan:
            print(
                "{}:{} {}-{} {} {} {}".format(
                    item,
                    ten_deities[ming.me][item],
                    liuqins[ten_deities[ming.me][item]],
                    ten_deities[item][ming.zhis[0]],
                    ten_deities[item][ming.zhis[1]],
                    ten_deities[item][ming.zhis[2]],
                    ten_deities[item][ming.zhis[3]],
                ),
                end="  ",
            )
            if Gan.index(item) == 4:
                print()
        print()

        # 计算上运时间，有年份时才适用

        temps_scores = (
            temps[ming.gans.year]
            + temps[ming.gans.month]
            + temps[ming.me]
            + temps[ming.gans.time]
            + temps[ming.zhis.year]
            + temps[ming.zhis.month] * 2
            + temps[ming.zhis.day]
            + temps[ming.zhis.time]
        )
        print(
            "\033[1;32;40m五行分数",
            self.scores,
            "  \n八字强弱：",
            self.strong,
            "通常>29为强，需要参考月份、坐支等",
            "weak:",
            self.weak,
        )

        gongs = get_gong(ming.zhis, ming.gans)
        ming.zhis_g = set(ming.zhis) | set(gongs)

        jus = []
        for item in zhi_hes:
            if set(item).issubset(ming.zhis_g):
                print("三合局", item)
                jus.append(ju[ten_deities[ming.me].inverse[zhi_hes[item]]])

        for item in zhi_huis:
            if set(item).issubset(ming.zhis_g):
                print("三会局", item)
                jus.append(ju[ten_deities[ming.me].inverse[zhi_huis[item]]])
        self.jus = jus
        print(
            "湿度分数",
            temps_scores,
            "正为暖燥，负为寒湿，正常区间[-6,6] 拱：",
            get_gong(ming.zhis, ming.gans),
            "\033[0m",
        )

        for item in self.gan_scores:
            print(
                "{}[{}]-{} ".format(
                    item, ten_deities[ming.me][item], self.gan_scores[item]
                ),
                end="  ",
            )
        print()
        print("-" * 120)
        yinyangs(ming.zhis)
        self.shen_zhus = list(zip(ming.gan_shens, ming.zhi_shens))

        minggong = Zhi[::-1][
            (Zhi.index(ming.zhis[1]) + Zhi.index(ming.zhis[3]) - 6) % 12
        ]
        print(minggong, minggongs[minggong])
        print("坐：", rizhus[ming.me + ming.zhis.day])

        # 地网
        if "辰" in ming.zhis and "巳" in ming.zhis:
            print("地网：地支辰巳。天罗：戌亥。天罗地网全凶。")

        # 天罗
        if "戌" in ming.zhis and "亥" in ming.zhis:
            print("天罗：戌亥。地网：地支辰巳。天罗地网全凶。")

    # 计算格局
    def get_geju2(self):
        # 魁罡格
        if ming.zhus[2] in (
            ("庚", "辰"),
            ("庚", "戌"),
            ("壬", "辰"),
            ("戊", "戌"),
        ):
            print(
                "魁罡格：基础96，日主庚辰,庚戌,壬辰, 戊戌，重叠方有力。日主强，无刑冲佳。"
            )
            print(
                "魁罡四柱曰多同，贵气朝来在此中，日主独逢冲克重，财官显露祸无穷。魁罡重叠是贵人，天元健旺喜临身，财官一见生灾祸，刑煞俱全定苦辛。"
            )

        # 金神格
        if ming.zhus[3] in (("乙", "丑"), ("己", "巳"), ("癸", "酉")):
            print(
                "金神格：基础97，时柱乙丑、己巳、癸酉。只有甲和己日，甲日为主，甲子、甲辰最突出。月支通金火2局为佳命。不通可以选其他格"
            )

        # 六阴朝阳
        if ming.me == "辛" and ming.zhis.time == "子":
            print("六阴朝阳格：基础98，辛日时辰为子。")

        # 六乙鼠贵
        if ming.me == "乙" and ming.zhis.time == "子":
            print(
                "六阴朝阳格：基础99，乙日时辰为子。忌讳午冲，丑合，不适合有2个子。月支最好通木局，水也可以，不适合金火。申酉大运有凶，午也不行。夏季为伤官。入其他格以格局论。"
            )

        # 从格
        if max(self.scores.values()) > 25:
            print("有五行大于25分，需要考虑专格或者从格。")
            print("从旺格：安居远害、退身避位、淡泊名利,基础94;从势格：日主无根。")

        if self.zhi_6he[3]:
            if abs(Gan.index(ming.gans[3]) - Gan.index(ming.gans[2])) == 1:
                print("日时干邻支合：连珠得合：妻贤子佳，与事业无关。母法总则P21-11")

        for i, item in enumerate(ming.zhis):
            if item == self.me_ku:
                if ming.gan_shens[i] in ("才", "财"):
                    print("财坐劫库，大破败。母法P61-4 戊寅 丙辰 壬辰 庚子")

        # print(zhi_6chong[3], ming.gans, me)
        if self.zhi_6chong[3] and ming.gans[3] == ming.me:
            print(
                "日时天比地冲：女为家庭辛劳，男艺术宗教。 母法P61-5 己丑 丙寅 甲辰 甲戌"
            )

        # print(zhi_6chong[3], ming.gans, me)
        if self.zhi_xing[3] and gan_ke(ming.me, ming.gans[3]):
            print(
                "日时天克地刑：破败祖业、自立发展、后无终局。 母法P61-7 己丑 丙寅 甲午 庚午"
            )

        if (self.cai, self.yin_lu) in ming.zhus and (self.cai not in ming.zhi_shens2):
            print("浮财坐印禄:破祖之后，自己也败。 母法P78-29 辛丑 丁酉 壬寅 庚子")

        for i in range(3):
            if is_yang(ming.me):
                break
            if (
                self.zhi_xing[i]
                and self.zhi_xing[i + 1]
                and gan_ke(ming.gans[i], ming.gans[i + 1])
            ):
                print("阴日主天克地刑：孤独、双妻。 母法P61-7 己丑 丙寅 甲午 庚午")

        # 建禄格
        if ming.zhi_shens[1] == "比":
            self.all_ges.append("建")
            print(
                "建禄格：最好天干有财官。如果官杀不成格，有兄弟，且任性。有争财和理财的双重性格。如果创业独自搞比较好，如果合伙有完善的财务制度也可以。"
            )
            if ming.gan_shens[0] in "比劫":
                print("\t建禄年透比劫凶")
            elif "财" in ming.gan_shens and "官" in ming.gan_shens:
                print("\t建禄财官双透，吉")
            if ming.me in ("甲", "乙"):
                print(
                    "\t甲乙建禄四柱劫财多，无祖财，克妻，一生不聚财，做事虚诈，为人大模大样，不踏实。乙财官多可为吉。甲壬申时佳；乙辛巳时佳；"
                )

            if ming.me in ("丙"):
                print("\t丙：己亥时辰佳；")
            if ming.me in ("丁"):
                print("\t丁：阴男克1妻，阳男克3妻。财官多可为吉。庚子时辰佳；")
            if ming.me in ("戊"):
                print(
                    "\t戊：四柱无财克妻，无祖业，后代多事端。如合申子辰，子息晚，有2子。甲寅时辰佳；"
                )
            if ming.me in ("己"):
                print(
                    "\t己：即使官财出干成格，妻也晚。偏财、杀印成格为佳。乙丑时辰佳；"
                )
            if ming.me in ("庚"):
                print(
                    "\t庚：上半月生难有祖财，下半月较好，财格比官杀要好。丙戌时辰佳；"
                )
            if ming.me in ("辛"):
                print("\t辛：干透劫财，妻迟财少；丁酉时辰佳；")
            if ming.me in ("壬"):
                print("\t 壬：戊申时辰佳；")
            if ming.me in ("癸"):
                print("\t 癸：己亥时辰佳")

        # 甲分析

        if ming.me == "甲":
            if ming.zhis.count("辰") > 1 or ming.zhis.count("戌") > 1:
                print("甲日：辰或戌多、性能急躁不能忍。")
            if ming.zhis[2] == "子":
                print("甲子：调候要火。")
            if ming.zhis[2] == "寅":
                print("甲寅：有主见之人，需要财官旺支。")
            if ming.zhis[2] == "辰":
                print("甲辰：印库、性柔和而有实权。")
            if ming.zhis[2] == "午":
                print("甲午：一生有财、调候要水。")
            if ming.zhis[2] == "戌":
                print("甲戌：自坐伤官，不易生财，为人仁善。")

        if (
            ming.me in ("庚", "辛")
            and ming.zhis[1] == "子"
            and ming.zhis.count("子") > 1
        ):
            print("冬金子月，再有一子字，孤克。 母法P28-106 甲戌 丙子 庚子 丁丑")

    def get_shensha(self):
        print()
        print("-" * 120)
        print(
            "\033[1;31;40m",
            "【神煞】",
            "\033[0m",
        )
        # 计算星宿
        print("星宿", ming.lunar.getXiu(), ming.lunar.getXiuSong())

        # 计算建除
        seq = 12 - Zhi.index(ming.zhis.month)
        print(jianchus[(Zhi.index(ming.zhis.day) + seq) % 12])
        # 天乙贵人
        flag = False
        for items in tianyis[ming.me]:
            for item in items:
                if item in ming.zhis:
                    if not flag:
                        print("| 天乙贵人：", end=" ")
                        flag = True
                    print(item, end=" ")

        # 玉堂贵人
        flag = False
        for items in yutangs[ming.me]:
            for item in items:
                if item in ming.zhis:
                    if not flag:
                        print("| 玉堂贵人：", end=" ")
                        flag = True
                    print(item, end=" ")

        # 天罗
        if nayins[ming.zhus[0]][-1] == "火":
            if ming.zhis.day in "戌亥":
                print("| 天罗：{}".format(ming.zhis.day), end=" ")

        # 地网
        if nayins[ming.zhus[0]][-1] in "水土":
            if ming.zhis.day in "辰巳":
                print("| 地网：{}".format(ming.zhis.day), end=" ")

        # 学堂分析
        for seq, item in enumerate(self.statuses):
            if item == "长":
                print("学堂:", ming.zhis[seq], "\t", end=" ")
                if nayins[ming.zhus[seq]][-1] == ten_deities[ming.me]["本"]:
                    print("正学堂:", nayins[ming.zhus[seq]], "\t", end=" ")

        # xuetang = xuetangs[ten_deities[ming.me]['本']][1]
        # if xuetang in ming.zhis:
        # print("学堂:", xuetang, "\t\t", end=' ')
        # if xuetangs[ten_deities[ming.me]['本']] in zhus:
        # print("正学堂:", xuetangs[ten_deities[ming.me]['本']], "\t\t", end=' ')

        # 学堂分析

        for seq, item in enumerate(self.statuses):
            if item == "建":
                print("| 词馆:", ming.zhis[seq], end=" ")
                if nayins[ming.zhus[seq]][-1] == ten_deities[ming.me]["本"]:
                    print("- 正词馆:", nayins[ming.zhus[seq]], end=" ")

        ku = ten_deities[ming.me]["库"][0]
        if ku in ming.zhis:
            print("库：", ku, end=" ")

            for item in ming.zhus:
                if ku != ming.zhus[1]:
                    continue
                if nayins[item][-1] == ten_deities[ming.me]["克"]:
                    print("库中有财，其人必丰厚")
                if nayins[item][-1] == ten_deities[ming.me]["被克"]:
                    print(item, ten_deities[ming.me]["被克"])
                    print("绝处无依，其人必滞")

        print()

        # 天元分析
        for item in zhi5[ming.zhis[2]]:
            name = ten_deities[ming.me][item]
            print(self_zuo[name])
        print("-" * 120)

        # 出身分析
        cai = ten_deities[ming.me].inverse["财"]
        guan = ten_deities[ming.me].inverse["官"]
        jie = ten_deities[ming.me].inverse["劫"]
        births = tuple(ming.gans[:2])
        if cai in births and guan in births:
            birth = "不错"
        # elif cai in births or guan in births:
        # birth = '较好'
        else:
            birth = "一般"

        print("出身:", birth)

        self.guan_num = ming.shens.count("官")
        self.sha_num = ming.shens.count("杀")
        self.cai_num = ming.shens.count("财")
        self.piancai_num = ming.shens.count("才")
        self.jie_num = ming.shens.count("劫")
        self.bi_num = ming.shens.count("比")
        self.yin_num = ming.shens.count("印")

        gan_ = tuple(ming.gans)
        for item in Gan:
            if gan_.count(item) == 3:
                print("三字干：", item, "--", gan3[item])
                break

        gan_ = tuple(ming.gans)
        for item in Gan:
            if gan_.count(item) == 4:
                print("四字干：", item, "--", gan4[item])
                break

        zhi_ = tuple(ming.zhis)
        for item in Zhi:
            if zhi_.count(item) > 2:
                print("三字支：", item, "--", zhi3[item])
                break

        print("=" * 120)
        print("你属:", ming.me, "特点：--", gan_desc[ming.me], "\n")
        print("年份:", ming.zhis[0], "特点：--", zhi_desc[ming.zhis[0]], "\n")

        # 羊刃分析
        key = "帝" if Gan.index(ming.me) % 2 == 0 else "冠"

        if ten_deities[ming.me].inverse[key] in ming.zhis:
            print("\n羊刃:", ming.me, ten_deities[ming.me].inverse[key])
            if ten_deities[ming.me].inverse["冠"]:
                print("羊刃重重又见禄，富贵饶金玉。 官、印相助福相资。")
            else:
                print("劳累命！")

        # 将星分析
        me_zhi = ming.zhis[2]
        other_zhis = ming.zhis[:2] + ming.zhis[3:]
        flag = False
        tmp_list = []
        if me_zhi in ("申", "子", "辰"):
            if "子" in other_zhis:
                flag = True
                tmp_list.append((ming.me_zhi, "子"))
        elif me_zhi in ("丑", "巳", "酉"):
            if "酉" in other_zhis:
                flag = True
                tmp_list.append((ming.me_zhi, "酉"))
        elif me_zhi in ("寅", "午", "戌"):
            if "午" in other_zhis:
                flag = True
                tmp_list.append((ming.me_zhi, "午"))
        elif me_zhi in ("亥", "卯", "未"):
            if "卯" in other_zhis:
                flag = True
                tmp_list.append((ming.me_zhi, "卯"))

        if flag:
            print("\n\n将星: 常欲吉星相扶，贵煞加临乃为吉庆。")
            print("=========================")
            print(
                """理愚歌》云：将星若用亡神临，为国栋梁臣。言吉助之为贵，更夹贵库墓纯粹而
            不杂者，出将入相之格也，带华盖、正印而不夹库，两府之格也；只带库墓而带正印，员郎
            以上，既不带墓又不带正印，止有华盖，常调之禄也；带华印而正建驿马，名曰节印，主旌节
            之贵；若岁干库同库为两重福，主大贵。"""
            )
            print(tmp_list)

        # 华盖分析
        flag = False
        if me_zhi in ("申", "子", "辰"):
            if "辰" in other_zhis:
                flag = True
        elif me_zhi in ("丑", "巳", "酉"):
            if "丑" in other_zhis:
                flag = True
        elif me_zhi in ("寅", "午", "戌"):
            if "戌" in other_zhis:
                flag = True
        elif me_zhi in ("亥", "卯", "未"):
            if "未" in other_zhis:
                flag = True

        if flag:
            print("\n\n华盖: 多主孤寡，总贵亦不免孤独，作僧道艺术论。")
            print("=========================")
            print(
                """《理愚歌》云：华盖虽吉亦有妨，或为孽子或孤孀。填房入赘多阙口，炉钳顶笠拔缁黄。
            又云：华盖星辰兄弟寡，天上孤高之宿也；生来若在时与胎，便是过房庶出者。"""
            )

        # 咸池 桃花
        flag = False
        taohuas = []
        year_zhi = ming.zhis[0]
        if me_zhi in ("申", "子", "辰") or year_zhi in ("申", "子", "辰"):
            if "酉" in ming.zhis:
                flag = True
                taohuas.append("酉")
        elif me_zhi in ("丑", "巳", "酉") or year_zhi in ("丑", "巳", "酉"):
            if "午" in other_zhis:
                flag = True
                taohuas.append("午")
        elif me_zhi in ("寅", "午", "戌") or year_zhi in ("寅", "午", "戌"):
            if "卯" in other_zhis:
                flag = True
                taohuas.append("卯")
        elif me_zhi in ("亥", "卯", "未") or year_zhi in ("亥", "卯", "未"):
            if "子" in other_zhis:
                flag = True
                taohuas.append("子")

        if flag:
            print("\n\n咸池(桃花): 墙里桃花，煞在年月；墙外桃花，煞在日时；")
            print("=========================")
            print(
                """一名败神，一名桃花煞，其神之奸邪淫鄙，如生旺则美容仪，耽酒色，疏财好欢，
            破散家业，唯务贪淫；如死绝，落魄不检，言行狡诈，游荡赌博，忘恩失信，私滥奸淫，
            靡所不为；与元辰并，更临生旺者，多得匪人为妻；与贵人建禄并，多因油盐酒货得生，
            或因妇人暗昧之财起家，平生有水厄、痨瘵之疾，累遭遗失暗昧之灾。此人入命，有破无成，
            非为吉兆，妇人尤忌之。
            咸池非吉煞，日时与水命遇之尤凶。"""
            )
            print(taohuas, ming.zhis)

        # 禄分析
        flag = False
        for item in ming.zhus:
            if item in lu_types[ming.me]:
                if not flag:
                    print("\n\n禄分析:")
                    print("=========================")
                print(item, lu_types[ming.me][item])

        # 文星贵人
        if wenxing[ming.me] in ming.zhis:
            print("文星贵人: ", ming.me, wenxing[ming.me])

        # 天印贵人
        if tianyin[ming.me] in ming.zhis:
            print("天印贵人: 此号天印贵，荣达受皇封", ming.me, tianyin[ming.me])

        short = min(self.scores, key=self.scores.get)
        print("\n\n五行缺{}的建议参见 http://t.cn/E6zwOMq".format(short))

        print("======================================")
        if "杀" in ming.shens:
            if yinyang(ming.me) == "+":
                print("阳杀:话多,热情外向,异性缘好")
            else:
                print("阴杀:话少,性格柔和")
        if "印" in ming.shens and "才" in ming.shens and "官" in ming.shens:
            print("印,偏财,官:三奇 怕正财")
        if "才" in ming.shens and "杀" in ming.shens:
            print("男:因女致祸、因色致祸; 女:赔货")

        if "才" in ming.shens and "枭" in ming.shens:
            print("偏印因偏财而不懒！")

    # 十神：比肩分析
    def get_bijian(self):
        print()
        print("-" * 120)
        print("\n【1.比肩分析】")
        if "比" in ming.gan_shens:  # 天干比肩
            print(
                "比：同性相斥。讨厌自己。老是想之前有没有搞错。没有持久性，最多跟你三五年。 散财，月上比肩，做事没有定性，不看重钱，感情不持久。不怀疑人家，人心很好。善意好心惹麻烦。年上问题不大。"
            )

            if ming.gan_shens[0] == "比" and ming.gan_shens[1] == "比":
                print(
                    "比肩年月天干并现：不是老大，出身平常。女仪容端庄，有自己的思想；不重视钱财,话多不能守秘。30随以前是非小人不断。"
                )

            if ming.gan_shens[1] == "比" and "比" in ming.zhi_shen3[1]:
                print("月柱干支比肩：争夫感情丰富。30岁以前钱不够花。")

            if ming.gan_shens[0] == "比":
                print("年干比：上面有哥或姐，出身一般。")

            if ming.zhi_shens[2] == "比":
                print("基52女坐比透比:夫妻互恨 丙辰 辛卯 辛酉 甲午。")

            if ming.gan_shens.count("比") > 1:
                print(
                    """----基51:天干2比
                自我排斥，易后悔、举棋不定、匆促决定而有失；男倾向于群力，自己决策容易孤注一掷，小事谨慎，大事决定后不再重复考虑。
                女有自己的思想、容貌佳，注意细节，喜欢小孩重过丈夫。轻视老公。对丈夫多疑心，容易吃醋冲动。
                男不得女欢心.
                难以保守秘密，不适合多言；
                地支有根，一生小是非不断。没官杀制，无耐心。 END"""
                )

            # 比肩过多
            if ming.shens2.count("比") > 2 and "比" in ming.zhi_shens:
                # print(shens2, ming.zhi_shens2)
                print(
                    """----比肩过多基51：
                女的爱子女超过丈夫；轻易否定丈夫。 换一种说法：有理想、自信、贪财、不惧内。男的双妻。
                兄弟之间缺乏帮助。夫妻有时不太和谐。好友知交相处不会很久。
                即使成好格局，也是劳累命，事必躬亲。除非有官杀制服。感情烦心。
                基53：善意多言，引无畏之争；难以保守秘密，不适合多言；易犯无事忙的自我表现；不好意思拒绝他人;累积情绪而突然放弃。
                比肩过多，女：你有帮夫运，多协助他的事业，多提意见，偶尔有争执，问题也不大。女：感情啰嗦
                对人警惕性低，乐天知命;情感过程多有波折
                """
                )

                if (not "官" in ming.shens) and (not "杀" in ming.shens):
                    print("基51: 比肩多，四柱无正官七杀，性情急躁。")

                if "劫" in ming.gan_shens:
                    print("天干比劫并立，比肩地支专位，女命感情丰富，多遇争夫。基52")

                if ming.gan_shens[0] == "比":
                    print("年干为比，不是长子，父母缘较薄，晚婚。")

                if ming.gan_shens[3] == "比":
                    print(
                        "母法总则P21-6：时干为比，如日时地支冲，男的对妻子不利，女的为夫辛劳，九流艺术、宗教则关系不大。"
                    )

                if ming.gan_shens[1] == "比":
                    if ming.zhi_shens[1] == "食":
                        print("月柱比坐食，易得贵人相助。")
                    if ming.zhi_shens[1] == "伤":
                        print("月柱比坐伤，一生只有小财气，难富贵。")
                    if ming.zhi_shens[1] == "比":
                        print(
                            "月柱比坐比，单亲家庭，一婚不能到头。地支三合或三会比，天干2比也如此。"
                        )
                    if ming.zhi_shens[1] == "财":
                        print(
                            "月柱比坐财，不利妻，也主父母身体不佳。因亲友、人情等招财物的无谓损失。"
                        )
                    if ming.zhi_shens[1] == "杀":
                        print("月柱比坐杀，稳重。")

            for seq, gan_ in enumerate(ming.gan_shens):
                if gan_ != "比":
                    continue
                if ming.zhis[seq] in empties[self.zhus[2]]:
                    print(
                        "基51:比肩坐空亡，不利父亲与妻。年不利父，月不利父和妻，在时则没有关系。甲戌 丙寅 甲子 己巳\n\t基52女：夫妻缘分偏薄，在年只是不利父，在月30岁以前夫妻缘薄 E"
                    )
                if ming.zhi_shens[seq] == "比":
                    print(
                        "比坐比-平吉：与官杀对立，无主权。养子：克偏财，泄正印。吉：为朋友尽力；凶：受兄弟朋友拖累。父缘分薄，自我孤僻，男多迟婚"
                    )
                if ming.zhi_shens[seq] == "劫":
                    print(
                        "女比肩坐劫:夫妻互恨，基52丁丑 壬子 壬戌 壬寅。\n\t还有刑冲且为羊刃，女恐有不测之灾：比如车祸、开刀和意外等。基52丙午 庚子 丙戌 丙申"
                    )
                    print(
                        "比坐劫-大凶：为忌亲友受损，合作事业中途解散，与妻子不合。如年月3见比，父缘薄或已死别。"
                    )
                    if ten_deities[ming.gans[seq]][ming.zhis[seq]] == "绝" and seq < 2:
                        print(
                            "比肩坐绝，兄弟不多，或者很难谋面。戊己和壬癸的准确率偏低些。"
                        )
                if ming.zhi_shens[seq] == "财":
                    print("比肩坐财：因亲人、人情等原因引起无谓损失。")
                if ming.zhi_shens[seq] == "杀":
                    print("比肩坐杀:稳重。")
                if ming.zhi_shens[seq] == "枭":
                    print("比肩坐偏印：三五年发达，后面守成。")
                if ming.zhi_shens[seq] == "劫" and Gan.index(ming.me) % 2 == 0:
                    print(
                        "比肩坐阳刃：父亲先亡，基于在哪柱判断时间。基51：丙午 丙申 丙申 丁酉。E在年不利父，在其他有刀伤、车祸、意外灾害。\t基52女命年克父亲，月若30岁以前结婚不利婚姻"
                    )
                if ming.zhi_shens[seq] in ("劫", "比") and "劫" in ming.gan_shens:
                    print("天干比劫并立，比肩又坐比劫，女多遇争夫，个性强，不易协调。")
                if self.zhi_xing[seq]:
                    print(
                        "比肩坐刑(注意不是半刑)，幼年艰苦，白手自立长。 甲申 己巳 甲寅 庚午 基51"
                    )
                    if ming.zhi_shens[seq] == "劫":
                        print("比肩坐刑劫,兄弟不合、也可能与妻子分居。")
                if self.zhi_6chong[seq]:
                    print(
                        "比肩冲，手足不和，基于柱定时间 甲申 己巳 甲寅 庚午 基51。女命忌讳比劫和合官杀，多为任性引发困难之事。"
                    )
        # 日支比
        if ming.zhi_shens[2] == "比":
            print(
                "日支比：1-39对家务事有家长式领导；钱来得不容易且有时有小损财。e 自我，如有刑冲，不喜归家！"
            )
        # 时支比
        if ming.zhi_shens[3] == "比":
            print("时支比：子女为人公正倔强、行动力强，能得资产。")
        # 月柱比
        if "比" in (ming.gan_shens[1], ming.zhi_shens[1]):
            print("月柱比：三十岁以前难有成就。冒进、不稳定。女友不持久、大男子主义。")

        # 时干和时支都有比
        if "比" in (ming.gan_shens[3], ming.zhi_shens[3]):
            print("时柱比：与亲人意见不合。")

        # 十神比肩总数大于2
        if ming.shens.count("比") + ming.shens.count("劫") > 1:
            print("比劫大于2，男：感情阻碍、事业起伏不定。")

        # 日坐禄
        if self.me_lu == ming.zhis[2]:

            if ming.zhis.count(self.me_lu) > 1:
                if self.yin_lu in ming.zhis:
                    if "比" in ming.gan_shens or "劫" in ming.gan_shens:

                        print(
                            "双禄带比印（专旺）、孤克之命。比论孤，劫论凶。母法总则P20-3。比禄印劫不可合见四位"
                        )

            if self.zhi_6he[2] and "比" in ming.gan_shens:
                if self.yin_lu in ming.zhis:
                    print(
                        "透比，坐禄六合，有印专旺：官非、残疾。六合近似劫财，如地支会印，法死。 母法总则P20-4"
                    )

                print("透比，坐禄六合，如地支会印，法死。 母法总则P20-4")

            if (self.zhi_xing[3] and self.gan_he[3] and ming.gan_shens[3] == "财") or (
                self.zhi_xing[2]
                and self.gan_he[2]
                and self.zhi_xing[1]
                and self.gan_he[1]
                and ming.gan_shens[1] == "财"
            ):

                print(
                    "日禄与正财干合支刑：克妻子，即便是吉命，也无天伦之乐。 母法总则P22-21"
                )

        if ming.zhis.count(self.me_lu) > 2:
            print("禄有三，孤。 母法总则P23-36")

        if ming.zhis[3] == self.me_ku:
            if "财" in ming.gan_shens or "才" in ming.gan_shens:
                print(
                    "时支日库，透财：清高、艺术九流。 母法总则P59-5 己未 辛未 丁巳 庚戌 P61-8 丁未 壬寅 癸卯 丙辰"
                )

            if self.piancai_lu == ming.zhis[2]:
                print(
                    "时支日库，坐偏财：吉祥近贵，但亲属淡薄。 母法总则P59-6 辛未 辛卯 丁酉 庚戌"
                )

        # 时坐禄
        if self.me_lu == ming.zhis[3]:
            if "伤" in ming.gan_shens and "伤" in ming.zhi_shens2:
                print("时禄，伤官格，晚年吉。 母法总则P56-26 己未 丙寅 乙丑 己卯")
            if "杀" == ming.gan_shens[3]:
                print("杀坐时禄：为人反复不定。 母法总则P56-28 己未 丙寅 乙丑 己卯")

        # 自坐劫库
        if ming.zhis[2] == self.me_ku:
            if ming.gan_shens[3] == "杀" and "杀" in ming.zhi_shen3[3]:
                print(
                    "自坐劫库,时杀格，贵！母法总则P30-143 辛未 辛卯 壬辰 戊申 母法总则P55-14 P60-22"
                )

            if ming.gan_shens[3] == "官" and "官" in ming.zhi_shen3[3]:
                print(
                    "自坐劫库,正官格，孤贵！母法总则P56-24 辛未 辛卯 壬辰 戊申 母法总则P55-14"
                )

            if zhi_ku(ming.zhis[3], (self.cai, self.piancai)):
                print(
                    "自坐劫库,时财库，另有刃禄孤刑艺术，无者辛劳！母法总则P30-149 母法总则P56-17 56-18"
                )

            if ming.gan_shens[3] == "财" and "财" in ming.zhi_shen3[3]:
                print(
                    "自坐劫库，时正财格，双妻，丧妻。 母法总则P55-13 己酉 戊寅 壬辰 丁未 P61-6 乙酉 戊寅 壬辰 丁未"
                )

            if (self.yin, self.me_lu) in self.zhus:
                print("自坐劫库,即便吉，也会猝亡 母法总则P61-9 丁丑 甲辰 壬辰 辛亥")

    # 十神：劫财分析
    def get_jiecai(self):
        print("\n【2.劫财分析】")
        if "劫" in ming.gan_shens:
            print(
                "劫财扶助，无微不至。劫财多者谦虚之中带有傲气。凡事先理情，而后情理。先细节后全局。性刚强、精明干练、女命不适合干透支藏。"
            )
            print(
                "务实，不喜欢抽象性的空谈。不容易认错，比较倔。有理想，但是不够灵活。不怕闲言闲语干扰。不顾及别人面子。"
            )
            print(
                "合作事业有始无终。太重细节。做小领导还是可以的。有志向，自信。杀或食透干可解所有负面。女命忌讳比劫和合官杀，多为任性引发困难之事。"
            )

            if ming.gan_shens[0] == "劫" and ming.gan_shens[1] == "劫":
                print(
                    "劫年月天干并现：喜怒形于色，30岁以前大失败一次。过度自信，精明反被精明误。"
                )

            if ming.gan_shens[1] == "劫":
                if "劫" in ming.zhi_shen3[1]:
                    print(
                        "月柱干支劫：与父亲无缘，30岁以前任性，早婚防分手，自我精神压力极其重。"
                    )
                if ming.zhis[1] == self.cai_lu and ming.zhis.count(self.yin_lu) > 1:
                    print("月干劫：月支财禄，如地支2旺印，旺财不敌，官非、刑名意外。")

            if ming.shens2.count("劫") > 2:
                print("----劫财过多, 婚姻不好")
            if ming.zhi_shens[2] == "劫":
                print(
                    "日坐劫财，透天干。在年父早亡，在月夫妻关系不好。比如财产互相防范；鄙视对方；自己决定，哪怕对方不同意；老夫少妻；身世有差距；斤斤计较；敢爱敢恨的后遗症\n\t以上多针对女。男的一般有双妻。天干有杀或食可解。基54丁未 己酉 丙午 己丑"
                )

        if ming.zhus[2] in (("壬", "子"), ("丙", "午"), ("戊", "午")):
            print(
                "日主专位劫财，壬子和丙午，晚婚。不透天干，一般是眼光高、独立性强。对配偶不利，互相轻视；若刑冲，做事立场不明遭嫉妒，但不会有大灾。女性婚后通常还有自己的事业,能办事。"
            )
        if ("劫", "伤") in self.shen_zhus or (
            "伤",
            "劫",
        ) in self.shen_zhus:
            print(
                "同一柱中，劫财、阳刃伤官都有，外表华美，富屋穷人，婚姻不稳定，富而不久；年柱不利家长，月柱不利婚姻，时柱不利子女。伤官的狂妄。基55丙申 丁酉 甲子 丁卯"
            )

        if ming.gan_shens[0] == "劫":
            print(
                "年干劫财：家运不济。克父，如果坐劫财，通常少年失父；反之要看地支劫财根在哪一柱子。"
            )

        if "劫" in (ming.gan_shens[1], ming.zhi_shens[1]):
            print("月柱劫：容易孤注一掷，30岁以前难稳定。男早婚不利。")
        if "劫" in (ming.gan_shens[3], ming.zhi_shens[3]):
            print("时柱劫：只要不是去经济大权还好。")
        if ming.zhi_shens[2] == "劫":
            print(
                "日支劫：男的克妻，一说是家庭有纠纷，对外尚无重大损失。如再透月或时天干，有严重内忧外患。"
            )

        if (
            "劫" in ming.shens2
            and "比" in ming.zhi_shens
            and "印" in ming.shens2
            and not_yang(ming.me)
        ):
            print("阴干比劫印齐全，单身，可入道！")

        if ming.zhi_shens[0] == "劫" and is_yang(ming.me):
            print("年阳刃：得不到长辈福；不知足、施恩反怨。")
        if ming.zhi_shens[3] == "劫" and is_yang(ming.me):
            print("时阳刃：与妻子不和，晚无结果，四柱再有比刃，有疾病与外灾。")

        # 阳刃格
        if ming.zhi_shens[1] == "劫" and is_yang(ming.me):
            self.all_ges.append("刃")
            print("阳刃格：喜七杀或三四个官。基础90 甲戊庚逢冲多祸，壬丙逢冲还好。")
            if ming.me in ("庚", "壬", "戊"):
                print(
                    "阳刃'庚', '壬','午'忌讳正财运。庚逢辛酉凶，丁酉吉，庚辰和丁酉六合不凶。壬逢壬子凶，戊子吉；壬午和戊子换禄不凶。"
                )
            else:
                print(
                    "阳刃'甲', '丙',忌讳杀运，正财偏财财库运还好。甲：乙卯凶，辛卯吉；甲申与丁卯暗合吉。丙：丙午凶，壬午吉。丙子和壬午换禄不凶。"
                )

            if (
                ming.zhis.count(self.yin_lu) > 0 and ming.gan_shens[1] == "劫"
            ):  # 母法总则P20-1
                print(
                    "阳刃格月干为劫：如果印禄位有2个，过旺，凶灾。不透劫财，有一印禄,食伤泄，仍然可以吉。 母法总则P20-1"
                )

            if ming.gan_shens[3] == "枭" and "枭" in ming.zhi_shen3[3]:

                print(
                    "阳刃格:时柱成偏印格，贫、夭、带疾。 母法总则P28-107 癸未 辛酉 庚寅 戊寅"
                )

        if ming.zhi_shens.count("劫") > 1 and Gan.index(ming.me) % 2 == 0:
            if ming.zhis.day == self.yin_lu:
                print(
                    "双阳刃，自坐印专位：刑妻、妨子。凶终、官非、意外灾害。母法总则P21-13"
                )

        if ming.zhi_shens[1:].count("劫") > 0 and Gan.index(ming.me) % 2 == 0:
            if ming.zhis.day == self.yin_lu and (
                "劫" in ming.gan_shens or "比" in ming.gan_shens
            ):
                print(
                    "阳刃，自坐印专位，透比或劫：刑妻。母法总则P36-8 己酉 丁卯 甲子 乙亥"
                )

        if ming.zhis[2] in (self.me_lu, self.me_di) and ming.zhis[3] in (
            self.me_lu,
            self.me_di,
        ):
            print(
                "日时禄刃全，如没有官杀制，刑伤父母，妨碍妻子。母法总则P30-151 丁酉 癸卯 壬子 辛亥 母法总则P31-153 "
            )

        # print(ming.gan_shens)
        for seq, gan_ in enumerate(ming.gan_shens):
            if gan_ != "劫":
                continue
            if ming.zhis[seq] in (self.cai_lu, self.piancai_lu):
                print(
                    "劫财坐财禄，如逢冲，大凶。先冲后合和稍缓解！母法总则P21-7 书上实例不准！"
                )

                if ming.zhi_shens[seq] == "财" and self.zhi_6he[seq]:
                    print(
                        "劫财坐六合财支：久疾暗病！母法总则P28-113 乙未 丙戌 辛亥 庚寅！"
                    )

        if (
            ming.gan_shens[1] == "劫"
            and ming.zhis[1] in (self.cai_lu, self.piancai_lu)
            and ming.zhis.count(self.yin_lu) > 1
            and "劫" in ming.gan_shens
        ):
            print(
                "月干劫坐财禄，有2印禄，劫透，财旺也败：官非、刑名、意外灾害！  母法总则P20-2"
            )

        # 自坐阳刃
        if "劫" in ming.zhi_shen3[2] and is_yang() and ming.zhis[2] in zhengs:
            if ming.zhis[3] in (self.cai_lu, self.piancai_lu):
                print(
                    "坐阳刃,时支财禄，吉祥但是妻子性格不受管制！母法总则P30-137 丁未 庚戌 壬子 乙巳"
                )
            if zhi_ku(ming.zhis[3], (self.cai, self.piancai)):
                print(
                    "坐阳刃,时支财库，名利时进时退！母法总则P30-148 丙寅 壬寅 壬子 庚戌"
                )

            if ming.gan_shens[3] == "杀" and "杀" in ming.zhi_shen3[3]:
                print(
                    "坐阳刃,时杀格，贵人提携而富贵！母法总则P30-143 甲戌 丙寅 壬子 戊申"
                )

    # 十神：偏印分析
    def get_pianyin(self):
        print("\n【3.偏印分析】")
        if "枭" in ming.gan_shens:
            print(
                "----偏印在天干如成格：偏印在前，偏财(财次之)在后，有天月德就是佳命(偏印格在日时，不在月透天干也麻烦)。忌讳倒食，但是坐绝没有这能力。"
            )
            print(
                "经典认为：偏印不能扶身，要身旺；偏印见官杀未必是福；喜伤官，喜财；忌日主无根；   女顾兄弟姐妹；男六亲似冰"
            )
            print("偏印格干支有冲、合、刑，地支是偏印的绝位也不佳。")

            # print(ming.zhi_shen3)
            if ming.gan_shens[1] == "枭" and "枭" in ming.zhi_shen3[1]:
                print("枭月重叠：福薄慧多，青年孤独，有文艺宗教倾向。")

            if ming.zhi_shens2.count("枭") > 1:
                print("偏印根透2柱，孤独有色情之患难。做事有始无终，女声誉不佳！pd40")

            if ming.zhi_shens2.count("枭"):
                print(
                    "偏印成格基础89生财、配印；最喜偏财同时成格，偏印在前，偏财在后。最忌讳日时坐实比劫刃。"
                )
                self.all_ges.append("枭")

            if self.shens2.count("枭") > 2:
                print(
                    "偏印过多，性格孤僻，表达太含蓄，要别人猜，说话有时带刺。偏悲观。有偏财和天月德贵人可以改善。有艺术天赋。做事大多有始无终。如四柱全阴，女性声誉不佳。"
                )
                print(
                    "对兄弟姐妹不错。男的因才干受子女尊敬。女的偏印多，子女不多。第1克伤食，第2艺术性。"
                )
                if "伤" in ming.gan_shens:
                    print(
                        "女命偏印多，又与伤官同透，夫离子散。有偏财和天月德贵人可以改善。"
                    )

            if ming.gan_shens.count("枭") > 1:
                print(
                    "天干两个偏印：迟婚，独身等，婚姻不好。三偏印，家族人口少，亲属不多建。基56甲午 甲戌 丙午 丙申"
                )

            if self.shen_zhus[0] == ("枭", "枭"):
                print(
                    "偏印在年，干支俱透，不利于长辈。偏母当令，正母无权，可能是领养，庶出、同父异母等。 基56乙卯 甲申 丁丑 丁未"
                )

            if ming.zhi_shen3[1] == ["枭"]:
                print("月专位偏印：有手艺。坐衰其貌不扬。")

        for seq, zhi_ in enumerate(ming.zhi_shens):
            if zhi_ != "枭" and ming.gan_shens[seq] != "枭":
                continue

            if ten_deities[ming.gans[seq]][ming.zhis[seq]] == "绝":
                print(
                    "偏印坐绝，或者天干坐偏印为绝，难以得志。费力不讨好。基56辛酉 辛卯 丁巳 甲辰  丁卯 丁未 己丑 丁卯"
                )

            if ming.gan_shens[seq] == "枭":
                if "枭" in ming.zhi_shen3[seq]:
                    print("干支都与偏印，克夫福薄！")

                if "比" in ming.zhi_shen3[seq]:
                    print("偏印坐比：劳心劳力，常遇阴折 pd41")

                if ming.zhi_shens[seq] == "伤":
                    print("偏印坐伤官：克夫丧子 pd41")

        if ming.zhi_shens[3] == "枭" and ming.gan_shens[0] == "枭":
            print("偏印透年干-时支，一直受家里影响。")

        if "枭" in (ming.gan_shens[0], ming.zhi_shens[0]):
            print("偏印在年：少有富贵家庭；有宗教素养，不喜享乐，第六感强。")
        if "枭" in (ming.gan_shens[1], ming.zhi_shens[1]):
            print("偏印在月：有慧少福，能舍己为人。")
            if ming.zhi_shens[1] == "枭" and ming.zhis[1] in "子午卯酉":
                print(
                    "偏印专位在月支：比较适合音乐，艺术，宗教等。子午卯酉。22-30之间职业定型。基56：壬午 癸卯 丁丑 丁未"
                )
                if ming.gan_shens[1] == "枭":
                    print(
                        "干支偏印月柱，专位入格，有慧福浅，不争名利。基57:戊子 辛酉 癸未 丁巳"
                    )
        if "枭" in (ming.gan_shens[3], ming.zhi_shens[3]):
            print("偏印在时：女与后代分居；男50以前奠定基础，晚年享清福。")
        if ming.zhi_shens[2] == "枭" or ming.zhis.day == self.xiao_lu:
            print("偏印在日支：家庭生活沉闷")
            if self.zhi_6chong[2] or self.zhi_xing[2]:
                print(
                    "偏印在日支(专位？),有冲刑：孤独。基57：甲午 癸酉 丁卯 丁未 母法总则P55-5： 辛丑 辛卯 癸酉 戊午 P77-13"
                )
            if ming.zhus[2] in (("丁", "卯"), ("癸", "酉")):
                print(
                    "日专坐偏印：丁卯和癸酉。婚姻不顺。又刑冲，因性格而起争端而意外伤害。 基56"
                )
            if ming.zhis[3] == self.me_jue:
                print(
                    "日坐偏印，日支绝：无亲人依靠，贫乏。 母法总则P55-5：丙辰 丙申 丁卯 壬子。pd41 专位偏印：男女姻缘都不佳。"
                )

            if "枭" in ming.gan_shens and is_yang() and ming.zhis.time == self.me_di:

                print(
                    "日坐偏印成格，时支阳刃：不利妻子，自身有疾病。 母法总则P55-6：甲子 甲戌 丙寅 甲午"
                )
            if ming.gan_shens[3] == ming.zhi_shens[3] == "劫":
                print(
                    "日坐偏印，时干支劫：因自己性格而引灾。 母法总则P57-34：甲子 甲戌 丙寅 甲午"
                )

            if ming.zhis.count(ming.me_di) > 1 and is_yang():
                print(
                    "日坐偏印，地支双阳刃：性格有极端倾向。 母法总则P57-35：甲申 庚午 丙寅 甲午"
                )

        if ming.zhis.time == self.xiao_lu:
            if ming.zhi_shens[3] == "枭" and "枭" in ming.gan_shens:
                if "财" in ming.shens2 or "才" in ming.shens2:
                    print(
                        "时支偏印成格有财：因机智引凶。 母法总则P60-18：甲申 乙亥 丁亥 癸卯"
                    )
                else:
                    print(
                        "时支偏印成格无财：顽固引凶。 母法总则P60-17：甲子 乙亥 丁亥 癸卯"
                    )

    # 十神：正印分析
    def get_zhengyin(self):
        print("\n【4.正印分析】")
        if "印" in ming.gan_shens:
            if "印" in ming.zhi_shens2:
                print(
                    "基础82，成格喜官杀、身弱、忌财克印。合印留财，见利忘义.透财官杀通关或印生比劫；合冲印若无他格或调候破格。日主强凶，禄刃一支可以食伤泄。"
                )
                self.all_ges.append("印")

            if ming.gan_shens[1] == "印" and "印" in ming.zhi_shen3[1]:
                print("印月重叠：女迟婚，月阳刃者离寡，能独立谋生，有修养的才女。")

            if ming.gan_shens[0] == "印":
                print("年干印为喜：出身于富贵之家。")

            if ming.shens2.count("印") > 2:
                print(
                    "正印多的：聪明有谋略，比较含蓄，不害人，识时务。正印不怕日主死绝，反而怕太强。日主强，正印多，孤寂，不善理财。 pd41男的克妻，子嗣少。女的克母。"
                )
            for seq, gan_ in enumerate(ming.gan_shens):
                if gan_ != "印":
                    continue
                if ten_deities[ming.gans[seq]][ming.zhis[seq]] in ("绝", "死"):
                    if seq < 3:
                        print("正印坐死绝，或天干正印地支有冲刑，不利母亲。时柱不算。")
                if ming.zhi_shens[seq] == "财":
                    print(
                        "男正印坐正财，夫妻不好。月柱正印坐正财专位，必离婚。在时柱，50多岁才有正常婚姻。(男) 基59 乙酉 己卯 庚子 丁亥  庚申 庚辰 庚午 己卯"
                    )
                if ming.zhi_shens[seq] == "印":
                    print(
                        "正印坐正印，专位，过于自信。基59：戊辰 乙卯 丙申 丙申。务实，拿得起放得下。女的话大多晚婚。母长寿；女子息迟，头胎恐流产。女四柱没有官杀，没有良缘。男的搞艺术比较好，经商则孤僻，不聚财。"
                    )

                if ming.zhi_shens[seq] == "枭" and len(zhi5[ming.zhis[seq]]) == 1:
                    print(
                        "正印坐偏印专位：基59壬寅 壬子 乙酉 甲申。有多种职业;家庭不吉：亲人有疾或者特别嗜好。子息迟;财务双关。明一套，暗一套。女的双重性格。"
                    )

                if ming.zhi_shens[seq] == "伤":
                    print(
                        "正印坐伤官：适合清高的职业。不适合追逐名利，女的婚姻不好。基59辛未 丁酉 戊子 丙辰"
                    )

                if ming.zhi_shens[seq] == "劫" and me in ("甲", "庚", "壬"):
                    print(
                        "正印坐阳刃，身心多伤，心疲力竭，偶有因公殉职。主要指月柱。工作看得比较重要。"
                    )

            if (
                "杀" in ming.gan_shens
                and "劫" in ming.zhi_shens
                and me in ("甲", "庚", "壬")
            ):
                print(
                    "正印、七杀、阳刃全：基60癸巳 庚申 甲寅 丁卯：女命宗教人，否则独身，清高，身体恐有隐疾，性格狭隘缺耐心。男小疾多，纸上谈兵，婚姻不佳，恐非婚生子女，心思细腻对人要求也高。"
                )

            if "官" in ming.gan_shens or "杀" in ming.gan_shens:
                print("身弱官杀和印都透天干，格局佳。")
            else:
                print("单独正印主秀气、艺术、文才。性格保守")
            if (
                "官" in ming.gan_shens
                or "杀" in ming.gan_shens
                or "比" in ming.gan_shens
            ):
                print(
                    "正印多者，有比肩在天干，不怕财。有官杀在天干也不怕。财不强也没关系。"
                )
            else:
                print("正印怕财。")
            if "财" in ming.gan_shens:
                print(
                    "印和财都透天干，都有根，最好先财后印，一生吉祥。先印后财，能力不错，但多为他人奔波。(男)"
                )

        if ming.zhi_shens[1] == "印":
            print("月支印：女命觉得丈夫不如自己，分居是常态，自己有能力。")
            if ming.gan_shens[1] == "印":
                print(
                    "月干支印：男权重于名，女命很自信，与夫平权。pd41:聪明有权谋，自我"
                )
                if "比" in ming.gan_shens:
                    print("月干支印格，透比，有冲亡。")

        if ming.zhi_shens[2] == "印":
            if ming.gan_shens[3] == "才" and "才" in ming.zhi_shen3[3]:
                print(
                    "坐印，时偏财格：他乡发迹，改弦易宗，妻贤子孝。 母法总则：P55-1 丁丑 丁未 甲子 戊辰"
                )

            if ming.gan_shens[3] == "财" and (
                "财" in ming.zhi_shen3[3] or ming.zhis[3] in (cai_di, cai_lu)
            ):
                print(
                    "坐印，时财正格：晚年发达，妻贤子不孝。 母法总则：P55-2 乙酉 丙申 甲子 己巳"
                )

        if ming.zhi_shens[3] == "印" and ming.zhis[3] in zhengs:
            print("时支专位正印。男忙碌到老。女的子女各居一方。亲情淡薄。")

        if ming.gan_shens[3] == "印" and "印" in ming.zhi_shen3[3]:
            print("时柱正印格，不论男女，老年辛苦。女的到死都要控制家产。子女无缘。")

        if ming.gan_shens.count("印") + ming.gan_shens.count("枭") > 1:
            print(
                "印枭在年干月干，性格迂腐，故作清高，女子息迟，婚姻有阻碍。印枭在时干，不利母子，性格不和谐。"
            )

        if ming.zhis[1] in (self.yin_lu, self.xiao_lu):
            print("印或枭在月支，有压制丈夫的心态。")

        if ming.zhis[3] in (self.yin_lu, self.xiao_lu):
            print("印或枭在时支，夫灾子寡。")

        # 坐印库
        if zhi_ku(ming.zhis[2], (self.yin, self.xiao)):
            if ming.shens2.count("印") > 2:
                print("母法总则P21-5: 日坐印库，又成印格，意外伤残，凶终。过旺。")
            if ming.zhi_shens[3] == "劫":
                print("自坐印库，时阳刃。带比禄印者贫，不带吉。 母法总则P21-14")

        if ming.zhis.count("印") > 1:
            if (
                ming.gan_shens[1] == "印"
                and ming.zhi_shens[1] == "印"
                and "比" in ming.gan_shens
            ):
                print("月干支印，印旺，透比，旺而不久，冲亡。母法总则P21-8")

        if ming.zhis[1] == self.yin_lu:
            if ("财" in ming.gan_shens and "财" in ming.zhi_shens) or (
                "才" in ming.gan_shens and "才" in ming.zhi_shens
            ):
                print("母法总则P22-18 自坐正印专旺，成财格，移他乡易宗，妻贤子孝。")

    # 十神：食神分析
    def get_shishen(self):
        print("\n【5.食神分析】")

        if "食" in ming.gan_shens:
            if "食" in ming.zhi_shens2:
                print(
                    "食神成格的情况下，寿命比较好。食神和偏财格比较长寿。食神厚道，为人不慷慨。食神有口福。成格基础84，喜财忌偏印(只能偏财制)。"
                )
                print("食神无财一生衣食无忧，无大福。有印用比劫通关或财制。")
                self.all_ges.append("食")

            if (ming.gan_shens[0] == "食" and ming.gan_shens[1] == "食") or (
                ming.gan_shens[1] == "食" and "食" in ming.zhi_shen3[1]
            ):
                print(
                    "食月重叠：生长安定环境，性格仁慈、无冲刑长寿。女早年得子。无冲刑偏印者是佳命。"
                )

            if "枭" in ming.gan_shens:
                print(
                    "男的食神碰到偏印，身体不好。怕偏印，正印要好一点。四柱透出偏财可解。"
                )
                if "劫" in ming.gan_shens:
                    print("食神不宜与劫财、偏印齐出干。体弱多病。基69")
                if "杀" in ming.gan_shens:
                    print("食神不宜与杀、偏印齐成格。体弱多病。")
            if "食" in ming.zhi_shens:
                print("食神天透地藏，女命阳日主适合社会性职业，阴日主适合上班族。")
            if (not "财" in ming.gan_shens) and (not "才" in ming.gan_shens):
                print("食神多，要食伤生财才好，无财难发。")
            if "伤" in ming.gan_shens:
                print("食伤混杂：食神和伤官同透天干：志大才疏。")
            if "杀" in ming.gan_shens:
                print("食神制杀，杀不是主格，施舍后后悔。")

            for seq, gan_ in enumerate(ming.gan_shens):
                if gan_ != "食":
                    continue
                if ming.zhi_shens[seq] == "劫":
                    print("食神坐阳刃，辛劳。基69 戊申 戊午 丙子 丙申")

        if ming.shens2.count("食") > 2:
            print(
                "食神四个及以上的为多，做伤官处理。食神多，要食伤生财才好，无财难发。"
            )
            if "劫" in ming.gan_shens or "比" in ming.gan_shens:
                print("食神带比劫，好施舍，乐于做社会服务。")

        if ("杀", "食") in self.shen_zhus or ("食", "杀") in self.shen_zhus:
            print(
                "食神与七杀同一柱，易怒。食神制杀，最好食在前。有一定概率。基69辛未 丁酉 乙未 戊寅"
            )

        if ("枭", "食") in self.shen_zhus or ("食", "枭") in self.shen_zhus:
            print(
                "女命最怕食神偏印同一柱。不利后代，时柱尤其重要。基69庚午 己卯 丁未 丁未"
            )

        if "食" in ming.zhi_shen3[2] and ming.zhis[2] in zhengs:
            print("日支食神专位容易发胖，有福。只有2日：癸卯，己酉。男命有有助之妻。")
        if ming.zhi_shens[2] == "食" and ming.zhi_shens[2] == "杀":
            print("自坐食神，时支杀专，二者不出天干，多成败，最后失局。")

        if ming.zhi_shens[2] == "食":
            print(
                "自坐食神，相敬相助，即使透枭也无事，不过心思不定，做事毅力不足，也可能假客气。专位容易发胖，有福。"
            )

        if ming.zhis[2] == self.shi_lu:
            if ming.zhis[3] == self.sha_lu and (self.sha not in ming.gan_shens):
                print(
                    "自坐食，时支专杀不透干：多成败，终局失制。母法总则P56-22 丙子 庚寅 己酉 丁卯"
                )

        if "食" in ming.zhi_shen3[3] and "枭" in ming.zhi_shen3[3] + ming.gan_shens[3]:
            print("时支食神逢偏印：体弱，慢性病，女的一婚不到头。")

        if ming.zhis[2] in kus and ming.zhi_shen3[2][2] in ("食", "伤"):
            print("自坐食伤库：总觉得钱不够。")

        if "食" in (ming.gan_shens[0], ming.zhi_shens[0]):
            print("年柱食：可三代同堂。")

        if zhi_ku(ming.zhis[3], (self.shi, self.shang)) and (
            "食" in ming.zhi_shen3[1] or "伤" in ming.zhi_shen3[1]
        ):
            print("时食库，月食当令，孤克。")

        # 自坐食伤库
        if zhi_ku(ming.zhis[2], (self.shi, self.shang)):
            if ming.zhis[3] == self.guan_lu:
                print(
                    "坐食伤库：时支官，发达时接近寿终。 母法总则P60-13 乙丑 丙戌 庚辰 壬午"
                )

        # 自坐食伤库
        if zhi_ku(ming.zhis[3], (self.shi, self.shang)):

            if ming.zhis[1] in (self.shi_di, self.shi_lu):
                print(
                    "坐食伤库：月支食伤当令，吉命而孤克。 母法总则P60-14 甲戌 丙子 辛卯 壬辰"
                )

    # 十神：伤官分析
    def get_shangguan(self):
        print("\n【6.伤官分析】")
        if "伤" in ming.gan_shens:
            print("伤官有才华，但是清高。要生财，或者印制。")
            if "伤" in ming.zhi_shens2:
                print(
                    "食神重成伤官，不适合伤官配印。金水、土金、木火命造更高。火土要调候，容易火炎土燥。伤官和七杀的局不适合月支为库。"
                )
                self.all_ges.append("伤")
                print(
                    "伤官成格基础87生财、配印。不考虑调候逆用比顺用好，调候更重要。生正财用偏印，生偏财用正印。\n伤官配印，如果透杀，透财不佳。伤官七杀同时成格，不透财为上好命局。"
                )

            if (ming.gan_shens[0] == "伤" and ming.gan_shens[1] == "伤") or (
                ming.gan_shens[1] == "伤" and "伤" in ming.zhi_shen3[1]
            ):
                print(
                    "父母兄弟均无缘。孤苦，性刚毅好掌权。30岁以前有严重感情苦重，适合老夫少妻，继室先同居后结婚。"
                )

            if "印" in ming.gan_shens and ("财" not in ming.gan_shens):
                print("伤官配印，无财，有手艺，但是不善于理财。有一定个性")
            if (
                ming.gan_shens[0] == "伤"
                and ming.gan_shens[1] == "伤"
                and (not "伤" in ming.zhi_shens2)
            ):
                print("年月天干都浮现伤官，亲属少。")

            if (
                ming.zhi_shens[1] == "伤"
                and len(zhi5[ming.zhis[1]]) == 1
                and ming.gan_shens[1] == "伤"
            ):
                print("月柱：伤官坐专位伤官，夫缘不定。假夫妻。比如老板和小蜜。")

            for seq, gan_ in enumerate(ming.gan_shens):
                if gan_ != "伤":
                    continue
                if ming.zhi_shens[seq] == "劫":
                    print(
                        "伤官地支坐阳刃，力不从心 基70己酉 丁卯 甲午 辛未。背禄逐马，克官劫财。影响15年。伤官坐劫财：只适合纯粹之精明商人或严谨掌握财之人。"
                    )

        if ming.shens2.count("伤") > 2:
            if ming.is_women:
                print("女命伤官多，即使不入伤官格，也缘分浅，多有苦情。")
            if ming.gan_shens.count("伤") > 2:
                print(
                    "天干2伤官：性骄，六亲不靠。婚前诉说家人，婚后埋怨老公。30岁以前为婚姻危机期。"
                )

        if ming.zhi_shens[2] == "伤" and len(zhi5[ming.zhis[2]]) == 1:
            print("女命婚姻宫伤官：强势克夫。男的对妻子不利。只有庚子日。")

        if ming.gan_shens[3] == "伤" and self.me_lu == ming.zhis[3]:
            print(
                "伤官坐时禄：六亲不靠，无冲刑晚年发，有冲刑不发。 母法P27-96己未 壬申 己亥 庚午, 可以参三命。"
            )

        if ming.zhis[3] in (self.shang_lu, self.shang_di) and ming.zhis[1] in (
            self.shang_lu,
            self.shang_di,
        ):
            print(
                "月支时支食伤当令：日主无根，泄尽日主，凶。 母法P28-104 甲午 乙亥 庚戌 丙子  母法P60-104"
            )

        # print("shang", shang, ten_deities[shang].inverse['建'], ming.zhi_shens)
        if ten_deities[self.shang].inverse["建"] in ming.zhis and ming.is_women:
            print("女命地支伤官禄：婚姻受不得穷。")

    # 十神：偏财分析
    def get_piancai(self):
        print("\n【7.偏财分析】")
        # 偏财分析
        if "才" in ming.gan_shens:
            print(
                "偏财明现天干，不论是否有根:财富外人可见;实际财力不及外观一半。没钱别人都不相信;协助他人常超过自己的能力"
            )
            print(
                "偏财出天干，又与天月德贵人同一天干者。在年月有声明远扬的父亲，月时有聪慧的红颜知己。喜奉承。"
            )
            print(
                "偏财透天干，四柱没有刑冲，长寿。女子为孝顺女，主要针对年月。时柱表示中年以后有自己的事业，善于理财。"
            )
            if "才" in ming.zhi_shens2:
                print(
                    "财格基础80:比劫用食伤通关或官杀制；身弱有比劫仍然用食伤通关。如果时柱坐实比劫，晚年破产。"
                )
                self.all_ges.append("才")
            print("偏财透天干，讲究原则，不拘小节。喜奉承，善于享受。财格基础80")

            if (
                "比" in ming.gan_shens
                or "劫" in ming.gan_shens
                and ming.gan_shens[3] == "才"
            ):
                print(
                    "年月比劫，时干透出偏财。祖业凋零，再白手起家。有刑冲为千金散尽还复来"
                )
            if "杀" in ming.gan_shens and "杀" in ming.zhi_shens:
                print(
                    "偏财和七杀并位，地支又有根，父子外合心不合。因为偏财生杀攻身。偏财七杀在日时，则为有难伺候的女朋友。 基62壬午 甲辰 戊寅 癸亥"
                )

            if ming.zhi_shens[0] == "才":
                print("偏财根透年柱，家世良好，且能承受祖业。")

            for seq, gan_ in enumerate(ming.gan_shens):
                if gan_ != "才":
                    pass
                if "劫" in ming.zhi_shen3[seq] and ming.zhis[seq] in zhengs:
                    print(
                        "偏财坐阳刃劫财,可做父缘薄，也可幼年家贫。也可以父先亡，要参考第一大运。偏财坐专位阳刃劫财,父亲去他乡.基61壬午 壬寅 戊子 丁巳"
                    )
                if get_empty(ming.zhus[2], ming.zhis[seq]) == "空":
                    print("偏财坐空亡，财官难求。")

        if ming.shens2.count("才") > 2:
            print(
                "偏财多的人慷慨，得失看淡。花钱一般不会后悔。偏乐观，甚至是浮夸。生活习惯颠倒。适应能力强。有团队精神。得女性欢心。小事很少失信。"
            )
            print(
                "乐善好施，有团队精神，女命偏财，听父亲的话。时柱偏财女，善于理财，中年以后有事业。"
            )
        if (ming.zhi_shens[2] == "才" and len(zhi5[ming.zhis[2]]) == 1) or (
            ming.zhi_shens[3] == "才" and len(zhi5[ming.zhis[3]]) == 1
        ):
            print(
                "日时地支坐专位偏财。不见刑冲，时干不是比劫，大运也没有比劫刑冲，晚年发达。"
            )

    # 十神：正财分析
    def get_zhengcai(self):
        print("\n【8.正财分析】")
        if (
            ming.gan_shens[0] in ("财", "才") and ming.gan_shens[1] in ("财", "才")
        ) or (
            ming.gan_shens[1] in ("财", "才")
            and ("财" in ming.zhi_shen3[1] or "才" in ming.zhi_shen3[1])
        ):
            print(
                "财或偏财月重叠：女职业妇女，有理财办事能力。因自己理财能力而影响婚姻。一财得所，红颜失配。男的双妻。"
            )

        if "财" in ming.gan_shens:
            if "财" in ming.zhi_shens2:
                all_ges.append("财")

            if is_yang():
                print("男日主合财星，夫妻恩爱。如果争合或天干有劫财，双妻。")
            if "财" in ming.zhi_shens:
                print("财格基础80:比劫用食伤通关或官杀制；身弱有比劫仍然用食伤通关。")

            if "官" in ming.gan_shens:
                print("正官正财并行透出，(身强)出身书香门第。")
            if "官" in ming.gan_shens or "杀" in ming.gan_shens:
                print("官或杀与财并行透出，女压夫，财生官杀，老公压力大。")
            if ming.gan_shens[0] == "财":
                print("年干正财若为喜，富裕家庭，但不利母亲。")
            if "财" in ming.zhi_shens:
                if "官" in ming.gan_shens or "杀" in ming.gan_shens:
                    print("男财旺透官杀，女厌夫。")
            if ming.gan_shens.count("财") > 1:
                print(
                    "天干两正财，财源多，大多做好几种生意，好赶潮流，人云亦云。有时会做自己外行的生意。"
                )
                if "财" not in ming.zhi_shens2:
                    print("正财多而无根虚而不踏实。重财不富。")

        for seq, gan_ in enumerate(ming.gan_shens):
            if gan_ != "财" and ming.zhis[seq] != "财":
                continue
            if ming.zhis[seq] in day_shens["驿马"][ming.zhis.day] and seq != 2:
                print("女柱有财+驿马，动力持家。")
            if ming.zhis[seq] in day_shens["桃花"][ming.zhis.day] and seq != 2:
                print("女柱有财+桃花，不吉利。")
            if ming.zhis[seq] in empties[zhus[2]]:
                print("财坐空亡，不持久。")
            if ten_deities[ming.gans[seq]][ming.zhis[seq]] in ("绝", "墓"):
                print("男财坐绝或墓，不利婚姻。")

        if ming.shens2.count("财") > 2:
            print("正财多者，为人端正，有信用，简朴稳重。")
            if "财" in ming.zhi_shens2 and (ming.me not in ming.zhi_shens2):
                print("正财多而有根，日主不在生旺库，身弱惧内。")

        if ming.zhi_shens[1] == "财" and ming.is_women:
            print("女命月支正财，有务实的婚姻观。")

        if ming.zhi_shens[1] == "财":
            print(
                "月令正财，无冲刑，有贤内助，但是母亲与妻子不和。生活简朴，多为理财人士。"
            )
        if ming.zhi_shens[3] == "财" and len(zhi5[ming.zhis[3]]) == 1:
            print("时支正财，一般两个儿子。")
        if ming.zhus[2] in (("戊", "子"),) or ming.zhus[3] in (("戊", "子"),):
            print(
                "日支专位正财，得勤俭老婆。即戊子。日时专位支正财，又透正官，中年以后发达，独立富贵。"
            )

        if ming.zhus[2] in (
            ("壬", "午"),
            ("癸", "巳"),
        ):
            print("坐财官印，只要四柱没有刑冲，大吉！")

        if ming.zhus[2] in (
            ("甲", "戌"),
            ("乙", "亥"),
        ):
            print("女('甲','戌'),('乙','亥'） 晚婚 -- 不准！")

        if "财" == ming.gan_shens[3] or "财" == ming.zhi_shens[3]:

            print(
                "未必准确：时柱有正财，口快心直，不喜拖泥带水，刑冲则浮躁。阳刃也不佳.反之有美妻佳子"
            )
        if (not "财" in ming.shens2) and (not "才" in ming.shens2):
            print("四柱无财，即便逢财运，也是虚名虚利. 男的晚婚")

        # print("shang", shang, ten_deities[shang].inverse['建'], ming.zhi_shens)
        # if ten_deities[shang].inverse['建'] in ming.zhis:
        # print("女命一财得所，红颜失配。")

        if ming.zhis.day in (self.cai_lu, self.cai_di):
            if (ming.zhi_shens[1] == "劫" or ming.zhi_shens[3] == "劫") and Gan.index(
                ming.me
            ) % 2 == 0:
                print(
                    "自坐财禄，月支或时支为阳刃，凶。无冲是非多，冲刑主病灾。 母法总则P22-15  母法总则P36-4 丙寅 戊戌 甲午 丁卯 P56-32 己未 丙寅 丙申 甲午"
                )
            if (
                ("劫" in ming.zhi_shens)
                and Gan.index(ming.me) % 2 == 0
                and "劫" in ming.gan_shens
            ):
                print(
                    "自坐财禄，透劫财，有阳刃，刑妻无结局。 母法总则P36-7 戊子 乙卯 甲午 乙亥"
                )
            if ming.me in ("甲", "乙") and ("戊" in ming.gans or "己" in ming.gans):
                print(
                    "火土代用财，如果透财，多成多败，早年灰心。 母法总则P22-19 辛未 癸巳 甲午 戊辰"
                )

            if ming.gan_shens[3] == "枭":
                print("财禄时干偏印：主亲属孤独 母法总则P31-158 丁丑 丙午 甲辰 己巳")
                if "枭" in ming.zhi_shen3[3]:
                    print(
                        "财禄时干偏印格：财虽吉、人丁孤单、性格艺术化 母法总则P56-20 己巳 丙辰 甲午 壬申"
                    )

            if ming.zhis[3] == self.yin_lu:
                print(
                    "坐财禄，时支印禄：先难后易 母法总则P30-147 甲申 己巳 壬午 己酉 母法总则P55-16"
                )

        if (
            self.gan_he[3]
            and ming.gan_shens[3] == "财"
            and jin_jiao(ming.zhis[2], ming.zhis[3])
        ) or (
            self.gan_he[2]
            and self.gan_he[1]
            and ming.gan_shens[1] == "财"
            and jin_jiao(ming.zhis[1], ming.zhis[2])
        ):

            print(
                "日主合财且进角合：一生吉祥、平安有裕！ 母法总则P22-22 丁丑 丙午 甲辰 己巳"
            )

        if ming.zhis.day == self.cai_lu or ming.zhi_shens[2] == "财":
            if ming.gan_shens[3] == "枭" and (
                "枭" in ming.zhi_shen3[3] or ming.zhis[3] == self.xiao_lu
            ):
                print(
                    "日坐财，时偏印格：他乡有成，为人敦厚。母法总则P55-4 甲寅 辛未 甲午 壬申"
                )
            if self.zhi_6chong[2] or self.zhi_xing[2]:
                print(
                    "日坐财，有冲或刑：财吉而有疾。母法总则P55-10 丙寅 戊戌 甲午 甲子"
                )

        if ming.gan_shens[3] == "财" and zhi_ku(ming.zhis[3], (ming.me, self.jie)):
            print(
                "正财坐日库于时柱:孤独、难为父母，但事业有成。 母法总则P31-156 丁丑 丙午 甲辰 己巳"
            )

        # 自坐财库
        if ming.zhis[2] == self.cai_ku:
            if ming.zhis[3] == self.me_ku:
                print(
                    "自坐财库,时劫库：有财而孤单。 母法总则P30-136 丁丑 丙午 甲辰 己巳 母法总则P55-11 P61-5 甲子 己巳 壬戌 甲辰"
                )

            if ming.zhis[2] == ming.zhis[3]:
                print(
                    "自坐财库,时坐财库：妻有灾，妻反被妾制服。 母法总则P30-150 辛酉 乙未 壬戌 庚戌 母法总则P56-19"
                )

            if ming.gan_shens[3] == "杀" and "杀" in ming.zhi_shen3[3]:
                print(
                    "自坐财库,时杀格，财生杀，凶！母法总则P30-147 甲寅 己巳 壬戌 戊申 有可能是时柱有杀就算。 母法总则P55-15"
                )

        # 时坐财库
        if zhi_ku(ming.zhis[3], (self.cai, self.piancai)):
            if "伤" in ming.gan_shens and "伤" in ming.zhi_shens:
                print(
                    "时坐财库,伤官生财:财好，体弱，旺处寿倾倒！母法总则P59-8 戊申 辛酉 戊子 丙辰"
                )

        if ming.gan_shens[3] == "财" and "财" in ming.zhi_shen3[3]:
            print(
                "时上正财格:不必财旺，因妻致富。 母法总则P30-140 丙午 戊戌 壬寅 丁未 母法总则P60-21"
            )

            if ming.zhis[3] == me_ku:
                print("时上正财格坐比劫库，克妻。 母法总则P30-141 丙午 戊戌 壬寅 丁未")
            if ming.zhis[2] == self.cai_ku:
                print(
                    "时上正财格自坐财库，妻佳，中年丧妻，续弦也佳。 母法总则P30-142 庚子 辛巳 壬戌 丁未 P61-7"
                )

        # print(cai_di, cai_lu, ming.zhis, gan_he)
        if ming.zhis[3] in (self.cai_di, self.cai_lu):
            if self.gan_he[3]:
                print(
                    "时财禄，天干日时双合，损妻家财。 母法总则P31-157 庚戌 戊寅 癸酉 戊午"
                )
            if "伤" == ming.gan_shens[3] and "伤" in ming.zhi_shens2:
                print(
                    "时支正财时干伤成格：虽富有也刑克。 母法总则P59-1 丁丑 壬寅 丁巳 戊申"
                )
            # print(zhi_ku(ming.zhis[1], (shi,shang)) , (shi,shang), ming.zhis[3] == cai_lu)
            if (
                zhi_ku(ming.zhis[1], (self.shi, self.shang))
                and ming.zhis[3] == self.cai_lu
            ):
                print(
                    "时支正财禄，月支伤入墓：生财极为辛勤。 母法总则P59-4 甲子 戊辰 庚戌 己卯"
                )

        # print(cai_di, cai_lu, ming.zhis, gan_he)
        if ming.zhis[3] == self.cai_lu:
            if self.zhi_xing[3] or self.zhi_6chong[3]:
                print(
                    "时支正财禄有冲刑：得女伴且文学清贵。 母法总则P60-11 丁丑 辛亥 己巳 乙亥"
                )
            if any(self.zhi_xing[:3]) or any(self.zhi_6chong[:3]):
                print(
                    "时支正财禄,它支有冲刑：刑妻、孤高、艺术、近贵人。 母法00总则P60-19 乙未 己丑 庚寅 己卯"
                )
            if ming.gan_shens.count("财") > 1:
                print(
                    "时支正财禄,天干财星多：孤雅、九流、表面风光。 母法总则P60-20 乙酉 乙酉 庚辰 己卯"
                )

    # 十神：正官分析
    def get_zhengguan(self):
        print("\n【9.正官分析】")
        if "官" in ming.gan_shens:
            if "官" in ming.zhi_shens2:
                print(
                    "官若成格：忌伤；忌混杂；基础78。有伤用财通关或印制。混杂用合或者身官两停。日主弱则不可扶。"
                )
                self.all_ges.append("官")

                if "比" in ming.gan_shens or "劫" in ming.gan_shens:
                    print("官格透比或劫：故做清高或有洁癖的文人。")

                if "伤" in ming.gan_shens:
                    print("官格透伤：表里不一。")

                if "财" in ming.gan_shens or "才" in ming.gan_shens:
                    print("官格透财：聚财。")

                if "印" in ming.gan_shens:
                    print("官格透印：人品清雅。")

                if not (
                    "印" in ming.gan_shens
                    or "财" in ming.gan_shens
                    or "才" in ming.gan_shens
                ):
                    print("官独透成格：敦厚人。")

            if (ming.gan_shens[0] == "官" and ming.gan_shens[1] == "官") or (
                ming.gan_shens[1] == "官" and "官" in ming.zhi_shen3[1]
            ):
                print("官月重叠：女易离婚，早婚不吉利。为人性格温和。")

            if ming.gan_shens[3] == "官" and len(zhi5[ming.zhis[3]]) == 1:
                print("官专位时坐地支，男有得力子息。")
            if ming.gan_shens[0] == "官":
                print("年干为官，身强有可能出身书香门第。")
                if ming.gan_shens[3] == "官":
                    print("男命年干，时干都为官，对后代和头胎不利。")
            if (not "财" in ming.gan_shens) and (not "印" in ming.gan_shens):
                print("官独透天干成格，四柱无财或印，为老实人。")
            if "伤" in ming.gan_shens:
                print(
                    "正官伤官通根透，又无其他格局，失策。尤其是女命，异地分居居多，婚姻不美满。基64:辛未 丁酉 甲戌 辛未 "
                )
            if "杀" in ming.gan_shens:
                print("年月干杀和偏官，30以前婚姻不稳定。月时多为体弱多病。")

            if (
                "印" in ming.gan_shens
                and "印" in ming.zhi_shens2
                and "官" in ming.zhi_shens2
            ):
                print("官印同根透，无刑冲合，吉。")
                if "财" in ming.gan_shens and "财" in ming.zhi_shens2:
                    print("财官印同根透，无刑冲合，吉。")

            if (
                ming.gan_shens[1]
                == "官"
                in ten_deities[ming.me][ming.zhis[1]]
                in ("绝", "墓")
            ):
                print(
                    "官在月坐墓绝，不是特殊婚姻就是迟婚。如果与天月德同柱，依然不错。丈夫在库中：1，老夫少妻；2，不为外人所知的亲密感情；3，特殊又合法的婚姻。"
                )
            if ming.zhi_shens[1] == "官" and ming.gan_shens[1] == "官":
                print("月柱正官坐正官，婚变。月柱不宜通。坐禄的。")

            for seq, gan_ in enumerate(ming.gan_shens):
                if gan_ != "官":
                    continue
                if ming.zhi_shens[seq] in ("劫", "比"):
                    print(
                        "天干正官，地支比肩或劫财，亲友之间不适合合作，但是他适合经营烂摊子。"
                    )
                if ming.zhi_shens[seq] == "杀":
                    print(
                        "正官坐七杀，男命恐有诉讼之灾。女命婚姻不佳。月柱尤其麻烦，二度有感情纠纷。年不算，时从轻。 基64 壬子 壬子 丁丑 癸卯"
                    )
                if ming.zhi_shens[seq] == "劫" and Gan.index(ming.me) % 2 == 0:
                    print(
                        "官坐羊刃：要杀才能制服阳刃，有力不从心之事情。 辛卯 丁酉 庚午 庚辰 基65"
                    )
                if ming.zhi_shens[seq] == "印":
                    print("官坐印，无刑冲合，吉")

        if (
            ming.shens2.count("官") > 2
            and "官" in ming.gan_shens
            and "官" in ming.zhi_shens2
        ):
            print("正官多者，虚名。为人性格温和，比较实在。做七杀看")
        if ming.zhis.day == self.guan_lu or ming.zhi_shens[2] == "官":
            print("日坐正官专位，淑女。 基65 庚申 癸未 丙子 乙未")
            if is_yang() and ming.zhis.time == me_di:
                print("日坐正官，时支阳刃：先富后败，再东山再起。 子平母法 P55-7")

        if ming.gan_shens.count("官") > 2:
            print("天干2官，女下有弟妹要照顾，一生为情所困。")

        if ming.zhi_shens[1] == "官" and "伤" in ming.zhi_shens2:
            print(
                "月支正官，又成伤官格，难做真正夫妻。有实，无名。 基66辛丑 辛卯 戊子 辛酉"
            )

    # 十神：七杀分析
    def get_qisha(self):
        print("\n【10.七杀分析】")
        # 杀分析
        if "杀" in ming.gan_shens:
            print(
                "七杀是非多。但是对男人有时是贵格。比如毛主席等。成格基础85可杀生印或食制印、身杀两停、阳刃驾杀。"
            )
            if "杀" in ming.zhi_shens2:
                print(
                    "杀格：喜食神制，要食在前，杀在后。阳刃驾杀：杀在前，刃在后。身杀两停：比如甲寅日庚申月。杀印相生，忌食同成格。"
                )
                self.all_ges.append("杀")

                if "比" in ming.gan_shens or "劫" in ming.gan_shens:
                    print("杀格透比或劫：性急但还有分寸。")

                if "杀" in ming.gan_shens:
                    print("杀格透官：精明琐屑，不怕脏。")

                if "食" in ming.gan_shens or "伤" in ming.gan_shens:
                    print("杀格透食伤：外表宁静，内心刚毅。")

                if "印" in ming.gan_shens:
                    print("杀格透印：圆润、精明干练。")

            if ming.gan_shens[0] == "杀" and ming.gan_shens[1] == "杀":
                print("杀月干年干重叠：不是老大，出身平常，多灾，为人不稳重。")

            if ming.gan_shens[1] == "杀" and "杀" in ming.zhi_shen3[1]:
                print("杀月重叠：女易离婚，其他格一生多病。")

            if ming.gan_shens[0] == "杀":
                print("年干七杀，早年不好。或家里穷或身体不好。")
                if ming.gan_shens[1] == "杀":
                    print("年月天干七杀，家庭复杂。")
            if "官" in ming.gan_shens:
                print(
                    "官和杀同见天干不佳。女在年干月干，30以前婚姻不佳，或体弱多病。基65 甲寅 乙亥 戊子 丙辰"
                )
            if ming.gan_shens[1] == "杀" and ming.zhi_shens[1] == "杀":
                print("月柱都是七杀，克得太过。有福不会享。六亲福薄。时柱没关系。")
                if "杀" not in ming.zhi_shens2:
                    print("七杀年月浮现天干，性格好变，不容易定下来。30岁以前不行。")
            if "杀" in ming.zhi_shens and "劫" in ming.zhi_shens:
                print("七杀地支有根时要有阳刃强为佳。杀身两停。")
            if ming.gan_shens[1] == "杀" and ming.gan_shens[3] == "杀":
                print("月时天干为七杀：体弱多病")
            if ming.gan_shens[0] == "杀" and ming.gan_shens[3] == "杀":
                print("七杀年干时干：男头胎麻烦（概率），女婚姻有阻碍。")
            if ming.gan_shens[3] == "杀":
                print("七杀在时干，固执有毅力。基67")
            if "印" in ming.gan_shens:
                print("身弱杀生印，不少是精明练达的商人。")
            if "财" in ming.gan_shens or "才" in ming.gan_shens:
                print("财生杀，如果不是身弱有印，不佳。")
                for zhi_ in ming.zhis:
                    if set(
                        (
                            ten_deities[ming.me].inverse["杀"],
                            ten_deities[ming.me].inverse["财"],
                        )
                    ) in set(zhi5[zhi_]):
                        print("杀不喜与财同根透出，这样杀的力量太强。")

        for seq, gan_ in enumerate(ming.gan_shens):
            if gan_ != "杀" and ming.zhi_shens[seq] != "杀":
                continue
            if gan_ == "杀" and "杀" in ming.zhi_shen3[seq] and seq != 3:
                print("七杀坐七杀，六亲福薄。")
            if get_empty(ming.zhus[2], ming.zhis[seq]) == "空":
                print("七杀坐空亡，女命夫缘薄。 基68 壬申 庚戌 甲子 丙寅")
            if ming.zhis[seq] == "食":
                print("七杀坐食：易有错误判断。")
            if self.zhi_xing[seq] or self.zhi_6chong[seq]:
                print("七杀坐刑或对冲，夫妻不和。")

        if ming.shens2.count("杀") > 2:
            print("杀多者如果无制，性格刚强。打抱不平，不易听人劝。女的喜欢佩服的人。")
        if ming.zhi_shens[2] == "杀" and len(zhi5[ming.zhis[2]]) == 1:
            print(
                "天元坐杀：乙酉，己卯，如无食神，阳刃，性急，聪明，对人不信任。如果七杀还透出月干无制，体弱多病，甚至夭折。如果在时干，晚年不好。"
            )

        if (
            ming.zhus[2] in (("丁", "卯"), ("丁", "亥"), ("丁", "未"))
            and ming.zhis.time == "子"
        ):
            print("七杀坐桃花，如有刑冲，引感情引祸。忌讳午运。")

        if ming.gan_shens.count("杀") > 2:
            print("天干2杀，不是老大、性格浮躁不持久。")

        if ten_deities[self.shang].inverse["建"] in ming.zhis and ming.is_women:
            print("女地支有杀的禄：丈夫条件还可以。对外性格急，对丈夫还算顺从。")

        if ming.zhis[2] == self.me_jue:
            print("#" * 10, "自坐绝")
            if self.zhi_6he[2]:

                print(
                    "自己坐绝（天元坐杀）：日支与它支合化、双妻，子息迟。母法总则P21-9 P56-30 d第10点暂未编码。"
                )

            print("自己坐绝支，绝支合会，先贫后富。母法总则P57-3 母法总则P23-33")
            if ming.zhis[3] == ming.zhis[2]:
                print(
                    "日主日时绝，旺达则有刑灾。母法总则P57-2 母法总则P24-43 戊午 癸亥 乙酉 乙酉"
                )

            if ming.zhis[3] == ming.zhis[2] == ming.zhis[1]:
                print("日主月日时绝，旺达则有刑灾，平常人不要紧。母法总则P57-1")
            if ming.zhi_shens.count("比") + ming.zhi_shens.count("劫") > 1:
                print(
                    "自坐绝，地支比劫大于1，旺衰巨变，凶：母法总则P22-16。 母法总则P36-5月支或时支都为阳刃，凶。"
                )

            if ming.zhis[1] == self.me_jue:
                print("日主月日绝，有格也疾病夭。母法总则P23-35")

            if ming.zhis[3] == self.cai_lu:
                print(
                    " 母法总则P59-2  自坐绝，月支财禄:身弱财旺有衰困时，克妻子。书上例子不对"
                )

            if ming.zhis[3] == self.cai_di:
                print(
                    " 母法总则P59-3  自坐绝，月支偏财禄:有困顿时娶背景不佳妻。书上例子不对"
                )

        if ming.zhis[3] == self.me_jue:
            print(
                "#" * 10,
                "自己时坐绝: 母法总则P57-4: 若成伤官格，难求功名，适合艺术九流。",
            )
            if ming.zhi_shens[2] == "枭":
                print(
                    "母法总则P57-5: 自时支坐绝，自坐枭: 不是生意人，清贫艺术九流人士。"
                )
            # print(ming.zhi_shens, cai_di, cai_lu)
            if ming.zhis[1] in (self.cai_di, self.cai_lu):
                print(
                    " 母法总则P57-6  自时支坐绝，月支坐财:先富，晚年大败，刑破。 癸未 庚申 丁巳 庚子"
                )

            if ming.zhis[1] in (ming.me_lu, self.me_di):
                print(
                    " 母法总则P28-114  自时支坐绝，月支帝:刑妻克子。 甲子 癸酉 辛丑 辛卯 -- 阴干也算阳刃？"
                )

            if ming.zhis[3] in (self.cai_di, self.cai_lu):
                print(
                    " 母法总则P57-8  自时支坐绝，时支财:中年发后无作为。 甲子 癸酉 辛丑 辛卯"
                )

        if ming.zhis[2] == self.sha_lu:
            if zhi_ku(ming.zhis[3], (self.guan, self.sha)):
                print(
                    "自坐杀禄，时支为官杀库，一生有疾，生计平常。 母法总则P21-12 母法总则P55-8 甲子 丙寅 乙酉 己丑 P56-31"
                )

        if ming.zhis[3] == self.sha_lu:
            if self.zhi_xing[3] or self.zhi_6chong[3]:

                print(
                    "时支杀禄带刑冲：纵然吉命也带疾不永寿。 母法总则P60-15 乙未 乙酉 戊申 甲寅"
                )

        if ming.gan_shens[3] == "杀" and ming.zhis[3] in (self.cai_di, self.cai_lu):
            print(
                "七杀时柱坐财禄旺：性格严肃。 母法总则P59-7 母法总则P79-3 双妻，子息迟。 "
            )

        # print(sha_lu, zhi_6chong,zhi_xing )
        if ming.zhis[3] == self.sha_lu:
            if self.zhi_6chong[3] or self.zhi_xing[3]:
                print(
                    "七杀时禄旺：遇刑冲寿夭带疾。 母法总则P28-118 冲别的柱也算？ 乙未 戊寅 辛丑 甲午 "
                )
            if ming.zhis[1] == self.sha_lu:
                print(
                    "七杀时月禄旺：体疾。 母法总则P28-119 甲寅 庚午 辛丑 甲午  母法总则P60-16"
                )

        # print(zhi_ku(ming.zhis[2], (guan,sha)),set(ming.zhis), set('辰戌丑未'))
        if zhi_ku(ming.zhis[2], (self.guan, self.sha)):
            if set(ming.zhis).issubset(set("辰戌丑未")):
                print(
                    "自坐七杀入墓：地支都为库，孤独艺术。 母法总则P57-33  丙辰 戊戌 乙丑 庚辰"
                )

        if "杀" in ming.gan_shens and ming.zhi_shens.count("杀") > 1:
            print(
                "七杀透干，地支双根，不论贫富，亲属离散。母法总则P79-6 乙未 丙戌 戊寅 甲寅"
            )

        if "杀" in self.jus + self.all_ges:

            if "比" in ming.gan_shens or "劫" in ming.gan_shens:
                print("杀格透比或劫：性急但还有分寸。")

            if "杀" in ming.gan_shens:
                print("杀格透官：精明琐屑，不怕脏。")

            if "食" in ming.gan_shens or "伤" in ming.gan_shens:
                print("杀格透食伤：外表宁静，内心刚毅。")

            if "印" in ming.gan_shens:
                print("杀格透印：圆润、精明干练。")

    def get_dayun_detail(self):
        # 计算大运
        get_yun(ming)

    def get_geju3(self):
        print()
        print("-" * 120)
        print(
            "\033[1;31;40m",
            "格",
            self.all_ges,
            "局",
            self.jus,
            "\033[0m",
        )

        if ming.me + ming.zhis.month in months:
            print("\n\n《穷通宝鉴》")
            print("=========================")
            print(months[ming.me + ming.zhis.month])

        sum_index = "".join([ming.me, "日", *ming.zhus[3]])
        if sum_index in summarys:
            print("\n\n《三命通会》")
            print("=========================")
            print(summarys[sum_index])

        # 检查三会 三合的拱合
        result = ""
        # for i in range(2):
        # result += check_gong(ming.zhis, i*2, i*2+1, me, gong_he)
        # result += check_gong(ming.zhis, i*2, i*2+1, me, gong_hui, '三会拱')

        result += check_gong(ming.zhis, 1, 2, ming.me, gong_he)
        result += check_gong(ming.zhis, 1, 2, ming.me, gong_hui, "三会拱")

        if result:
            print(result)

        print("=" * 120)

        # 格局分析
        ge = ""
        if (ming.me, ming.zhis.month) in jianlus:
            print(jianlu_desc)
            print("-" * 120)
            print(jianlus[(ming.me, ming.zhis.month)])
            print("-" * 120 + "\n")
            ge = "建"
        # elif (ming.me == '丙' and ('丙','申') in zhus) or (ming.me == '甲' and ('己','巳') in zhus):
        # print("格局：专财. 运行官旺 财神不背,大发财官。忌行伤官、劫财、冲刑、破禄之运。喜身财俱旺")
        elif (ming.me, ming.zhis.month) in (("甲", "卯"), ("庚", "酉"), ("壬", "子")):
            ge = "月刃"
        else:
            zhi = ming.zhis[1]
            if zhi in wuhangs["土"] or (ming.me, ming.zhis.month) in (
                ("乙", "寅"),
                ("丙", "午"),
                ("丁", "巳"),
                ("戊", "午"),
                ("己", "巳"),
                ("辛", "申"),
                ("癸", "亥"),
            ):
                for item in zhi5[zhi]:
                    if item in ming.gans[:2] + ming.gans[3:]:
                        ge = ten_deities[ming.me][item]
            else:
                d = zhi5[zhi]
                ge = ten_deities[ming.me][max(d, key=d.get)]
        self.ge = ge

    def get_jiecai_ge(self):
        print("1.【劫财格分析】")
        if self.ge == "劫":
            print("\n****劫财(阳刃)分析****：阳刃冲合岁君,勃然祸至。身弱不作凶。")
            print("======================================")
            if "劫" == ming.gan_shens[3] or "劫" == ming.zhi_shens[3]:
                print("劫财阳刃,切忌时逢,岁运并临,灾殃立至,独阳刃以时言,重于年月日也。")

            shi_num = ming.shens.count("食")
            print("-" * 120)

    def get_yin_ge(self):
        print("2.【印格分析】")
        if self.ge == "印":
            print(
                "\n印分析 **** 喜:食神 天月德 七煞 逢印看煞 以官为引   忌： 刑冲 伤官 死墓 辰戊印怕木 丑未印不怕木"
            )
            print("一曰正印 二曰魁星 三曰孙极星")
            print(
                "以印绶多者为上,月最要,日时次之,年干虽重,须归禄月、日、时,方可取用,若年露印,月日时无,亦不济事。"
            )
            print("======================================")
            if "官" in ming.shens:
                print("官能生印。身旺印强，不愁太过，只要官星清纯")
            if "杀" in ming.shens:
                print(
                    "喜七煞,但煞不可太多,多则伤身。原无七煞,行运遇之则发;原有七煞,行财运,或印绶死绝,或临墓地,皆凶。"
                )
            if "伤" in ming.shens or "食" in ming.shens:
                print(
                    "伤食：身强印旺，恐其太过，泄身以为秀气；若印浅身轻，而用层层伤食，则寒贫之局矣。"
                )
            if "财" in ming.shens or "才" in ming.shens:
                print(
                    "有印多而用财者，印重身强，透财以抑太过，权而用之，只要根深，无防财破。 若印轻财重，又无劫财以救，则为贪财破印，贫贱之局也。"
                )

            if self.yin_num > 1:
                print(
                    "印绶复遇拱禄、专禄、归禄、鼠贵、夹贵、时贵等格,尤为奇特,但主少子或无子,印绶多者清孤。"
                )
            if "劫" in ming.shens:
                print("化印为劫；弃之以就财官")
            print()
            print("-" * 120)

    def get_xiao_ge(self):
        print("3.【偏印格分析】")
        if self.ge == "枭":
            print(
                "\n印分析 **** 喜:食神 天月德 七煞 逢印看煞 以官为引   忌： 刑冲 伤官 死墓 辰戊印怕木 丑未印不怕木"
            )
            print("一曰正印 二曰魁星 三曰孙极星")
            print(
                "以印绶多者为上,月最要,日时次之,年干虽重,须归禄月、日、时,方可取用,若年露印,月日时无,亦不济事。"
            )
            print("======================================")
            if "官" in ming.shens:
                print("官能生印。身旺印强，不愁太过，只要官星清纯")
            if "杀" in ming.shens:
                print(
                    "喜七煞,但煞不可太多,多则伤身。原无七煞,行运遇之则发;原有七煞,行财运,或印绶死绝,或临墓地,皆凶。"
                )
            if "伤" in ming.shens or "食" in ming.shens:
                print(
                    "伤食：身强印旺，恐其太过，泄身以为秀气；若印浅身轻，而用层层伤食，则寒贫之局矣。"
                )
            if "财" in ming.shens or "才" in ming.shens:
                print("弃印就财。")

            if self.yin_num > 1:
                print(
                    "印绶复遇拱禄、专禄、归禄、鼠贵、夹贵、时贵等格,尤为奇特,但主少子或无子,印绶多者清孤。"
                )
            if "劫" in ming.shens:
                print("化印为劫；弃之以就财官")
            print()
            print("-" * 120)

    def get_shishen_ge(self):
        print("4.【食神格分析】")
        if self.ge == "食":
            print(
                "\n****食神分析****: 格要日主食神俱生旺，无冲破。有财辅助财有用。  食神可生偏财、克杀"
            )
            print(
                " 阳日食神暗官星，阴日食神暗正印。食神格人聪明、乐观、优雅、多才多艺。食居先，煞居后，功名显达。"
            )
            print("======================================")
            print(
                """
            喜:身旺 宜行财乡 逢食看财  忌:身弱 比 倒食(偏印)  一名进神　　二名爵星　　三名寿星
            月令建禄最佳，时禄次之，更逢贵人运
            """
            )

            shi_num = ming.shens.count("食")
            if shi_num > 2:
                print(
                    "食神过多:食神重见，变为伤官，令人少子，纵有，或带破拗性. 行印运",
                    end=" ",
                )
            if set(("财", "食")) in set(ming.gan_shens[:2] + ming.zhi_shens[:2]):
                print("祖父荫业丰隆", end=" ")
            if set(("财", "食")) in set(ming.gan_shens[2:] + ming.zhi_shens[2:]):
                print("妻男获福，怕母子俱衰绝，两皆无成", end=" ")
            if self.cai_num > 1:
                print("财多则不清，富而已", end=" ")

            for seq, item in enumerate(ming.gan_shens):
                if item == "食":
                    if ten_deities[ming.gans[seq]][ming.zhis[seq]] == "墓":
                        print("食入墓，即是伤官入墓，住寿难延。")

            for seq, item in enumerate(ming.gan_shens):
                if item == "食" or ming.zhi_shens[seq] == "食":
                    if get_empty(self.zhus[2], ming.zhis[seq]):
                        print(
                            "大忌空亡，更 有官煞显露，为太医师巫术数九流之士，若食神逢克，又遇空亡，则不贵，再行死绝或枭运，则因食上气上生灾，翻胃噎食，缺衣食，忍饥寒而已"
                        )

            # 倒食分析
            if (
                "枭" in ming.shens
                and (ming.me not in ["庚", "辛", "壬"])
                and ten_deities[ming.me] != "建"
            ):
                flag = True
                for item in zhi5[ming.zhis.day]:
                    if ten_deities[ming.me]["合"] == item:
                        flag = False
                        break
                if flag:
                    print(
                        "倒食:凡命带倒食，福薄寿夭，若有制合没事，主要为地支为天干的杀;日支或者偏印的坐支为日主的建禄状态。偏印和日支的主要成分天干合"
                    )
                    print(
                        "凡命有食遇枭，犹尊长之制我，不得自由，作事进退悔懒，有始无终，财源屡成屡败，容貌欹斜，身品琐小，胆怯心虚，凡事无成，克害六亲，幼时克母，长大伤妻子"
                    )
                    print("身旺遇此方为福")
            print()
            print("-" * 120)

    def get_shuangguan_ge(self):
        print("5.【伤官格分析】")
        if self.ge == "伤":
            print(
                "\n****伤官分析****: 喜:身旺,财星,印绶,伤尽 忌:身弱,无财,刑冲,入墓枭印　"
            )
            print(
                " 多材艺，傲物气高，心险无忌惮，多谋少遂，弄巧成拙，常以天下之人不如己，而人亦惮之、恶之。 一名剥官神　　二名羊刃煞"
            )
            print(" 身旺用财，身弱用印。用印不忌讳官煞。用印者须去财方能发福")
            print(
                "官星隐显，伤之不尽，岁运再见官星，官来乘旺，再见刑冲破害，刃煞克身，身弱财旺，必主徒流死亡，五行有救，亦残疾。若四柱无官而遇伤煞重者，运入官乡，岁君又遇，若不目疾，必主灾破。"
            )
            print("娇贵伤不起、谨慎过头了略显胆小，节俭近于吝啬")
            print("======================================")

            if "财" in self.shens or "才" in ming.shens:
                print("伤官生财")
            else:
                print("伤官无财，主贫穷")

            if "印" in ming.shens or "枭" in ming.shens:
                print(
                    "印能制伤，所以为贵，反要伤官旺，身稍弱，始为秀气;印旺极深，不必多见，偏正叠出，反为不秀，故伤轻身重而印绶多见，贫穷之格也。"
                )
                if "财" in ming.shens or "才" in ming.shens:
                    print(
                        "财印相克，本不并用，只要干头两清而不相碍；又必生财者，财太旺而带印，佩印者印太重而带财，调停中和，遂为贵格"
                    )
            if "官" in ming.shens:
                print(shang_guans[ten_deities[ming.me]["本"]])
                print(
                    "金水独宜，然要财印为辅，不可伤官并透。若冬金用官，而又化伤为财，则尤为极秀极贵。若孤官无辅，或官伤并透，则发福不大矣。"
                )
            if "杀" in ming.shens:
                print("煞因伤而有制，两得其宜，只要无财，便为贵格")
            if ming.gan_shens[0] == "伤":
                print(
                    "年干伤官最重，谓之福基受伤，终身不可除去，若月支更有，甚于伤身七煞"
                )

            for seq, item in enumerate(ming.gan_shens):
                if item == "伤":
                    if ten_deities[ming.gans[seq]][ming.zhis[seq]] == "墓":
                        print("食入墓，即是伤官入墓，住寿难延。")

            for seq, item in enumerate(ming.gan_shens):
                if item == "食" or ming.zhi_shens[seq] == "食":
                    if get_empty(zhus[2], ming.zhis[seq]):
                        print(
                            "大忌空亡，更有官煞显露，为太医师巫术数九流之士，若食神逢克，又遇空亡，则不贵，再行死绝或枭运，则因食上气上生灾，翻胃噎食，缺衣食，忍饥寒而已"
                        )
            print()
            print("-" * 120)

    def get_cai_ge(self):
        print("6.【财格分析】")

        if self.ge == "财" or self.ge == "才":
            print(
                "\n****财分析 **** 喜:旺,印,食,官 忌:比 羊刃 空绝 冲合   财星,天马星,催官星,壮志神"
            )
            if ming.gan_shens.count("财") + ming.gan_shens.count("才") > 1:
                print(
                    "财喜根深，不宜太露，然透一位以清用，格所最喜，不为之露。即非月令用神，若寅透乙、卯透甲之类，一亦不为过，太多则露矣。"
                )
                print(
                    "财旺生官，露亦不忌，盖露不忌，盖露以防劫，生官则劫退，譬如府库钱粮，有官守护，即使露白，谁敢劫之？"
                )
            if "伤" in ming.gan_shens:
                print("有伤官，财不能生官")
            if "食" in ming.shens:
                print("有财用食生者，身强而不露官，略带一位比劫，益觉有情")
                if "印" in ming.shens or "枭" in ming.shens:
                    print("注意印食冲突")
            if "比" in ming.shens:
                print("比不吉，但是伤官食神可化!")
            if "杀" in ming.shens:
                print("不论合煞制煞，运喜食伤身旺之方!")

            if "财" == ming.zhi_shens[0]:
                print(
                    "岁带正马：月令有财或伤食，不犯刑冲分夺，旺祖业丰厚。同类月令且带比，或遇运行伤劫 贫"
                )
            if "财" == ming.zhi_shens[3]:
                print(
                    "时带正马：无冲刑破劫，主招美妻，得外来财物，生子荣贵，财产丰厚，此非父母之财，乃身外之财，招来产业，宜俭不宜奢。"
                )
            if "财" == ming.zhi_shens[2] and (ming.me not in ("壬", "癸")):
                print("天元坐财：喜印食 畏官煞，喜月令旺 ")
            if (
                ("官" not in ming.shens)
                and ("伤" not in ming.shens)
                and ("食" not in ming.shens)
            ):
                print("财旺生官:若月令财无损克，亦主登科")

            if (
                self.cai_num > 2
                and ("劫" not in ming.shens)
                and ("比" not in ming.shens)
                and ("比" not in ming.shens)
                and ("印" not in ming.shens)
            ):
                print(
                    "财　不重叠多见　财多身弱，柱无印助; 若财多身弱，柱无印助不为福。"
                )

            if "印" in ming.shens:
                print("先财后印，反成其福，先印后财，反成其辱是也?")
            if "官" in ming.gan_shens:
                print("官星显露，别无伤损，或更食生印助日主健旺，富贵双全")
            if "财" in ming.gan_shens and (
                ("劫" not in ming.shens) and ("比" not in ming.shens)
            ):
                print("财不宜明露")
            for seq, item in enumerate(ming.gan_shens):
                if item == "财":
                    if ten_deities[ming.gans[seq]][ming.zhis[seq]] == "墓":
                        print("财星入墓，必定刑妻")
                    if ten_deities[ming.gans[seq]][ming.zhis[seq]] == "长":
                        print("财遇长生，田园万顷")

            if ("官" not in ming.shens) and (
                ("劫" in ming.shens) or ("比" in ming.shens)
            ):
                print("切忌有姊妹兄弟分夺，柱无官星，祸患百出。")

            if self.bi_num + self.jie_num > 1:
                print("兄弟辈出: 纵入官乡，发福必渺.")

            for seq, item in enumerate(ming.zhi_shens):
                if item == "才" or ten_deities[ming.me][ming.zhis[seq]] == "才":
                    if get_empty(ming.zhus[2], ming.zhis[seq]):
                        print("空亡 官将不成，财将不住")

            print("-" * 120)

        # 财库分析
        if ten_deities[ten_deities[ming.me].inverse["财"]]["库"][-1] in ming.zhis:
            print("财临库墓: 一生财帛丰厚，因财致官, 天干透土更佳")
        if self.cai_num < 2 and (("劫" in ming.shens) or ("比" in ming.shens)):
            print("财少身强，柱有比劫，不为福")

    def get_zhengguan_ge(self):
        print("7.【官格分析】")
        if self.ge == "官":
            print(
                "\n**** 官分析 ****\n 喜:身旺 财印   忌：身弱 偏官 伤官 刑冲 泄气 贪合 入墓"
            )
            print(
                "一曰正官 二曰禄神 最忌刑冲破害、伤官七煞，贪合忘官，劫财比等等，遇到这些情况便成为破格 财印并存要分开"
            )
            print(
                "运：财旺印衰喜印，忌食伤生财；旺印财衰喜财，喜食伤生财；带伤食用印制；"
            )
            print(
                "带煞伤食不碍。劫合煞财运可行，伤食可行，身旺，印绶亦可行；伤官合煞，则伤食与财俱可行，而不宜逢印"
            )
            print("======================================")

            if self.guan_num > 1:
                print("官多变杀，以干为准")
            if (
                "财" in ming.shens
                and "印" in ming.shens
                and ("伤" not in ming.shens)
                and ("杀" not in ming.shens)
            ):
                print(
                    "官星通过天干显露出来，又得到财、印两方面的扶持，四柱中又没有伤煞，行运再引到官乡，是大富大贵的命。"
                )
            if "财" in ming.shens or "才" in ming.shens:
                print("有财辅助")
            if "印" in ming.shens or "枭" in ming.shens:
                print(
                    "有印辅助　正官带伤食而用印制，运喜官旺印旺之乡，财运切忌。若印绶叠出，财运亦无害矣。"
                )
            if "食" in ming.shens:
                print(
                    "又曰凡论官星，略见一位食神坐实，便能损局，有杀则无妨。惟月令隐禄，见食却为三奇之贵。因为食神和官相合。"
                )
            if "伤" in ming.shens:
                print("伤官需要印或偏印来抑制，　有杀也无妨")
            if "杀" in ming.shens:
                print(
                    "伤官需要印或偏印来抑制。用劫合煞，则财运可行，伤食可行，身旺，印绶亦可行，只不过复露七煞。若命用伤官合煞，则伤食与财俱可行，而不宜逢印矣。"
                )

            if ming.zhi_shens[2] in ("财", "印"):
                print("凡用官，日干自坐财印，终显")
            if ming.zhi_shens[2] in ("伤", "杀"):
                print("自坐伤、煞，终有节病")

            # 检查天福贵人
            if (self.guan, ten_deities[self.guan].inverse["建"]) in self.zhus:
                print("天福贵人:主科名巍峨，官职尊崇，多掌丝纶文翰之美!")

            # 天元坐禄
            if self.guan in zhi5[ming.zhis[2]]:
                print(
                    "天元作禄: 日主与官星并旺,才是贵命。大多不贵即富,即使是命局中有缺点,行到好的大运时,便能一发如雷。"
                )
                print(tianyuans[ten_deities[ming.me]["本"]])

            # 岁德正官
            if ming.gan_shens[0] == "官" or ming.zhi_shens[0] == "官":
                print(
                    "岁德正官: 必生宦族,或荫袭祖父之职,若月居财官分野,运向财官旺地,日主健旺,贵无疑矣。凡年干遇官,福气最重,发达必早。"
                )

            # 时上正官
            if ming.gan_shens[0] == "官" or ming.zhi_shens[0] == "官":
                print(
                    "时上正官: 正官有用不须多，多则伤身少则和，日旺再逢生印绶，定须平步擢高科。"
                )

            print()
            print("-" * 120)
        # 官库分析
        if ten_deities[ten_deities[ming.me].inverse["官"]]["库"][-1] in ming.zhis:
            print("官临库墓")
            if lu_ku_cai[ming.me] in ming.zhis:
                print("官印禄库: 有官库，且库中有财")

    def get_qisha_ge(self):
        print("8.【七杀格分析】")
        if self.ge == "杀":
            print(
                "\n杀(偏官)分析 **** 喜:身旺  印绶  合煞  食制 羊刃  比  逢煞看印及刃  以食为引   忌：身弱  财星  正官  刑冲  入墓"
            )
            print(
                "一曰偏官 二曰七煞 三曰五鬼 四曰将星 五曰孤极星 原有制伏,煞出为福,原无制伏,煞出为祸   性情如虎，急躁如风,尤其是七杀为丙、丁火时。"
            )
            print(
                "坐长生、临官、帝旺,更多带比同类相扶,则能化鬼为官,化煞为权,行运引至印乡,必发富贵。倘岁运再遇煞地,祸不旋踵。"
            )
            print("七杀喜酒色而偏争好斗、爱轩昂而扶弱欺强")
            print("======================================")
            if "财" in ming.shens:
                print("逢煞看财,如身强煞弱,有财星则吉,身弱煞强,有财引鬼盗气,非贫则夭;")
            if "比" in ming.shens:
                print("如果比比自己弱，可以先挨杀。")
            if "食" in ming.shens:
                print("有食神透制,即《经》云:一见制伏,却为贵本")
                if (
                    "财" in ming.shens
                    or "印" in ming.shens
                    or "才" in ming.shens
                    or "枭" in ming.shens
                ):
                    print(
                        "煞用食制，不要露财透印，以财能转食生煞，而印能去食护煞也。然而财先食后，财生煞而食以制之，或印先食后，食太旺而印制，则格成大贵。"
                    )
            if "劫" in ming.shens:
                print("有阳刃配合,即《经》云:煞无刃不显,逢煞看刃是也。")
            if "印" in ming.shens:
                print("印: 则煞生印，印生身")
            if self.sha_num > 1:
                print("七煞重逢")
                if self.weak:
                    print(
                        "弃命从煞，须要会煞从财.四柱无一点比印绶方论，如遇运扶身旺，与煞为敌，从煞不专，故为祸患"
                    )
                    print(
                        "阴干从地支，煞纯者多贵，以阴柔能从物也。阳干从地支，煞纯者亦贵，但次于阴，以阳不受制也。"
                    )
                    print("水火金土皆从，惟阳木不能从，死木受斧斤，反遭其伤故也。")
                    print(
                        "古歌曰：五阳坐日全逢煞，弃命相从寿不坚，如是五阴逢此地，身衰煞旺吉堪言。"
                    )
            if "杀" == ming.zhi_shens[2]:
                print("为人心多性急，阴险怀毒，僭伪谋害，不近人情")
            if "杀" == ming.zhi_shens[3] or "杀" == ming.gan_shens[3]:
                print(
                    " 时杀：月制干强，其煞反为权印。《经》云：时上偏官身要强，阳刃、冲刑煞敢当，制多要行煞旺运，煞多制少必为殃。"
                )
                print(
                    " 一位为妙，年、月、日重见，反主辛苦劳碌。若身旺，煞制太过，喜行煞旺运，或三合煞运，如无制伏，要行制伏运方发。但忌身弱，纵得运扶持发福，运过依旧不济。"
                )
                print("《独步》云：时上一位，贵藏在支中，是日，主要旺强名利，方有气。")
                print(
                    "《古歌》云：时上偏官喜刃冲，身强制伏禄丰隆。正官若也来相混，身弱财多主困穷。"
                )
                print(
                    "时上偏官一位强，日辰自旺喜非常。有财有印多财禄，定是天生作栋梁。"
                )
                print("煞临子位，必招悖逆之儿。")

            if "杀" == ming.zhi_shens[0]:
                print(" 年上七煞：出身寒微，命有贵子。")
                print(
                    "岁煞一位不宜制，四柱重见却宜制，日主生旺，制伏略多，喜行煞旺地，制伏太过，或煞旺身衰，官煞混杂，岁运如之，碌碌之辈。若制伏不及，运至身衰煞旺乡，必生祸患。"
                )
                print("《独步》云：时上一位，贵藏在支中，是日，主要旺强名利，方有气。")
                print(
                    "《古歌》云：时上偏官喜刃冲，身强制伏禄丰隆。正官若也来相混，身弱财多主困穷。"
                )
                print(
                    "时上偏官一位强，日辰自旺喜非常。有财有印多财禄，定是天生作栋梁。"
                )
            if "官" in ming.shens:
                print("官煞混杂：身弱多夭贫")

            for seq, item in enumerate(ming.gan_shens):
                if item == "杀":
                    if ten_deities[ming.gans[seq]][ming.zhis[seq]] == "长":
                        print("七煞遇长生乙位，女招贵夫。")
            print()
            print("-" * 120)
