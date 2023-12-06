import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import subway_modules
df = pd.read_csv('..//dataset//data1.csv', encoding='cp949', index_col = False)
pd.set_option('display.max_columns', 500)
plt.rc('font', family='Malgun Gothic')

df = subway_modules.nomalize_subwayline(df)
df = subway_modules.nomalize_subwayline2(df)
select_list = subway_modules.get_selectlist()

'''
subway_predict는 예측하는 방법이 맞았는지 검증하기 위해 만든 파일입니다.
연도별 1월~9월의 오전 8시 승차 인원을 바탕으로 10월의 오전 8시 승차 인원을 예측하여 그래프로 비교합니다.

'''
df_train = pd.DataFrame()

select = select_list[8]
station_list = ['강남', '강변', '건대입구', '교대', '구로디지털단지', '구의', '낙성대', '당산', '대림', '도림천', '동대문역사문화공원', '뚝섬', '문래', '방배', '봉천', '사당', '삼성', '상왕십리', '서울대입구', '서초', '선릉', '성수', '시청', '신답', '신당', '신대방', '신도림', '신림', '신설동', '신정네거리', '신촌', '아현', '양천구청', '역삼', '영등포구청', '왕십리', '용답', '용두', '을지로3가', '을지로4가', '을지로입구', '이대', '잠실', '잠실나루', '종합운동장', '충정로', '한양대', '합정', '홍대입구']

temp_dic = {}
for station in station_list :
    for i in range(1, 11) :
        temp_list = []
        for j in range(2015, 2023) :
            value = df.loc[(df['호선명'] == '2호선') &(df['지하철역'] == station) & (df['사용월'] == j*100 + i), select]
            temp_list.append(int(value.iloc[0]))
        temp_dic[i-1] = temp_list
    df_temp = pd.DataFrame(temp_dic)
    df_train = pd.concat([df_train, df_temp], axis=0)

featuers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
X_train = df_train[featuers]
y_train = df_train[9]
reg = LinearRegression().fit(X_train, y_train)
print('reg.score:', reg.score(X_train, y_train))

temp_dic = {}
for station in station_list :    
    temp_list = []
    for i in range(1, 10) : 
        value = df.loc[(df['호선명'] == '2호선') &(df['지하철역'] == station) & (df['사용월'] == 2023 * 100+ i), select]
        temp_list.append(int(value.iloc[0]))
    temp_dic[station] = temp_list

df_test = pd.DataFrame(temp_dic).transpose()   

X_test = df_test[featuers]
y_pred = reg.predict(X_test) 
y_true = {}
for station in station_list :     
    value = df.loc[(df['호선명'] == '2호선') &(df['지하철역'] == station) & (df['사용월'] == 2023 * 100+ 10), select]
    y_true[station] = int(value.iloc[0])

plt.plot(y_true.keys(), y_pred, label='예측값')
plt.plot(y_true.keys(), y_true.values(), label='실제값')
plt.xticks(rotation = 40)
plt.legend()
plt.title('2023 10월 08-09시 월별 승차 승객 수 예측값과 실제값 비교')
plt.show()