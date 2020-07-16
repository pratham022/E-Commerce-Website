from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Blogpost
# Create your views here.

def index(request):
    blog_set = Blogpost.objects.all()
    i = 0
    blog_list = []
    for blog_item in blog_set:
        blog_id = blog_item.blog_id
        title = blog_item.post_title[0:20]+"..."
        date = blog_item.post_date
        brief = blog_item.brief[0:40]+'...'
        blog = [title, date, brief, blog_id]
        blog_list.append(blog)

    params = {'all_blogs': blog_list}
    print(params)

    return render(request, 'blog/index.html', params)

def blogpost(request, myid):

    obj = Blogpost.objects.filter(blog_id=myid)
    post_title = obj[0].post_title
    post_date = obj[0].post_date
    brief = obj[0].brief
    intro1 = obj[0].intro1
    intro2 = obj[0].intro2
    subheading1 = obj[0].subheading1
    content1 = obj[0].content1
    subheading2 = obj[0].subheading2
    content2 = obj[0].content2
    subheading3 = obj[0].subheading3
    content3 = obj[0].content3
    about_content = obj[0].about_content
    image = obj[0].image
    params = {'blog_detail': [post_title, post_date, brief, intro1, intro2, subheading1, content1, subheading2,
              content2, subheading3, content3, about_content, image, myid]}
    return render(request, 'blog/blogpost.html', params)
