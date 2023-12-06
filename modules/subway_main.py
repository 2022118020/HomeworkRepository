#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import subway_modules


pd.set_option('display.max_columns', 500)
plt.rc('font', family='Malgun Gothic')


# In[32]:


def readInt() :
    '''
    메뉴에서 정수값으로 값을 받기에 필요한 함수입니다.
    유효한 정수값을 받을 때까지 반복합니다.
    '''
    flag = True
    while flag :
        val = input('Enter an integer: ')
        try :
            val = int(val)
            if 0 <= val <= 23 :
                return val
        except ValueError :
            print(val, 'is not an integer or not suitable ')

def hourToSelect(input_int, hour) :
    '''
    메뉴 2, 3번에서 사용자가 보기 원하는 시간대를 입력하면 select_list에서 선택할 수 있게 select 키로 바꿔주는 함수입니다.
    예를들어 '18시-19시 승차인원'을 보려면 select_list의 [28]번 리스트값을 봐야해서 28으로 바꿔주어야 합니다.
    또, '18-19시 하차인원'을 보려면 select_list의 [29]번 리스트 값을 봐야해서 29로 바꿔주어야 합니다.
    입력값은 시작시간으로 받습니다. 예를들어 '18-19시'를 보려면 18로 받습니다.
    input_int를 사용해 '승차인원'을 볼 건지 '하차인원'을 볼 건지 구분합니다.
    '''
    if input_int == 2 :
        return 2*(hour - 4)
    elif input_int == 3 :
        return 2*hour - 9



def showOnOffPopulation(df, select_list) :
    '''
    메인루프에서 메뉴 1번을 선택하면 실행하는 함수입니다.
    시간대별로 월별 승/하차 인원수를 보여줍니다.
    '''
    timeline = list()
    get_on_mean = list()
    get_off_mean = list()

    for i in range (1, len(select_list), 2) :
        timeline.append(select_list[i][:2])

    for select in select_list :
        print(df[['지하철역', select]].groupby('지하철역').mean().mean())
        result = df[['지하철역', select]].groupby('지하철역').mean().mean()
        if '승차' in select :
            get_on_mean.append(result)
        else :
            get_off_mean.append(result)

    plt.plot(timeline, get_on_mean, label='승차승객 수')
    plt.plot(timeline, get_off_mean, label='하차승객 수')
    plt.legend()
    plt.title('시간별 평균 지하철 월 승하차 인원 수')
    plt.show()




def showOnOffatHour(df, select, hour, input_int) :
    '''
    메인루프에서 2, 3번을 선택하면 실행되는 함수입니다.
    시간대별로 승/하차 인원 수가 많은 상위 10개역을 인원수와 함께 보여줍니다.
    '''
    df_temp = df[['지하철역', select]].groupby('지하철역').mean().sort_values(by = select, ascending=False).head(10).to_dict()
    if input_int == 2 :
        onoff= '승차'
    elif input_int == 3 :
        onoff = '하차' 
    x = list(df_temp[select].keys())
    y = list(df_temp[select].values())
    title = str(hour) + '시-' + str(hour+1) + '시 월별 지하철' + onoff + '인원'
    plt.bar(x, y, width=0.6, color='green')
    plt.xticks(rotation = 40)
    plt.title(title)
    plt.show()


def showPopulation(df, select_list, hour) :
    '''
    메인루프에서 4번을 선택하면 실행되는 함수입니다.
    시간대별로 승+하차 인원 수가 많은 상위 10개역을 인원수와 함께 보여줍니다.
    '''
    count = 4
    df_temp = df
    for i in range(0, len(select_list), 2) :
        j = i + 1
        df_temp[str(count) + '시'] = df_temp[select_list[i]] + df_temp[select_list[j]]    
        count +=1
        if count == 24 :
            count = 0
    
    select = str(hour) + '시'
    temp = df_temp[['지하철역', select]].groupby('지하철역').mean().sort_values(by = select, ascending=False).head(10).to_dict()
    x = list(temp[select].keys())
    y = list(temp[select].values())
    title = str(hour) + '시-' + str(hour+1) + '시 월별 지하철 승하차 인원'
    plt.bar(x, y, width=0.6, color='green')
    plt.xticks(rotation = 40)
    plt.title(title)
    plt.show()


def showMonthPopulation(df, input_month) :
    '''
    메인루프에서 5번을 선택하면 실행되는 함수입니다.
    해당 연/월에 승차 혹은 하차 인원 수가 많은 상위 20개역을 인원수와 함께 보여줍니다.
    '''
    try :
        input_month = int(input_month)
        df_temp = df.loc[df['사용월'] == input_month, select_list]
    except :
        print('올바르지 않은 값을 입력하였습니다.')
        return
    flat_values = df_temp.values.flatten()
    top_10_indices = np.argpartition(flat_values, -20)[-20:]
    for idx in top_10_indices:
        row_index, col_index = np.unravel_index(idx, df_temp.shape)
        value = df_temp.iat[row_index, col_index]
        row_name = df_temp.index[row_index]
        station_name = df.loc[row_name, '지하철역']
        col_name = df_temp.columns[col_index]
        print(f"역 이름: {station_name}, 시간대: {col_name}, 인원 수: {value}") 
      

