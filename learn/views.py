from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import quote
from django.http import HttpResponse, HttpResponseRedirect
import random
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import time


# @login_required(login_url='/signup')
def search(request):
    if request.user.is_authenticated():
        return render(request, 'search.html')
    else:
        return HttpResponseRedirect('/signup')


def download(request):
    if request.method == 'POST':
        author = request.POST["author"]

        def search_book(author, totallist=[]):
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
                        rating = x.select(".rating_nums")
                        if rating:
                            rating = float(rating[0].string)
                        else:
                            rating = 0
                        print(rating)
                        link = x.a['href']
                        totallist.append([title, info, rating, link])
                nexturl = soup.find('span', class_="next").a
                if nexturl:
                    nexturl = nexturl['href']
                    time.sleep(random.choice(range(3)))
                    crawl('https://book.douban.com' + nexturl)
            url = "https://book.douban.com/subject_search?search_text=%s&cat=1001" % quote(
                author)
            crawl(url)
            totallist.sort(key=lambda x: x[2], reverse=True)
            wb = Workbook()
            ws = wb.active
            ws.append(['书名', '相关信息', '评分', '豆瓣地址'])
            for item in totallist:
                ws.append(item)
            # response = HttpResponse(content_type='application/vnd.ms-excel')
            # response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % quote(
            #     author)
            # wb.save(response)
            return response
        return search_book(author)


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
