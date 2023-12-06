def nomalize_subwayline(dataframe) :
    '''
    엑셀 데이터셋에서 호선명이 흔히 아는 지하철노선도의 호선명으로 표기되어있지 않아, 고치는 함수입니다.
    예를 들어 1호선은 '경부선', '경원선', '경인선', '장항선', '1호선'으로 나누어져 있어서 이를 모두 1호선으로 고쳤습니다.
    '''
    dataframe = dataframe.replace({'호선명':['경부선', '경원선', '경인선', '장항선']},'1호선')
    dataframe = dataframe.replace({'호선명':'일산선'}, '3호선')
    dataframe = dataframe.replace({'호선명':['안산선', '과천선']}, '4호선')
    dataframe = dataframe.replace({'호선명': ['경의선', '중앙선']}, '경의중앙선')
    return dataframe

def nomalize_subwayline2(dataframe) :
    '''
    2호선에서 최근 바뀐 이름들을 정규화하는 함수입니다.
    예를 들면 삼성역은 과거에는 '삼성'으로, 최근에는 '삼성(무역센터)'로 표기되어 있어 모두 '삼성'으로 통일하였습니다.
    '''
    dataframe = dataframe.replace({'지하철역' : ['충정로', '충정로(경기대입구)']}, '충정로')
    dataframe = dataframe.replace({'지하철역' : ['동대문역사문화공원', '동대문역사문화공원(DDP)']}, '동대문역사문화공원')
    dataframe = dataframe.replace({'지하철역' : ['왕십리', '왕십리(성동구청)']}, '왕십리')
    dataframe = dataframe.replace({'지하철역' : ['용두', '용두(동대문구청)']}, '용두')
    dataframe = dataframe.replace({'지하철역' : ['구의', '구의(광진구청)']}, '구의')
    dataframe = dataframe.replace({'지하철역' : ['강변', '강변(동서울터미널)']},'강변' )
    dataframe = dataframe.replace({'지하철역' : ['잠실', '잠실(송파구청)']}, '잠실')
    dataframe = dataframe.replace({'지하철역' : ['삼성', '삼성(무역센터)']}, '삼성')
    dataframe = dataframe.replace({'지하철역' : ['교대', '교대(법원.검찰청)']}, '교대')
    dataframe = dataframe.replace({'지하철역' : ['낙성대', '낙성대(강감찬)']}, '낙성대')
    dataframe = dataframe.replace({'지하철역' : ['서울대입구', '서울대입구(관악구청)']}, '서울대입구')
    dataframe = dataframe.replace({'지하철역' : ['대림', '대림(구로구청)']}, '대림')
    return dataframe

def get_selectlist():
    '''
    엑셀 데이터셋에서 '04~05시 승차인원', '04~05시 하차인원' 등으로 칼럼명이 표시되어 있어서 
    해당 행을 선택하기 위해 행 이름 리스트를 만드는 함수입니다.
    '''
    lst = []
    hour_list = ['04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
     '21', '22', '23', '24', '00', '01', '02', '03', '04']
    for i in range(len(hour_list)) :
        try :
            lst.append(hour_list[i] +'시-' + hour_list[i+1] +'시 승차인원')
            lst.append(hour_list[i] + '시-' + hour_list[i+1] + '시 하차인원')
        except :
            pass
    lst.remove('24시-00시 승차인원')
    lst.remove('24시-00시 하차인원')
    return lst