from django.apps import AppConfig
from .views import fetch_courses_and_teachers  # 引入爬取資料的函式
import threading  # 用於非同步執行

class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'
    has_run = False  # 新增一個類別變數作為旗標

    def ready(self):
        if not WebConfig.has_run:  # 檢查是否已經執行過
            WebConfig.has_run = True
            print("開始爬取指定學期資料...")
            semesters = ["113,2  ", "113,1  ", "112,2  ", "112,1  ", "111,2  "]  # 定義要爬取的學期
            for semester in semesters:
                threading.Thread(target=fetch_courses_and_teachers, args=(semester,)).start()
