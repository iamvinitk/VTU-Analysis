import xlwt
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import os


def grade(marks):
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 45:
        return 5
    elif marks >= 40:
        return 4
    else:
        return 0


# Change the subject code according to the semester (41 -> 4th Sem, 51 -> 5th Sem)
def start_index(subject_code):
    if '65' in subject_code:
        return (4 + 32), 3  # (Index of subject in html, Grade point for that subject)
    elif '66' in subject_code:
        return (4 + 40), 3
    elif '61' in subject_code:
        return 4, 4
    elif '62' in subject_code:
        return (4 + 8), 4
    elif '63' in subject_code:
        return (4 + 16), 4
    elif '64' in subject_code:
        return (4 + 24), 4
    elif '67' in subject_code:
        return (4 + 48), 2
    elif '68' in subject_code:
        return (4 + 56), 2


cwd = os.path.join(os.getcwd(), 'chromedriver.exe')
driver = webdriver.Chrome(cwd)
driver.implicitly_wait(10)
wb = xlwt.Workbook()
ws = wb.add_sheet('CSE')
k = 1
# Adding column titles
ws.write(0, 0, "USN")
ws.write(0, 1, "Name")
ws.write(0, 2, "SGPA")
ws.write(0, 3, "TotalGrade")
for i in range(0, 8):
    ws.write(0, 3 + (i * 8) + 1, "SC" + str(i + 1))
    ws.write(0, 3 + (i * 8) + 2, "SN" + str(i + 1))
    ws.write(0, 3 + (i * 8) + 3, "Internal" + str(i + 1))
    ws.write(0, 3 + (i * 8) + 4, "External" + str(i + 1))
    ws.write(0, 3 + (i * 8) + 5, "Total" + str(i + 1))
    ws.write(0, 3 + (i * 8) + 6, "Result" + str(i + 1))
    ws.write(0, 3 + (i * 8) + 7, "Grade" + str(i + 1))
    ws.write(0, 3 + (i * 8) + 8, "GradeTotal" + str(i + 1))

for usn in range(1, 10):
    try:
        lsn = '1MJ15IS' + str(usn).zfill(3)
        print('USN : ', lsn)
        driver.get("http://results.vtu.ac.in/vitaviresultcbcs2018/index.php")
        username = driver.find_element_by_name("lns")
        username.send_keys(lsn)
        username.send_keys(Keys.ENTER)

        html = driver.page_source.encode('utf-8')

        bs = BeautifulSoup(html, 'html.parser')
        div = bs.findAll("div", {"class": "divTableCell"}, text=True)
        table = bs.findAll("td")
        sem = bs.findAll('b')

        # Validate result to ensure that it belongs to the particular semester
        if sem[6].text == 'Semester : 6':
            total_grade = 0
            for m, value in enumerate(div[6:49:6]):
                start, grade_point = start_index(value.text)
                for n in range(0, 6):
                    print(m, div[((6 * (m + 1)) + n)].text)
                    ws.write(k, start + n, div[((6 * (m + 1)) + n)].text)
                ws.write(k, start + 6, str(grade(int(div[((6 * (m + 1)) + 4)].text))))
                total_grade += grade(int(div[((6 * (m + 1)) + 4)].text)) * grade_point
                ws.write(k, start + 7, str(grade(int(div[((6 * (m + 1)) + 4)].text)) * grade_point))
            print(table[3].text)
            ws.write(k, 0, table[1].text[3:])
            ws.write(k, 1, table[3].text[2:])
            ws.write(k, 2, str("{0:.2f}".format((total_grade / 26))))
            ws.write(k, 3, str(total_grade))
            print(total_grade)
            k += 1

    except NoAlertPresentException as e:
        continue
    except Exception as e:
        print(e)
        alert = driver.switch_to.alert
        alert.accept()

wb.save('result.xls')
