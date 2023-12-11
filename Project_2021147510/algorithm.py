import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns  # heatmap 만들기 위한 라이브러리
import matplotlib.font_manager as fm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 데이터 불러오기
company_data = pd.read_excel("after_preprocess.xlsx")
cause_data = company_data.drop(['복지 및 급여'], axis=1)

# 1. 다중 선형회귀분석

x_data = company_data[["복지 및 급여", "사내문화",
                       "승진 기회 및 가능성", "경영진", "퇴사율"]]  # 변수 여러개, # target에 대하여 원인을 따질 데이터
target = company_data[["업무와 삶의 균형"]]
x_data1 = sm.add_constant(x_data, has_constant="add")  # for b0, 상수항 추가
# 다중공산성이 높은 경영진은 제거
x_data1 = x_data1.drop("경영진", axis=1)

multi_model = sm.OLS(target, x_data1)  # OLS 검정
fitted_multi_model = multi_model.fit()
results = fitted_multi_model

# 회귀분석 결과를 데이터프레임으로 저장
result_df = pd.DataFrame(fitted_multi_model.summary(
).tables[1].data[1:], columns=fitted_multi_model.summary().tables[1].data[0])
result_df.set_index('coef', inplace=True)

result_path = 'regression_results_cleaned.xlsx'  # 결과를 엑셀 파일로 저장
result_df.to_excel(result_path)


# 2-1. 상관행렬 시각화
plt.rcParams['font.family'] = 'AppleGothic'  # 폰트를 설정해줘야 한글이 깨지지 않음
cmap = sns.light_palette("darkgray", as_cmap=True)
sns.heatmap(x_data1.corr(), annot=True, cmap=cmap)
plt.show()
plt.savefig('corr_heatmap.png')

# 2-2. 변수끼리 산점도를 시각화
sns.pairplot(x_data1)
plt.show()
plt.savefig('scatter.png')

# 3. VIF를 이용한 다중공산성 체크 , x_data1에서 다중공산성이 높은 데이터는 제거하고 다시 실행
vif = pd.DataFrame()


vif["VIF Factor"] = [variance_inflation_factor(
    x_data1.values, i) for i in range(x_data1.shape[1])]
vif["features"] = x_data1.columns

print(vif)
