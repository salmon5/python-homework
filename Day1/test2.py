#Author: xiaoyu hao

'''实现功能
1.三级菜单
2.可依次选择进入各子菜单，并打印对应内容
'''

map_dict = \
    {'华东':
         {'上海市':['上海','浦东'],
          '江苏省':['南京'],
          '浙江省':['杭州'],
          '安徽省':['合肥'],
          '福建省':['福州'],
          '江西省':['南昌'],
          '山东省':['济南'],
          '台湾省':['台北']
          },
     '华北':
         {'北京市':['北京'],
          '天津市':['天津'],
          '山西省':['太原'],
          '河北省':['石家庄'],
          '内蒙古自治区中部':['呼和浩特']},
     '华中':
         {'河南省':['郑州'],
          '湖北省':['武汉'],
          '湖南省':['长沙']},
     '华南':
         {'广东省':['广州'],
          '广西壮族自治区':['桂林'],
          '海南省':['海口'],
          '香港特别行政区':['香港'],
          '澳门特别行政区':['澳门']},
     '西南':
         {'四川省':['成都'],
          '贵州省':['贵阳'],
          '云南省':['昆明'],
          '重庆市':['重庆'],
          '西藏自治区':['拉萨']},
     '西北':
         {'陕西省':['西安'],
          '甘肃省':['兰州'],
          '青海省':['西宁'],
          '宁夏回族自治区':['银川'],
          '新疆维吾尔自治区':['乌鲁木齐'],
          '内蒙古自治区西部':[]},
     '东北':
         {'黑龙江省':['哈尔滨'],
          '吉林省':['长春'],
          '辽宁省':['沈阳'],
          '内蒙古自治区东部':[]}
    }

num = 1
#字典转换列表
#打印所有的地理区域

def display():
    select_msg = '''
        --------------------------------------------------------------
                        中国七大地理地区分布查询系统
        1. 显示中国地理分布
        4. 退出（q/）
        --------------------------------------------------------------
    '''
    return select_msg

#ch_district = list(map_dict.items())
#print(ch_district)

city_index = [(index, key) for index, key in enumerate(map_dict)]

choose_dict = city_index[1][1]
city_map = map_dict[choose_dict]
print(choose_dict)
print(city_index)
print(type(map_dict[choose_dict]))


print("---------------------------------------------------------------------------")

for i in map_dict:
    print(i)
    for j in map_dict[i]:
        print(j)
