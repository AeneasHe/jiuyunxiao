#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Aeneas(aeneas.he@gmail.com)
# CreateDate: 2019-2-21

# python main.py 1977 8 11 19 -w
# python main.py 1988 3 14 6

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
# 印代表幼年
# 财代表青年
# 官杀代表中年
# 食伤代表晚年

me.get_bijian()
me.get_jiecai()
me.get_pianyin()
me.get_zhengyin()
me.get_shishen()
me.get_shangguan()
me.get_piancai()
me.get_zhengcai()
me.get_zhengguan()
me.get_qisha()

# # 格局分析
me.get_geju3()
me.get_jiecai_ge()
me.get_xiao_ge()
me.get_yin_ge()
me.get_shishen_ge()
me.get_shuangguan_ge()
me.get_cai_ge()
me.get_qisha_ge()
me.get_zhengguan_ge()

# # 大运分析
# me.get_dayun_detail()
