from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib


from . import forms
from .models import ItemCount, Video


def landing_page(request):
    temp_dict = {}
    try:
        item_count_obj = ItemCount.objects.get(id=1)
    except:
        item_count_obj = ItemCount()
        item_count_obj.total_count = 250
        item_count_obj.save()

    total_count = int(item_count_obj.total_count)
    if total_count > 250:
        total_count = 250
    videos_list = Video.objects.all()
    paginator = Paginator(videos_list,total_count)
    page = request.GET.get('page')
    try:
        page_videos = paginator.page(page)
    except PageNotAnInteger:
        page_videos = paginator.page(1)
    except EmptyPage:
        page_videos = paginator.page(paginator.num_pages)

    temp_dict['videos'] = page_videos

    return render_to_response(
        'home.html',
        temp_dict, context_instance=RequestContext(request))


@staff_member_required
def adminpanel(request):
    temp_dict = {}
    try:
        item_count_obj = ItemCount.objects.get(id=1)
    except:
        item_count_obj = ItemCount()
        item_count_obj.total_count = 250
        item_count_obj.save()

    form = forms.SetItemCountForm(instance=item_count_obj)
    if request.POST:
        form = forms.SetItemCountForm(request.POST, instance=item_count_obj)
        if form.is_valid:
            form.save()
    temp_dict['form'] = form
    return render_to_response(
        'adminpanel.html',
        temp_dict, context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


@staff_member_required
def video_scraping(request):
    try:
        page = urllib.urlopen("http://www.imdb.com/chart/top")
        soup = BeautifulSoup(page)
        flag = 1
        print soup
    except:
        pass

    if flag == 1:
        try:
            item_count_obj = ItemCount.objects.get(id=1)
        except:
            item_count_obj = ItemCount()
            item_count_obj.total_count = 250
            item_count_obj.save()
        poster_columns = soup.findAll('td', {'class':'posterColumn'})
        print len(poster_columns)
        count = 1
        for poster in poster_columns:
            x = poster.findNextSibling('td')
            y = x.findNextSibling('td')
            title = x.a.text
            hover_text = x.a['title']
            movie_url = 'http://www.imdb.com/'+str(poster.a['href'])
            img_url = poster.a.img['src']
            rating = y.strong.text
            no_of_votes = str(y.strong['title']).split(' ')[3]

            try:
                video_obj = Video.objects.get(title=title)
            except:
                video_obj = Video()
                video_obj.video_rank = str(x.span.text).replace('.','')
                video_obj.count = count
                video_obj.title = title
                video_obj.hover_text = hover_text
                video_obj.movie_url = movie_url
                video_obj.image_url = img_url
                video_obj.rating = rating
                video_obj.no_of_votes = no_of_votes
                video_obj.save()
                count += 1
    return HttpResponseRedirect('/')

