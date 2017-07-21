from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
import markdown2
from django.db import models
from .models import User, Library, Information, Article, Contact
from django.views.generic.list import ListView
from .forms import BlogCommentForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView


# Create your views here.
# 表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


# 注册
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # 获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 添加到数据库
            check = User.objects.filter(username__exact=username)
            if check:
                return HttpResponseRedirect('/check/')
            else:
                User.objects.create(username=username, password=password)
                return HttpResponseRedirect('/jump/')
     #       else:
     #           return error_msg


    else:
        uf = UserForm()
    return render_to_response('user/regist.html', {'uf': uf}, context_instance=RequestContext(req))


# 登陆
def login(req):
    if req.method == 'POST':

        uf = UserForm(req.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/loginsuccess')
                # 将username写入浏览器cookie
                response.set_cookie('username', username)
                return response
            else:
                # 比较失败，还在login
                return HttpResponseRedirect('/logfail')
    else:
        uf = UserForm()
    return render_to_response('user/login.html', {'uf': uf}, context_instance=RequestContext(req))



# 登陆成功
def index(req):
    a_username = req.COOKIES.get('username')
    title_list = User.objects.filter(username__exact=a_username)[0:1]
    return render_to_response('index.html', {'title_list': title_list})


# 退出
def logout(req):
    response = render_to_response('user/logout.html')
    # 清理cookie里保存username
    response.delete_cookie('username')
    return response


def personal(request):
    b_username = request.COOKIES.get('username')
    title_list = User.objects.filter(username__exact=b_username)[0:1]

    if request.method == 'POST':
        a_user = request.POST['user']
        a_duty_id = request.POST['duty_id']
        a_ship_age = request.POST['ship_age']
        a_company_name = request.POST['company_name']
        a_duty = request.POST['duty']
        a_certificate_level = request.POST['certificate_level']
        a_special_certificate = request.POST.get('special_certificate', False)
        a_route_area = request.POST.get('route_area', False)
        a_recruitment_ship = request.POST.get('recruitment_ship', False)
        a_tonnage = request.POST.get('tonnage', False)
        a_time = request.POST.get('time', False)

        userinformation = User.objects.get(username=a_user)
        userinformation.duty_id = a_duty_id
        userinformation.ship_age = a_ship_age
        userinformation.company_name = a_company_name
        userinformation.duty = a_duty
        userinformation.certificate_level = a_certificate_level
        userinformation.special_certificate = a_special_certificate
        userinformation.route_area = a_route_area
        userinformation.recruitment_ship = a_recruitment_ship
        userinformation.tonnage = a_tonnage
        userinformation.time = a_time
        userinformation.save()

    user_list = User.objects.all()
    return render_to_response('user/personal.html', {'user_list': user_list, 'title_list': title_list})


def jump(req):
    return render_to_response('user/jump.html')


def logfail(req):
    return render_to_response('user/logfail.html')


def loginsuccess(req):
    return render_to_response('user/loginsuccess.html')

def check(req):
    return render_to_response('user/check.html')


def search(request):
    b_username = request.COOKIES.get('username')
    title_list = User.objects.filter(username__exact=b_username)[0:1]

    search_ship_age = request.GET.get('search_ship_age')
    search_duty = request.GET.get('search_duty')
    search_duty_id = request.GET.get('search_duty_id')
    search_company_name = request.GET.get('search_company_name')
    search_certificate_level = request.GET.get('search_certificate_level')
    search_special_certificate = request.GET.get('search_special_certificate')
    search_route_area = request.GET.get('search_route_area')
    search_recruitment_ship = request.GET.get('search_recruitment_ship')
    search_tonnage = request.GET.get('search_tonnage')
    search_time = request.GET.get('search_time')

    Information.objects.create(
        ship_age=search_ship_age,
        duty=search_duty,
        duty_id=search_duty_id,
        company_name=search_company_name,
        certificate_level=search_certificate_level,
        special_certificate=search_special_certificate,
        route_area=search_route_area,
        recruitment_ship=search_recruitment_ship,
        tonnage=search_tonnage,
        time=search_time
    )

    information_list = Information.objects.filter(ship_age__exact=search_ship_age,
                                                  duty__exact=search_duty,
                                                  duty_id__exact=search_duty_id,
                                                  company_name__exact=search_company_name,
                                                  certificate_level__exact=search_certificate_level,
                                                  special_certificate__exact=search_special_certificate,
                                                  route_area__exact=search_route_area,
                                                  recruitment_ship__exact=search_recruitment_ship,
                                                  tonnage__exact=search_tonnage,
                                                  time__exact=search_time
                                                  )[0:1]

    request.session["ship_age"] = search_ship_age
    request.session["duty"] = search_duty
    request.session["duty_id"] = search_duty_id
    request.session["company_name"] = search_company_name
    request.session["certificate_level"] = search_certificate_level
    request.session["special_certificate"] = search_special_certificate
    request.session["route_area"] = search_route_area
    request.session["recruitment_ship"] = search_recruitment_ship
    request.session["tonnage"] = search_tonnage
    request.session["time"] = search_time
    #response.set_cookie('duty', search_duty)
    #response.set_cookie('duty_id', search_duty_id)
    #response.set_cookie('company_name', search_company_name)
    #response.set_cookie('certificate_level', search_certificate_level)
    #response.set_cookie('search_special_certificate', search_special_certificate)
    #response.set_cookie('route_area', search_route_area)
    #response.set_cookie('recruitment_ship', search_recruitment_ship)
    #response.set_cookie('tonnage', search_tonnage)
    #response.set_cookie('time', search_time)

    return render_to_response('recruit/search.html', {'information_list': information_list,
                                                      'title_list': title_list})


def search_detail(request):
    b_username = request.COOKIES.get('username')
    title_list = User.objects.filter(username__exact=b_username)[0:1]

    search_ship_age = request.session.get('ship_age')
    search_duty = request.session.get('duty')
    search_duty_id = request.session.get('duty_id')
    search_company_name = request.session.get('company_name')
    search_certificate_level = request.session.get('certificate_level')
    search_special_certificate = request.session.get('special_certificate')
    search_route_area = request.session.get('route_area')
    search_recruitment_ship = request.session.get('recruitment_ship')
    search_tonnage = request.session.get('tonnage')
    search_time = request.session.get('time')
  #  search_ship_age = request.GET.get('search_ship_age')
 #   search_duty = request.GET.get('search_duty')
   # search_duty_id = request.GET.get('search_duty_id')
   # search_company_name = request.GET.get('search_company_name')
   # search_certificate_level = request.GET.get('search_certificate_level')
   # search_special_certificate = request.GET.get('search_special_certificate')
   # search_route_area = request.GET.get('search_route_area')
  #  search_recruitment_ship = request.GET.get('search_recruitment_ship')
   # search_tonnage = request.GET.get('search_tonnage')
   # search_time = request.GET.get('search_time')

    Information.objects.create(
        ship_age=search_ship_age,
        duty=search_duty,
        duty_id=search_duty_id,
        company_name=search_company_name,
        certificate_level=search_certificate_level,
        special_certificate=search_special_certificate,
        route_area=search_route_area,
        recruitment_ship=search_recruitment_ship,
        tonnage=search_tonnage,
        time=search_time
    )
    information_list = Information.objects.filter(ship_age__exact=search_ship_age,
                                                  duty__exact=search_duty,
                                                  duty_id__exact=search_duty_id,
                                                  company_name__exact=search_company_name,
                                                  certificate_level__exact=search_certificate_level,
                                                  special_certificate__exact=search_special_certificate,
                                                  route_area__exact=search_route_area,
                                                  recruitment_ship__exact=search_recruitment_ship,
                                                  tonnage__exact=search_tonnage,
                                                  time__exact=search_time
                                                  )[0:1]
    error_msg = '未搜索到内容，请重新输入'

    if search_duty == '':
        post_list = Library.objects.all()
    else:
        post_list = Library.objects.filter(duty__exact=search_duty)
    if search_ship_age == '':
        post_list = post_list.filter()
    else:
        post_list = post_list.filter(ship_age__exact=search_ship_age)
    if search_company_name == '':
        post_list = post_list.filter()
    else:
        post_list = post_list.filter(company_name__iexact=search_company_name)
    if search_certificate_level == '':
        post_list = post_list.filter()
    else:
        post_list = post_list.filter(certificate_level__exact=search_certificate_level)
    if search_special_certificate == '':
        post_list = post_list.filter()
    else:
        post_list = post_list.filter(special_certificate__exact=search_special_certificate)
    if search_route_area == '':
        post_list = post_list.filter()
    else:
        post_list = post_list.filter(route_area__exact=search_route_area)
    if search_tonnage == '':
        post_list = post_list.filter()
    else:
        post_list = post_list.filter(tonnage__exact=search_tonnage)
    if search_time == '':
        post_list = post_list.filter()
    else:
        post_list = post_list.filter(time__exact=search_time)

  #  del request.session['duty']
 #   del request.session['ship_age']
  #  del request.session['company_name']
  #  del request.session['certificate_level']
  #  del request.session['special_certificate']
  #  del request.session['route_area']
 #   del request.session['tonnage']
 #   del request.session['time']
  #  del request.session['duty_id']
 #   del request.session['recruitment_ship']

    return render_to_response('recruit/search_detail.html',
                              {'error_msg': error_msg,
                               'post_list': post_list,
                               'information_list': information_list,
                               'title_list':title_list}
                              )


class News(ListView):
    template_name = "news/news_list.html"
    context_object_name = "article_list"

    def get_queryset(self):
        # 过滤数据，获取所有已发布文章，并且将内容转成markdown形式
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'] )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['body_archive'] = Article.objects.archive()
        return super(News, self).get_context_data(**kwargs)



class ArticleDetailView(DetailView):
    model = Article
    template_name = "news/detail.html"
    # 指定要渲染的文件
    context_object_name = "article"
    # 在模板中要使用的上下文名字
    pk_url_kwarg = 'article_id'
    # pk_url_kwarg用于接受一个来自url中的主键，然后会根据这个主键进行查询
    # 我们之前在urlpatterns已经捕获article_id

    def get_object(self, queryset=None):
        # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
        # 返回该视图要显示的对象
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj

    # 第五周新增
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class ArchiveView(ListView):
    template_name = "news/news_list.html"
    context_object_name = "article_list"

    def get_queryset(self):  # 接收从url传递的year和month参数，转为int类型
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])  # 按照year和month过滤文章
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        return super(ArchiveView, self).get_context_data(**kwargs)


# 第五周新增
class CommentPostView(FormView):
    form_class = BlogCommentForm
    template_name = 'news/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return render(self.request, 'news/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })


def contact(request):
    b_username = request.COOKIES.get('username')
    title_list = User.objects.filter(username__exact=b_username)[0:1]
    con_list = Contact.objects.all()
    return render_to_response('contact/contact.html', {'con_list': con_list,'title_list':title_list})
