from datetime import datetime
import openpyxl
import pymysql as pymysql
from psycopg2.extensions import AsIs
import os
import re

filename = "GoogleFontsList_KR.xlsx"
book = openpyxl.load_workbook(filename)
data = []
id = 0
created = datetime.now()
modified = datetime.now()

# listdir() 해당 경로의 파일을 리스트로 변환
font_folder = 'rocket_font_unicode'
fonts = os.listdir(font_folder)
print(fonts)

# db연결
db = pymysql.connect(host='main-server.rocketfont.net', port=3306, user='super', passwd='Rocket@Font1', db='rocket_font_main_db', charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor, ssl={"fake_flag_to_enable_tls":True})
cursor = db.cursor()

for font in fonts:
    print(font)
    file = open('./rocket_font_unicode/'+font, 'r')
    font_unicode = file.read()
    unicode_list = []
    unicode_list = re.findall(r'\d+', font_unicode)
    font_name = font[:-4]
    font_sql = "SELECT font_srl from font where font_file_name = %s"
    cursor.execute(font_sql, (font_name))
    print()
    font_srl = cursor.fetchall()[0]['font_srl']
    print(font_srl)
    for unicode in unicode_list:
        id += 1
        unicode_sql = "("+str(font_srl)+", "+str(id)+", "+str(unicode)+", "+str(created)+", "+str(modified)+")"
        print(unicode_sql)

        unicode_sql_list = []
        unicode_sql_list.append(unicode_sql)

    sql = "INSERT INTO font_unicode (font_srl, font_unicode_srl, unicode, created, modified) VALUES %s"
    cursor.execute(sql, unicode_sql_list)

    cursor.execute("INSERT INTO font_unicode (font_srl, font_unicode_srl, unicode, created, modified) VALUES (...);", AsIs(unicode_sql_list))

# for sheet in book:
#     for row in sheet.iter_rows(min_row=2):
#         data.append([
#             row[0].value,
#             row[2].value,
#             row[3].value,
#             row[4].value,
#         ])
#
# for font_file_name, font_family_name, font_style, font_weight in data:
#     id += 1
#     sql = "INSERT INTO font (font_srl, font_file_name, font_family_name, font_style, font_weight, font_license_srl, font_copyright_srl, font_creator_srl, created, modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     cursor.execute(sql, (id, font_file_name, font_family_name, font_style, font_weight, 1, 1, 1, created, modified))

db.close()
