import json
import pymysql as pymysql
from datetime import datetime
import re

# db연결
db = pymysql.connect(host='main-server.rocketfont.net', port=3306, user='super', passwd='Rocket@Font1', db='rocket_font_main_db', charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor, ssl={"fake_flag_to_enable_tls":True})
cursor = db.cursor()

# 입력 데이터 정의
input_fontFileName = ""
input_fontFamilyName = ""
input_fontStyle = ""
input_fontWeight = ""
input_fontName = ""
today = datetime.now()
modified = today

input_fontFileName = input('추가할 웹폰트의 이름을 입력하세요: ')
font_face = input('추가할 웹폰트의 json 소스를 입력하세요: ')
# 임시 데이터
font_face = '''{
  "font-family": "LotteMartHappy",
  "font-style": "normal",
  "font-weight": 400,
  "src": "url('//cdn.jsdelivr.net/korean-webfonts/1/corps/lottemart/LotteMartHappy/LotteMartHappyMedium.woff2') format('woff2'), url('//cdn.jsdelivr.net/korean-webfonts/1/corps/lottemart/LotteMartHappy/LotteMartHappyMedium.woff') format('woff')"
}'''
input_unicode = input('추가할 웹폰트의 유니코드를 입력하세요: ')
unicode_list = []
unicode_list = re.findall(r'\d+', input_unicode)

font_face_json = json.loads(font_face)
input_fontFamilyName = font_face_json["font-family"]
input_fontWeight = font_face_json["font-weight"]
input_fontStyle = font_face_json["font-style"]

# font_srl 추출
sql = "SELECT font_srl from font where font_file_name = %s"
cursor.execute(sql, (input_fontFileName))
Font_srl = cursor.fetchall()[0]['font_srl']

# 폰트 중복여부 판별
sql = "select EXISTS (select * from font where font_file_name=%s) as success;"
cursor.execute(sql, (input_fontFileName))
isExist = cursor.fetchall()[0]['success']

# 같은 이름의 폰트가 없으면
if isExist == 0:
     print(input_fontStyle)
     created = today
     # sql = "INSERT INTO font (font_srl, font_file_name, font_family_name, font_style, font_weight, font_license_srl, font_copyright_srl, font_creator_srl, created, modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
     # cursor.execute(sql, (cursor.lastrowid, input_fontFileName, input_fontFamilyName, input_fontStyle, input_fontWeight, 1, 1, 1, Created, Modified))

     for Unicode in unicode_list:
          Font_unicode_srl = cursor.lastrowid + 1


     sql = "INSERT INTO font_unicode (font_srl, ,font_unicode_srl, unicode, created, modified) VALUES (%s, %s, %s, %s, %s)"
     cursor.execute(sql, (Font_srl, Font_unicode_srl, Unicode, created, modified))


     print("1 record inserted, ID: ", cursor.lastrowid)

elif isExist == 1:
     ans = input("이미 존재하는 폰트입니다. 수정하시겠습니까?(Y/N): ")
     if ans == 'Y':
          Modified = today
          col_num = int(input("1: font_family_name, 2: font_file_name, 3: font_style, 4: font_weight\n변경할 열을 선택하세요: "))
          new_data = input("새로운 값을 입력하세요: ")
          if col_num == 1:
               sql = "UPDATE font SET font_family_name = %s, modified = %s WHERE font_file_name = %s"
               cursor.execute(sql, (new_data, today, input_fontFileName))
          elif col_num == 2:
               sql = "UPDATE font SET font_file_name = %s, modified = %s WHERE font_file_name = %s"
               cursor.execute(sql, (new_data, today, input_fontFileName))
          elif col_num == 3:
               sql = "UPDATE font SET font_style = %s, modified = %s WHERE font_file_name = %s"
               cursor.execute(sql, (new_data, today, input_fontFileName))
          elif col_num == 4:
               sql = "UPDATE font SET font_weight = %s, modified = %s WHERE font_file_name = %s"
               cursor.execute(sql, (new_data, today, input_fontFileName))

db.close()