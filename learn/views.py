from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import quote
from django.http import HttpResponseRedirect
import random
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import time
import json
from .models import douban_book


# @login_required(login_url='/signup')
def search(request):
    if request.user.is_authenticated():
        return render(request, 'search.html')
    else:
        return HttpResponseRedirect('/signup')


def update_book(request):
    if request.method == 'POST':
        author = request.POST["author"]

        def search_book(author):
            hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
                   {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
                   {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

            def crawl(url, booklist=[]):
                headers = random.choice(hds)
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, "lxml")
                for x in soup.find_all('div', class_="info"):
                    title = x.a['title'].strip()
                    if title not in booklist:
                        booklist.append(title)
                        info = x.select(".pub")[0].string.strip()
                        if author not in info:
                            continue
                        rating = x.select(".rating_nums")
                        if rating:
                            rating = float(rating[0].string)
                        else:
                            continue
                        print(rating)
                        link = x.a['href']
                        douban_book.objects.get_or_create(title=title, info=info, rating=rating, link=link, author=author)
                nexturl = soup.find('span', class_="next").a
                if nexturl:
                    nexturl = nexturl['href']
                    time.sleep(random.choice(range(3)))
                    crawl('https://book.douban.com' + nexturl)
            url = "https://book.douban.com/subject_search?search_text=%s&cat=1001" % quote(
                author)
            crawl(url)
            # totallist.sort(key=lambda x: x[2], reverse=True)
            # 以list形式导入数据，但是会重复！
            # booklist = [Book(title=x[0], info=x[1], rating=x[2], douban_link=x[3]) for x in totallist]
            # Book.objects.bulk_create(booklist)

            # 直接下载excel
            # wb = Workbook()
            # ws = wb.active
            # ws.append(['书名', '相关信息', '评分', '豆瓣地址'])
            # for item in totallist:
            #     ws.append(item)
            # response = HttpResponse(content_type='application/vnd.ms-excel')
            # response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % quote(
            #     author)
            # wb.save(response)
            # return response

            # 取评分前十在网页显示
            # return totallist[:10]
        # return render(request, "search_result.html", {'totallist': json.dumps(search_book(author))})
        search_book(author)
        return HttpResponseRedirect('/search')


def show_result(request):
    if request.method == "POST":
        author = request.POST["author"]
        totallist = list(douban_book.objects.filter(author=author).order_by('-rating').values_list("title", "info", "rating", "link"))
        return render(request, "search_result.html", {'totallist': json.dumps(totallist)})
    else:
        print('no')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/search')
    return render(request, 'login.html')


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                return render(request, 'login.html')

            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect('/login')
    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return HttpResponseRedirect('/signup')
