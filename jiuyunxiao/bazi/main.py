#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Aeneas(aeneas.he@gmail.com)
# CreateDate: 2019-2-21

# python main.py 1977 8 11 19 -w
# python main.py 1988 3 14 6
# python main.py 1992 8 26 7 -w 黄
# python main.py 2010 8 14 6 -w 赖

from mingengine import MingEngine


me = MingEngine()

me.get_base()
me.get_relationship()
me.get_shens()  # 计算十神

me.get_dayun()
me.get_geju()
me.get_geju2()

# 神煞
me.get_shensha()

# 十神分析
# 比劫代表自己
# 财代表青年
# 官杀代表中年
# 食伤代表晚年

me.get_zhengyin()  # 印
me.get_pianyin()  # 偏印
me.get_bijian()  # 比肩
me.get_jiecai()  # 劫财

me.get_shishen()  # 食神
me.get_shangguan()  # 伤官
me.get_zhengcai()  # 正财
me.get_piancai()  # 偏财
me.get_zhengguan()  # 正官
me.get_qisha()  # 偏官


# # 格局分析
me.get_geju3()

me.get_yin_ge()  # 正印
me.get_xiao_ge()  # 偏印
me.get_jiecai_ge()  # 劫财

me.get_shishen_ge()  # 食神
me.get_shuangguan_ge()  # 伤官
me.get_cai_ge()  # 财格
me.get_zhengguan_ge()  # 正官格
me.get_qisha_ge()  # 七杀格


# # 大运分析
# me.get_dayun_detail()
