from ganzhi import *


class Ming:
    # 命造

    # 八字信息
    def __init__(self, gans, zhis, is_women, lunar):
        self.gans = gans  # 天干
        self.zhis = zhis  # 地支
        self.is_women = is_women  # 性别
        self.lunar = lunar  # 农历日期时辰

        self.zhus = [item for item in zip(gans, zhis)]  # 四柱
        self.me = gans.day  # 日元
        self.month = zhis.month  # 月令
        self.alls = list(gans) + list(zhis)  # 命主八字列表

    # 排盘
    def get_shens(self):
        # 天干
        gan_shens = []
        for seq, item in enumerate(self.gans):
            if seq == 2:
                gan_shens.append("--")
            else:
                gan_shens.append(ten_deities[self.me][item])
        self.gan_shens = gan_shens  # 主星 天干十神

        # 地支
        zhi_shens = []  # 地支的主气神
        for item in self.zhis:
            d = zhi5[item]
            zhi_shens.append(ten_deities[self.me][max(d, key=d.get)])
        self.zhi_shens = zhi_shens  # 地支十神

        # 藏干
        zhi_shens2 = []  # 副星，地支的所有神，包含主气、余气和尾气, 混合在一起
        zhi_shen3 = []  # 地支所有神，字符串格式
        for item in self.zhis:
            d = zhi5[item]
            tmp = ""
            for item2 in d:
                zhi_shens2.append(ten_deities[self.me][item2])
                tmp += ten_deities[self.me][item2]
            zhi_shen3.append(tmp)

        self.zhi_shens2 = (
            zhi_shens2  # 副星，地支的所有神，包含主气、余气和尾气, 混合在一起
        )
        self.zhi_shen3 = zhi_shen3  # 地支所有神，按柱合并

        self.shens = gan_shens + zhi_shens  # 天干地支十神
        self.shens2 = gan_shens + self.zhi_shens2  # 十神

        # print("===============")
        # print(self.zhi_shens)  #['财', '枭', '杀', '官']
        # print(self.zhi_shens2)
        #  # ['财', '官', '印', '枭', '杀', '才', '食', '官', '枭', '才']
        # print(self.zhi_shen3)  # ['财官印', '枭', '杀才食', '官枭才']
        # print(self.shens)
        # print(self.shens2)
