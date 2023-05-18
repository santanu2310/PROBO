from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import json
from django.core.validators import validate_email
from django.core import serializers
from django.views.generic import TemplateView

# Create your views here.

def home(request):
    if request.method == "POST":
        email = json.loads(request.body)['email']
        try:
            validate_email(email)
        except:
            print('pour email')
            return JsonResponse(data={'status':'P_Email'})
        print(email)
        try:
            new_sub = Subscriber.objects.create(email = email)
            new_sub.save()
            return JsonResponse(data={'status':'Success'})
        except:
            print('email already exist')
            return JsonResponse(data={'status':'E_Email'})
        
    banners = Blog.objects.order_by('?')[:4]
    if banners:
        banner1 = banners[:3]
        banner2 = banners[3]

    popular_topics_categories = Category.objects.order_by('?')[:5]
    popular_topics = Blog.objects.order_by('-visitors')[:8]
    editor_picks = Blog.objects.filter(eidtors_pick = True).order_by('?')[:3]
    context = {'banner1':banner1, 'banner2':banner2, 'popular_topics':popular_topics, 'editor_picks':editor_picks, 'popular_topics_categories':popular_topics_categories}
    return render(request,'blog_app/index.html', context)

def blog(request,id):
    blog = Blog.objects.get(id = id)

    blog.visitors+=1
    blog.save()

    related_blogs = Blog.objects.filter(category = blog.category).order_by('-visitors').exclude(id = blog.id)[:3]
    context = {'blog':blog, 'related_blogs':related_blogs}
    return render(request,'blog_app/blog.html', context)

def articles(request):
    categories = Category.objects.all()
    popular_topics_categories = Category.objects.order_by('?')[:5]
    recent_blogs = Blog.objects.order_by('-date')[:12]
    context = {'categories':categories, 'recent_blogs':recent_blogs,'popular_topics_categories':popular_topics_categories}
    return render(request, 'blog_app/articles.html', context)

def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        vector = SearchVector('name','category__name','tags__name','short_desc')
        query = SearchQuery(q)
        blogs=Blog.objects.annotate(rank=SearchRank(vector, query, cover_density = True)).filter(rank__gte=0.1).order_by('-rank').distinct()
        
        paginator = Paginator(blogs,12)
        page_number = request.GET.get('page')
        blog_objs = paginator.get_page(page_number)
        context = {'blog_objs':blog_objs,'q':q}
        return render(request,'blog_app/blog_list.html', context)

def getblog(request):
    data = json.loads(request.body)
    category = Category.objects.filter(name = data['category'])[:1]
    if data['section'] == 'POTO69':
        blogs = Blog.objects.filter(category = category[0]).order_by('visitors')[:8]
    elif data['section'] == 'RECENT':
        blogs = Blog.objects.filter(category = category[0]).order_by('-date')[:12]

        
    return JsonResponse(data=serializers.serialize("json", blogs),safe=False)


class AboutView(TemplateView):
    template_name = "blog_app/about.html"

def contact(request):
    return render(request, 'blog_app/contact.html')