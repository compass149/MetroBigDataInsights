from django.shortcuts import render

def index(request):
    return render(request, 'intro/index.html')

def member(request):
    return render(request, 'intro/member.html',{'page_title': '팀원 소개 Page'})

def data_source(request):
    return render(request, 'intro/data_source.html',{'page_title': '활용 데이터'})

def data_processing(request):
    return render(request, 'intro/data_processing.html',{'page_title': '데이터 가공 및 처리 과정'})

def chart(request):
    return render(request, 'intro/chart.html',{'page_title': '지하철 혼잡도 차트'})

def conclusion(request):
    return render(request, 'intro/conclusion.html',{'page_title': '결론'})
