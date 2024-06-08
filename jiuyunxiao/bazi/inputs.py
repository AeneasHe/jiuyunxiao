import argparse
import collections
from lunar_python import Lunar, Solar
from datas import siling

from gets import getGZ
description = '''
$ python bazi.py -h
usage: bazi.py [-h] [-b] [-g] [-r] [-n] [--version] year month day time

positional arguments:
  year        year
  month       month
  day         day
  time        time

optional arguments:
  -h, --help  show this help message and exit
  -b          直接输入八字
  -g          是否采用公历
  -r          是否为闰月，仅仅使用于农历
  -w          是否为女women，默认为男man
  --version   show program's version number and exit

python main.py 1977 8 11 19 -w
'''

from mingzao import Ming


def get_input():
    parser = argparse.ArgumentParser(description=description,
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('year', action="store", help=u'year')
    parser.add_argument('month', action="store", help=u'month')
    parser.add_argument('day', action="store", help=u'day')
    parser.add_argument('time', action="store",help=u'time')    
    parser.add_argument("--start", help="start year", type=int, default=1850)
    parser.add_argument("--end", help="end year", default='2030')
    parser.add_argument('-b', action="store_true", default=False, help=u'直接输入八字')
    parser.add_argument('-g', action="store_true", default=False, help=u'是否采用公历')
    parser.add_argument('-r', action="store_true", default=False, help=u'是否为闰月，仅仅使用于农历')
    parser.add_argument('-w', action="store_true", default=False, help=u'是否为女，默认为男')
    parser.add_argument('--version', action='version',
                        version='%(prog)s 1.0 Rongzhong xu 2022 06 15')
    options = parser.parse_args()

    Gans = collections.namedtuple("Gans", "year month day time")
    Zhis = collections.namedtuple("Zhis", "year month day time")
    lunar = None

    print("-"*120)

   

    if options.b: # 直接输入八字
        import sxtwl
        gans = Gans(year=options.year[0], month=options.month[0], 
                    day=options.day[0],  time=options.time[0])
        zhis = Gans(year=options.year[1], month=options.month[1], 
                    day=options.day[1],  time=options.time[1])
        jds = sxtwl.siZhu2Year(getGZ(options.year), getGZ(options.month), getGZ(options.day), getGZ(options.time), options.start, int(options.end));
        for jd in jds:
            t = sxtwl.JD2DD(jd )
            print("可能出生时间: python bazi.py -g %d %d %d %d :%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))   
        
    else: 

        if options.g: # 公历
            solar = Solar.fromYmdHms(int(options.year), int(options.month), int(options.day), int(options.time), 0, 0)
            lunar = solar.getLunar()
        else: # 农历
            month_ = int(options.month)*-1 if options.r else int(options.month)
            lunar = Lunar.fromYmdHms(int(options.year), month_, int(options.day),int(options.time), 0, 0)
            solar = lunar.getSolar()

        day = lunar # 农历日期
        ba = lunar.getEightChar()  # 根据农历算出八字

        # 分别取出天干、地支
        gans = Gans(year=ba.getYearGan(), month=ba.getMonthGan(), day=ba.getDayGan(), time=ba.getTimeGan())
        zhis = Zhis(year=ba.getYearZhi(), month=ba.getMonthZhi(), day=ba.getDayZhi(), time=ba.getTimeZhi())

        #print("direction",direction)
        sex = '女' if options.w else '男'
        print("{}命".format(sex), end=' ')
        print("\t公历:", end=' ')
        print("{}年{}月{}日".format(solar.getYear(), solar.getMonth(), solar.getDay()), end=' ')
        
        yun = ba.getYun(not options.w)   
        print("  农历:", end=' ')
        print("{}年{}月{}日 穿=害 上运时间：{} 命宫:{} 胎元:{}\n".format(lunar.getYear(), lunar.getMonth(), 
            lunar.getDay(), yun.getStartSolar().toFullString().split()[0], ba.getMingGong(), ba.getTaiYuan()), end=' ')
        print("\t", siling[zhis.month], lunar.getPrevJieQi(True), lunar.getPrevJieQi(True).getSolar().toYmdHms(),lunar.getNextJieQi(True), 
            lunar.getNextJieQi(True).getSolar().toYmdHms())

    ming = Ming(gans,zhis,options.w,lunar)

    return ming