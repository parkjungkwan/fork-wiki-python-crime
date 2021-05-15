import pandas as pd
cctv = pd.read_csv('./CCTV.csv', encoding='utf-8')
cctv.head() # 최 상단의 5개의 로우만 출력
cctv_meta = cctv.columns
cctv_meta
"""
Index(['기관명', '소계',  # feature
'2013년도 이전',
'2014년',
'2015년',
'2016년'], dtype='object')
"""
cctv.rename(columns={cctv.columns[0]: '구별'}, inplace=True)
# inplace=True 는 실제 변수의 내용
cctv.head()

# import xlrd
pop = pd.read_excel('./POP.xls',encoding='utf-8',header=2,usecols='B,D,G,J,N')
pop.head()

# DF
pop.rename(columns={
     pop.columns[0] : '구별',
     pop.columns[1] : '인구수',
     pop.columns[2] : '한국인',
     pop.columns[3] : '외국인',
     pop.columns[4] : '고령자'
    },inplace=True)
pop.head()
import numpy as np
cctv.sort_values(by='소계', ascending=True)
# 0번행 삭제
pop.drop([0],inplace=True)
pop.head()
pop['구별'].unique() # 중복제거
pop[pop['구별'].isnull()] # null 체크

# *********
# 외국인비율과 고령자비율 계산
# *********
pop['외국인비율'] = pop['외국인'] / pop['인구수'] * 100
pop['고령자비율'] = pop['고령자'] / pop['인구수'] * 100
pop.head()
pop.sort_values(by='인구수', ascending=True)

# *********
# CCTV데이터와 인구현황 데이터 합치기(Merge)
# *********
data_result = pd.merge(cctv, pop, on='구별')
data_result.head()

# 행방향 삭제는 drop
# 열방향 삭제는 del
del data_result['2013년도 이전']
del data_result['2014년']
del data_result['2015년']
del data_result['2016년']
# 그래프를 그리기 위해 구이름을 index 로 설정
data_result.set_index('구별',inplace=True)
data_result.head()
# 상관관계
# - 상관계수 절대값이 0.1 이하면 거의 무시
# - 상관계수 절대값이 0.3 이하면 약한 상관관계
# - 상관계수 절대값이 0.5 이하면 중립
# - 상관계수 절대값이 0.7 이상이면 강한 상관관계
np.corrcoef(data_result['고령자비율'],data_result['소계'])
np.corrcoef(data_result['외국인비율'],data_result['소계'])
data_result.sort_values(by='인구수', ascending=True).head()

data_result.to_csv('./data_result.csv')