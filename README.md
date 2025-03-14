# 🚇 서울 지하철 혼잡도 빅데이터 분석  

![서울 지하철](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Seoul_Subway_Lines.svg/800px-Seoul_Subway_Lines.svg.png)  

## 📌 프로젝트 개요  
서울 지하철의 혼잡도를 분석하고 이를 웹 서비스로 시각화한 프로젝트입니다.  
Django를 활용한 웹 애플리케이션과 Tableau를 이용한 시각화를 통해 데이터를 효과적으로 제공하는 것을 목표로 했습니다.  

## 🛠 기술 스택  
- **프레임워크 & 백엔드**: Django, Python  
- **데이터 분석 & 시각화**: Pandas, Tableau  
- **프론트엔드**: HTML, CSS, JavaScript  
- **데이터 소스**: 서울교통공사(열차 혼잡도 데이터), Open Data API  

---

## 📊 데이터 분석 과정  
1. **데이터 수집**:  
   - 서울시 공공데이터 포털에서 혼잡도 관련 데이터를 수집  
   - API를 활용하여 실시간 및 과거 데이터 확보  

2. **데이터 전처리**:  
   - 결측치 처리 및 데이터 정제  
   - 날짜 및 시간별 혼잡도 변환  

3. **시각화 (Tableau 활용)**:  
   - 노선별/시간대별 혼잡도 대시보드 제작  
   - 사용자별 맞춤형 데이터 필터링 기능 추가  

4. **웹 서비스 개발 (Django 활용)**:  
   - 혼잡도 데이터를 Django로 처리하여 웹에 제공  
  
---

## 🎥 주요 기능  
✅ **서울 지하철 혼잡도 실시간 조회**  
✅ **노선별/시간대별 혼잡도 시각화 (Tableau 대시보드 연동)**  
✅ **사용자 위치 기반 혼잡도 예측 제공**  


---

## 🔧 실행 방법  

1. `cd mysite`
2. `python -m venv venv`
3. `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `set DJANGO_SETTINGS_MODULE=mysite.settings`
6. `python.exe -m pip install --upgrade pip`
7. `pip install django-tinymce`
8. `python manage.py makemigrations`
9. `python manage.py runserver`


``` PS C:\Project\teamtwo\django> cd mysite
PS C:\Project\teamtwo\django\mysite> python manage.py runserver
Watching for file changes with StatReloader
Exception in thread django-main-thread:
Traceback (most recent call last):

ModuleNotFoundError: No module named 'tinymce'
오류가 뜰 경우 pip install django-tinymce 적기