def showPredict(df, select) :
    '''
    지하철 2호선의 2023년 11월의 승/하차 인원수를 예측합니다.
    사용자에게 원하는 시간대와 승/하차 인지를 메인루프에서 입력받고 진행합니다.
    ''' 
    station_list = ['강남', '강변', '건대입구', '교대', '구로디지털단지', '구의', '낙성대', '당산', '대림', '도림천', '동대문역사문화공원', '뚝섬', '문래', '방배', '봉천', '사당', '삼성', '상왕십리', '서울대입구', '서초', '선릉', '성수', '시청', '신답', '신당', '신대방', '신도림', '신림', '신설동', '신정네거리', '신촌', '아현', '양천구청', '역삼', '영등포구청', '왕십리', '용답', '용두', '을지로3가', '을지로4가', '을지로입구', '이대', '잠실', '잠실나루', '종합운동장', '충정로', '한양대', '합정', '홍대입구']
    #station_list는 2호선의 역입니다. 새로 생긴 잠실새내역은 제외했습니다.

    '''
    지하철 2호선의 연도별 1월~10월 승/하차인원 데이터로 11월 승/하차인원을 예측하는 트레이닝셋을 만드는 코드입니다.
    '''
    df_train = pd.DataFrame()
    temp_dic = {}
    for station in station_list :
        for i in range(1, 12) :
            temp_list = []
            for j in range(2015, 2023) :
                value = df.loc[(df['호선명'] == '2호선') &(df['지하철역'] == station) & (df['사용월'] == j*100 + i), select]
                temp_list.append(int(value.iloc[0]))
            temp_dic[i-1] = temp_list
        df_temp = pd.DataFrame(temp_dic)
        df_train = pd.concat([df_train, df_temp], axis=0)
    featuers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    X_train = df_train[featuers]
    y_train = df_train[10]
    
    reg = LinearRegression().fit(X_train, y_train)
    print('reg.score:', reg.score(X_train, y_train))
    #트레이닝 해주었습니다.
    
    '''
    지하철 2호선의 2023년 1~10월 승/하차인원 데이터로 2023년 11월 승/하차인원을 예측합니다.
    '''
    temp_dic = {}
    for station in station_list :    
        temp_list = []
        for i in range(1, 11) : 
            value = df.loc[(df['호선명'] == '2호선') &(df['지하철역'] == station) & (df['사용월'] == 2023 * 100+ i), select]
            temp_list.append(int(value.iloc[0]))
        temp_dic[station] = temp_list
    df_test = pd.DataFrame(temp_dic).transpose()
    X_test = df_test[featuers]
    y_pred = reg.predict(X_test) 
    y_pred
    for i in range (len(station_list)) :
        print('%s역 : %.2f명' % (station_list[i], y_pred[i]))

## --main

Input_flag = True 
df = pd.read_csv('..//dataset//data1.csv', encoding='cp949', index_col = False)
df = subway_modules.nomalize_subwayline(df)
df = subway_modules.nomalize_subwayline2(df)
select_list = subway_modules.get_selectlist()

while Input_flag :
    print('*********************************************')
    print('지하철에서 유동인구가 많은 역은 언제/어디인가?')
    print('*********************************************')
    print(' 1. 시간대 별 승/하차 인원 수 보기')
    print(' 2. 시간대 별 승차 인원이 많은 역 보기')  
    print(' 3. 시간대 별 하차 인원이 많은 역 보기')
    print(' 4. 시간대 별 승하차 합산 인원이 많은 역 보기')
    print(' 5. 유동인구가 많은 시간대/역 보기')
    print(' 6. 2023년 11월 2호선의 승하차인원수 예측하기')
    print(' 7. 종료')
    print('*********************************************')
    input_int = readInt()
    if input_int == 1 : showOnOffPopulation(df, select_list)
    elif input_int == 2 :
        print('원하는 시간대를 선택하여주세요.')
        print('(08시-09시 승차인원: 8, 18시-19시 승차인원: 18, 0시-1시 승차인원 : 0)')
        hour = readInt()
        select = hourToSelect(input_int, hour)
        showOnOffatHour(df, select_list[select], hour, input_int)
    elif input_int == 3 :
        print('원하는 시간대를 선택하여주세요.')
        print('(08시-09시 하차인원: 8, 18시-19시 하차인원: 18, 0시-1시 하차인원 : 0)')
        hour = readInt()
        select = hourToSelect(input_int, hour)
        showOnOffatHour(df, select_list[select], hour, input_int)
    elif input_int == 4 :
        print('원하는 시간대를 선택하여주세요.')
        print('(08시-09시 승하차인원: 8, 18시-19시 승하차인원: 18, 0시-1시 승하차인원 : 0)')
        hour = readInt()
        showPopulation(df, select_list, hour)
    elif input_int == 5 :
        print('원하는 연도/월을 선택하여주세요.')
        print('2015년 1월부터 2023년 10월까지의 데이터를 볼 수 있습니다.')
        print('(2015년 1월: 201501, 2023년 10월: 202310)')
        print('올바른 형식의 값을 입력하지 않으면 메인화면으로 돌아갑니다.')
        input_month = input('Enter an Integer: ')
        showMonthPopulation(df, input_month)
    elif input_int == 6 :
        print('원하는 시간대를 선택하여주세요.')
        print('(08시-09시 : 8, 18시-19시 : 18, 0시-1시: 0)')
        hour = readInt()
        print('승차인원을 원하면 2, 하차인원을 원하면 3을 반드시 2, 3 중 하나로 입력해주세요.')
        input_int = readInt()
        select = hourToSelect(input_int, hour)
        if input_int == 2 :
            input_int_string = '승차'
        elif input_int == 3 :
            input_int_string = '하차'
        print('2023년 11월 %d시 %s승객 수 예측'%(hour, input_int_string))
        showPredict(df, select_list[select])
        
        pass
    elif input_int == 7 :
        print('프로그램을 종료합니다')
        Input_flag = False
    else :
        pass

