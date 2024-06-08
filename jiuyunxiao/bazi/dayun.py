from  ganzhi import *
from common import *
from gets import *

def get_yun(ming):
    # 如果命造有准确日期时辰，计算大运
    if ming.lunar: 
        ba = ming.lunar.getEightChar()  # 根据农历算出八字
        yun = ba.getYun(not ming.is_women)   

        print("\n\n大运")    
        print("="*120)  
        for dayun in yun.getDaYun()[1:]:
            gan_ = dayun.getGanZhi()[0]
            zhi_ = dayun.getGanZhi()[1]
            fu = '*' if (gan_, zhi_) in ming.zhus else " "
            zhi5_ = ''
            for gan in zhi5[zhi_]:
                zhi5_ = zhi5_ + "{}{}　".format(gan, ten_deities[ming.me][gan]) 
            
            zhi__ = set() # 大运地支关系
            
            for item in ming.zhis:
            
                for type_ in zhi_atts[zhi_]:
                    if item in zhi_atts[zhi_][type_]:
                        zhi__.add(type_ + ":" + item)
            zhi__ = '  '.join(zhi__)
            
            empty = chr(12288)
            if zhi_ in empties[ming.zhus[2]]:
                empty = '空'        
            
            jia = ""
            if gan_ in ming.gans:
                for i in range(4):
                    if gan_ == ming.gans[i]:
                        if abs(Zhi.index(zhi_) - Zhi.index(ming.zhis[i])) == 2:
                            jia = jia + "  --夹：" +  Zhi[( Zhi.index(zhi_) + Zhi.index(ming.zhis[i]) )//2]
                        if abs( Zhi.index(zhi_) - Zhi.index(ming.zhis[i]) ) == 10:
                            jia = jia + "  --夹：" +  Zhi[(Zhi.index(zhi_) + Zhi.index(ming.zhis[i]))%12]
                    
            out = "{1:<4d}{2:<5s}{3} {15} {14} {13}  {4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<10s} {11}".format(
                chr(12288), dayun.getStartAge(), '', dayun.getGanZhi(),ten_deities[ming.me][gan_], gan_,check_gan(gan_, ming.gans), 
                zhi_, yinyang(zhi_), ten_deities[ming.me][zhi_], zhi5_, zhi__,empty, fu, nayins[(gan_, zhi_)], ten_deities[ming.me][zhi_]) 
            gan_index = Gan.index(gan_)
            zhi_index = Zhi.index(zhi_)
            out = out + jia + get_shens(ming.gans, ming.zhis, ming.me,gan_, zhi_)
            
            print(out)
            zhis2 = list(ming.zhis) + [zhi_]
            gans2 = list(ming.gans) + [gan_]
            for liunian in dayun.getLiuNian():
                gan2_ = liunian.getGanZhi()[0]
                zhi2_ = liunian.getGanZhi()[1]
                fu2 = '*' if (gan2_, zhi2_) in ming.zhus else " "
                #print(fu2, (gan2_, zhi2_),zhus)
                
                zhi6_ = ''
                for gan in zhi5[zhi2_]:
                    zhi6_ = zhi6_ + "{}{}　".format(gan, ten_deities[ming.me][gan])        
                
                # 大运地支关系
                zhi__ = set() # 大运地支关系
                for item in zhis2:
                
                    for type_ in zhi_atts[zhi2_]:
                        if type_ == '破':
                            continue
                        if item in zhi_atts[zhi2_][type_]:
                            zhi__.add(type_ + ":" + item)
                zhi__ = '  '.join(zhi__)
                
                empty = chr(12288)
                if zhi2_ in empties[ming.zhus[2]]:
                    empty = '空'       
                out = "{1:>3d} {2:<5d}{3} {15} {14} {13}  {4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<10s} {11}".format(
                    chr(12288), liunian.getAge(), liunian.getYear(), gan2_+zhi2_,ten_deities[ming.me][gan2_], gan2_,check_gan(gan2_, gans2), 
                    zhi2_, yinyang(zhi2_), ten_deities[ming.me][zhi2_], zhi6_, zhi__,empty, fu2, nayins[(gan2_, zhi2_)], ten_deities[ming.me][zhi2_]) 
                
                jia = ""
                if gan2_ in gans2:
                    for i in range(5):
                        if gan2_ == gans2[i]:
                            zhi1 = zhis2[i]
                            if abs(Zhi.index(zhi2_) - Zhi.index(zhis2[i])) == 2:
                                # print(2, zhi2_, zhis2[i])
                                jia = jia + "  --夹：" +  Zhi[( Zhi.index(zhi2_) + Zhi.index(zhis2[i]) )//2]
                            if abs( Zhi.index(zhi2_) - Zhi.index(zhis2[i]) ) == 10:
                                # print(10, zhi2_, zhis2[i])
                                jia = jia + "  --夹：" +  Zhi[(Zhi.index(zhi2_) + Zhi.index(zhis2[i]))%12]  

                            if (zhi1 + zhi2_ in gong_he) and (gong_he[zhi1 + zhi2_] not in ming.zhis):
                                jia = jia + "  --拱：" + gong_he[zhi1 + zhi2_]
                                
                out = out + jia + get_shens(ming.gans, ming.zhis,ming.me, gan2_, zhi2_)
                all_zhis = set(zhis2) | set(zhi2_)
                if set('戌亥辰巳').issubset(all_zhis):
                    out = out + "  天罗地网：戌亥辰巳"
                if set('寅申巳亥').issubset(all_zhis) and len(set('寅申巳亥')&set(ming.zhis)) == 2 :
                    out = out + "  四生：寅申巳亥"   
                if set('子午卯酉').issubset(all_zhis) and len(set('子午卯酉')&set(ming.zhis)) == 2 :
                    out = out + "  四败：子午卯酉"  
                if set('辰戌丑未').issubset(all_zhis) and len(set('辰戌丑未')&set(ming.zhis)) == 2 :
                    out = out + "  四库：辰戌丑未"             
                print(out)
                
            
        
        # 计算星宿
        d2 = datetime.date(1, 1, 4)
        print("星宿", ming.lunar.getXiu(), ming.lunar.getXiuSong())
        
        # 计算建除
        seq = 12 - Zhi.index(ming.zhis.month)
        print(jianchus[(Zhi.index(ming.zhis.day) + seq)%12])      