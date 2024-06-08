from ganzhi import *

class Ming:
    # 命造

    # 八字信息
    def __init__(self, gans,zhis,is_women,lunar):
        self.gans = gans # 天干
        self.zhis=zhis # 地支
        self.is_women= is_women # 性别
        self.lunar = lunar # 农历日期时辰

        self.zhus= [item for item in zip(gans, zhis)] # 四柱
        self.me = gans.day # 日元
        self.month = zhis.month  # 月令
        self.alls = list(gans) + list(zhis)  # 命主八字列表
    
    # 十神信息
    def get_shens(self):
        gan_shens = []
        for seq, item in enumerate(self.gans):    
            if seq == 2:
                gan_shens.append('--')
            else:
                gan_shens.append(ten_deities[self.me][item])
        
        zhi_shens = [] # 地支的主气神
        for item in self.zhis:
            d = zhi5[item]
            zhi_shens.append(ten_deities[self.me][max(d, key=d.get)])

        self.gan_shens= gan_shens  # 天干十神
        self.zhi_shens= zhi_shens # 地支十神
        self.zhi_shens2 = [] # 地支的所有神，包含余气和尾气, 混合在一起
        self.zhi_shen3 = [] # 地支所有神，字符串格式
        self.shens = gan_shens + zhi_shens # 十神

        for item in self.zhis:
            d = zhi5[item]
            tmp = ''
            for item2 in d:
                self.zhi_shens2.append(ten_deities[self.me][item2])
                tmp += ten_deities[self.me][item2]
            self.zhi_shen3.append(tmp)
        self.shens2 = gan_shens + self.zhi_shens2
            