from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from django.shortcuts import render
import time
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import os

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 驗證表單數據
        if not username or not email or not password or not confirm_password:
            messages.error(request, '所有欄位皆為必填項！')
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, '密碼與確認密碼不一致！')
            return redirect('register')

        # 檢查用戶名是否存在
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM custom_users WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                messages.error(request, '該用戶名已被使用！')
                return redirect('register')

        # 插入新用戶（密碼加密）
        hashed_password = make_password(password)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO custom_users (username, email, password) VALUES (%s, %s, %s)",
                [username, email, hashed_password]
            )
        
        # 成功訊息
        messages.success(request, '註冊成功！請登入您的帳號。')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 查詢資料庫檢查用戶名和密碼
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password FROM custom_users WHERE username = %s", [username])
            user = cursor.fetchone()

            if not user:
                messages.error(request, '用戶名不存在！')
                return redirect('login')

            user_id, hashed_password = user
            if check_password(password, hashed_password):
                # 登錄成功
                request.session['user_id'] = user_id
                request.session['username'] = username
                messages.success(request, '登入成功！歡迎回來。')
                return redirect('login')
            else:
                messages.error(request, '密碼錯誤！')
                return redirect('login')

    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')
def evaluation_form(request):
    return render(request, 'evaluation_form.html')
def evaluation_list(request):
    return render(request, 'evaluation_list.html')
def course_bot(request):
    return render(request, 'course_bot.html')
def resume_generator(request):
    if request.method == 'POST':
        # 從用戶提交的表單中獲取數據
        context = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'education': request.POST.get('education'),
            'experience': request.POST.get('experience'),
            'skills': request.POST.get('skills'),
            'about': request.POST.get('about'),
        }
        # 你可以選擇將數據傳遞給下一個模板進行顯示
        return render(request, 'resume_preview.html', context)

    # 如果是 GET 請求，顯示輸入表單
    return render(request, 'resume_form.html')

from django.http import HttpResponse
def resume_download(request):
    # 這是一個佔位函數，用於測試
    return HttpResponse("Resume download functionality is not implemented yet.")

def evaluation_form(request):
    if request.method == 'POST':
        # 從 POST 請求中獲取表單提交的數據
        course = request.POST.get('course')
        instructor = request.POST.get('instructor')
        semester = request.POST.get('semester')
        content = request.POST.get('content', '')  # 默認值為空字符串，防止空值導致錯誤
        grading = request.POST.get('grading', '')
        assignments = request.POST.get('assignments', '')
        additional = request.POST.get('additional', '')
        recommendation = request.POST.get('recommendation')

        # 插入數據到資料庫
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO nmsl (course, instructor, semester, content, grading, assignments, additional, recommendation)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [course, instructor, semester, content, grading, assignments, additional, recommendation]
                )
        except Exception as e:
            # 如果插入失敗，打印錯誤並返回表單頁面
            print(f"資料插入失敗: {e}")
            return render(request, 'evaluation_form.html', {
                'error': '資料插入失敗，請檢查您的輸入是否正確',
                'courses_and_teachers': cache.get(f"courses_and_teachers_{semester}", []),
                'semester': semester
            })

        # 成功插入數據後，重定向到評價列表頁面
        return redirect('evaluation_list')

    else:
        # GET 請求：加載表單並加載動態課程數據
        semester = request.GET.get("semester", "113,2").strip()  # 預設學期為 "113,2"
        cache_key = f"courses_and_teachers_{semester}"  # 基於學期生成 Cache 鍵
        courses_and_teachers = cache.get(cache_key, [])  # 從 Cache 獲取課程與教師數據

        # 返回表單頁面，並傳遞課程和教師數據
        return render(request, "evaluation_form.html", {
            "courses_and_teachers": courses_and_teachers,
            "semester": semester
        })


def evaluation_list(request):
    # 從資料庫中抓取所有評價數據
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT course, instructor, semester, content, grading, assignments, additional, recommendation
            FROM nmsl
        """)
        rows = cursor.fetchall()

    # 整理數據到字典列表，方便模板使用
    evaluations = [
        {
            'course': row[0],
            'instructor': row[1],
            'semester': row[2],
            'content': row[3],
            'grading': row[4],
            'assignments': row[5],
            'additional': row[6],
            'recommendation': row[7],
        }
        for row in rows
    ]

    # 傳遞數據到模板
    return render(request, 'evaluation_list.html', {'evaluations': evaluations})



def fetch_courses_and_teachers(semester):
    print(f"開始爬取 {semester} 學期的課程與教師資料...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver_path = os.getenv("CHROMEDRIVER_PATH", "").strip()
    driver = (
        webdriver.Chrome(service=Service(driver_path), options=options)
        if driver_path
        else webdriver.Chrome(options=options)
    )
    courses_and_teachers = []

    try:
        url = "https://portalfun.yzu.edu.tw/cosSelect/index.aspx?D=G"
        driver.get(url)

        # 選擇學期
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "DDL_YM")))
        Select(driver.find_element(By.ID, "DDL_YM")).select_by_value(semester)
        time.sleep(2)

        # 選擇其他下拉選單（資工系、全部年級）
        Select(driver.find_element(By.ID, "DDL_Dept")).select_by_value("304")
        time.sleep(2)
        Select(driver.find_element(By.ID, "DDL_Degree")).select_by_value("0")
        time.sleep(2)

        # 點擊提交按鈕
        driver.find_element(By.ID, "Button1").click()
        time.sleep(3)

        # 解析網頁
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        for tr in soup.find_all("tr", class_="record2"):
            course_td = tr.find("td", {"title": "查詢學程"})
            teacher_td = tr.find("td", {"title": "教師簡介"})
            if course_td and teacher_td:
                course_name = course_td.find("a").text.strip()
                teacher_name = teacher_td.find("a").text.strip()
                courses_and_teachers.append({"course": course_name, "teacher": teacher_name})
        for tr in soup.find_all("tr", class_="hi_line"):
            course_td = tr.find("td", {"title": "查詢學程"})
            teacher_td = tr.find("td", {"title": "教師簡介"})
            if course_td and teacher_td:
                course_name = course_td.find("a").text.strip()
                teacher_name = teacher_td.find("a").text.strip()
                courses_and_teachers.append({"course": course_name, "teacher": teacher_name})

        # 存入 Cache，使用學期區分
        cache_key = f"courses_and_teachers_{semester.strip()}"
        cache.set(cache_key, courses_and_teachers, timeout=None)
        print(f"爬取完成！{semester} 學期資料已儲存到 Cache。")

    except Exception as e:
        print(f"爬取過程中發生錯誤: {e}")
    finally:
        driver.quit()
