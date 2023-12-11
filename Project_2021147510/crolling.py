import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

# 셀레니움 드라이버 생성
driver = webdriver.Chrome()
usr = "kjeiun@yonsei.ac.kr"
pwd = "010525kk!!"

driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
time.sleep(5)

# 로그인이 필요한 데이터를 가져오므로 user emai과 password를 임의의로 넣음.
login_id = driver.find_element(By.CSS_SELECTOR, "input#user_email")
login_id.send_keys(usr)
login_pwd = driver.find_element(By.CSS_SELECTOR, "input#user_password")
login_pwd.send_keys(pwd)

login_id.send_keys(Keys.RETURN)
time.sleep(5)

company_list = pd.read_excel('Company1000.xlsx').to_dict('records')

#!! 아래 주석 처리 된 부분은 company list를 받아오는 부분이고, 실제로 xlsx파일은 data부분에 추가되었기 때문에
# read excel으로 불러오는 부분으로 대체하였습니다.
# 실제 코드를 돌리실 때에는 기존에 저장된 company1000.xlsx파일을 이용하셔서 id를 바탕으로 주석처리된 부분은
# 사용하지 않으시고 돌리시면됩니다!!

# # 첫 번째 페이지부터 100페이지까지 순회
# for page_num in range(1, 101):

#     # 모든 페이지에 대해서 회사의 이름과 id 쌍을 얻기
#     # 웹 페이지 열기
#     url = f'https://www.jobplanet.co.kr/companies?sort_by=review_survey_total_avg_cache&page={page_num}'
#     driver.get(url)

#     # 웹 페이지가 로딩될 때까지 기다리기 (예: 5초 기다림)
#     driver.implicitly_wait(5)

#     # HTML 가져오기
#     html = driver.page_source

#     # Beautiful Soup을 사용하여 HTML 파싱
#     soup = BeautifulSoup(html, 'html.parser')

#     # 회사 id와 이름을 가지고 있는 element 찾기
#     a_element = soup.select(
#         '#listCompanies > div > div.section_group > section > div > div > dl.content_col2_3.cominfo > dt > a')

#     print(f'Page {page_num}, len: {len(a_element)}')

#     # 특정 회사의 name 과 id를 company_list 에 넣고 엑셀에 저장
#     for i in range(len(a_element)):
#         company_name = a_element[i].get_text(strip=True)
#         # print(company_name)
#         company_id_href = a_element[i]['href']
#         company_id = company_id_href.split('/')[2]
#         company_list.append(
#             {'Company Name': company_name, 'Company ID': company_id})
#     df = pd.DataFrame(company_list)
#     df.to_excel('Company1000.xlsx', index=False)

# 회사 id와 이름 이외에 구체적인 데이터를 담고 있는 list
totals = []

# company_list 에 있는 모든 company에 대하여 특정 기업의 별점정보와 연봉 입사 인원/ 퇴사인원 정보를 모두 딕셔너리 형태로 담은 list
count = 0

for company in company_list:

    try:
        count = count+1
        print(count)
        company_id = str(company['Company ID'])
        company_name = company['Company Name']
        driver.get('https://www.jobplanet.co.kr/companies/' +
                   company_id+'/reviews/')
        html = driver.page_source
        # Beautiful Soup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')
        point_list = soup.select(
            '#premiumReviewStatistics > div > div.review_stats_container > div > div.stats_smr_sec.left_sec > div.rate_bar_set.barfill.total > div > div > div.rate_bar_unit > span.txt_point')
        p1 = point_list[0].text
        p2 = point_list[1].text
        p3 = point_list[2].text
        p4 = point_list[3].text
        p5 = point_list[4].text
        driver.get('https://www.jobplanet.co.kr/companies/' +
                   company_id+'/salaries/')
        html = driver.page_source
        # Beautiful Soup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')
        salary = soup.select_one(
            '#sideContents > div:nth-child(3) > div > div:nth-child(1) > div.txt_rgt > div.num > em').text
        in_num = soup.select_one(
            '#sideContents > div:nth-child(3) > div > div:nth-child(2) > div.num > em').text
        out_num = soup.select_one(
            '#sideContents > div:nth-child(3) > div > div:nth-child(3) > div.num > em').text
        if (count % 10 == 0):
            df2 = pd.DataFrame(totals)
            df2.to_excel('testjobPlanetData'+str(count)+'.xlsx')
            print(str(count)+'th data 파일이 저장되었습니다!')

    # 혹시나 특정 회사에 해당 정보가 없어서 에러가 나는 경우 처리를 하기 위한 except문
    except Exception as e:
        print('Err occurs in'+company_name)
        print(e)
        salary = 'no info'
        in_num = 'no info'
        out_num = 'no info'

        if (count % 10 == 0):
            df2 = pd.DataFrame(totals)
            df2.to_excel('jobPlanetData'+str(count)+'.xlsx')
            print(str(count)+'th data 파일이 저장되었습니다!')

    totals.append(
        {'Company Name': company_name, 'Company ID': company_id, '복지 및 급여': p1, '업무와 삶의 균형': p2, '사내문화': p3, '승진 기회 및 가능성': p4, '경영진': p5, '연봉': salary, '입사자 수': in_num, '퇴사자 수': out_num})


# 데이터프레임 생성

df = pd.DataFrame(totals)

# 엑셀 파일로 저장
df.to_excel('jobplanet_data.xlsx', index=False)

# 셀레니움 드라이버 종료
driver.quit()
