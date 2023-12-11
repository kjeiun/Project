import pandas as pd

# 엑셀 파일에서 데이터 읽어오기
file_path = 'jobPlanetData700.xlsx'  # 파일 경로를 적절히 변경하세요
df = pd.read_excel(file_path)

# 'no info' 값을 NaN으로 변경하고 NaN이 있는 행 삭제
df.replace('no info', pd.NA, inplace=True)
df.dropna(subset=['연봉', '입사자 수', '퇴사자 수'], how='any', inplace=True)

# ','를 제거하여 숫자형으로 변환
df['연봉'] = df['연봉'].replace({',': ''}, regex=True).astype(int)
df['입사자 수'] = df['입사자 수'].replace({',': ''}, regex=True).astype(int)
df['퇴사자 수'] = df['퇴사자 수'].replace({',': ''}, regex=True).astype(int)

# '퇴사자수/(입사자수+퇴사자수)' 계산하여 새로운 열 추가
df['퇴사율'] = df.apply(lambda row: row['퇴사자 수'] / (row['입사자 수'] + row['퇴사자 수'])
                     if (row['입사자 수'] + row['퇴사자 수']) != 0 else 0, axis=1)

# 결과 확인
df.to_excel('after_preprocess.xlsx', index=False)
