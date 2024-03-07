from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from hitcount.utils import get_hitcount_model

from django.views import View
from django.urls import reverse_lazy, reverse
from news_app.forms import ContactForm, CommentForm
from news_app.models import News, Contact, Category, Like, Comment, CountView

"""
views: 2xil:
1. funksional view: def
2. klass view: basic va generic

request:
[GET, POST, PUT, PATCH, DELETE, HEAD, OPTION]


"""

# function views ---------------------------------------------

# @require_http_methods(['GET', 'HEAD'])
# def list_view(request):
#     all_news = News.published.all()
#     context = {
#         'news': all_news
#     }
#     return render(request, 'news/news_list.html', context)


# def detail_view(request, pk):
#     try:
#         new = News.published.get(pk=pk)
#         context = {
#             'new': new
#         }
#         return render(request, 'news/detail.html', context)
#     except:
#         return HttpResponseBadRequest(content="Bunday yangilik yo'q")


# def detail_view(request, pk):
#     new = get_object_or_404(News, pk=pk)
#     context = {
#         'new': new
#     }
#     return render(request, 'news/detail.html', context)


# Basic class views ----------------------------------------------------

# class ListView(View):
#     def get(self, request, *args, **kwargs):
#         all_news = News.published.all()
#         context = {
#             'news': all_news
#         }
#         return render(request, 'news/news_list.html', context)
#
#     def post(self):
#         pass
#
#     def put(self):
#         pass
#
#     def delete(self):
#         pass


# class DetailView(View):
#     model = News
#     template_name = 'news/detail.html'
#
#     def get(self, request, pk, *args, **kwargs):
#         new = get_object_or_404(self.model, pk=pk)
#         context = {
#             'new': new
#         }
#         return render(request, self.template_name, context)


# Generic views -----------------------------------------------------------


class HomePageView(View):
    model = News
    template_name = 'news/home.html'

    def get(self, request, *args, **kwargs):
        four_news = News.published.all()[1:5]
        all_news = News.published.all().order_by('-publish_time')
        last_new = News.published.first()
        trending_news = [[news, HitCount.objects.get_for_object(news).hits] for news in all_news]
        trending_news = sorted(trending_news, key=lambda news: news[1])
        trending_news = [news[0] for news in reversed(trending_news)]
        context = {
            'last_new': last_new,
            'four_news': four_news,
            'all_news': all_news,
            'trending_news': trending_news
        }
        return render(request, self.template_name, context)


class NewsCategoryListGenericView(ListView):
    model = News
    template_name = "news/news.html"
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return queryset.filter(status=News.Status.Published, category=category)


# class DetailGenericView(DetailView):
#     model = News
#     template_name = 'news/single.html'
#     context_object_name = 'new'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         news = self.get_object()
#         if self.request.user.is_authenticated:
#             like = Like.objects.filter(author=self.request.user, news=news)
#             context['liked'] = True if like else False
#         else:
#             context['liked'] = False
#         return context


class ContactGenericView(View):
    template_name = 'news/contact.html'
    form = ContactForm
    model = Contact

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form(None)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Sizning xabaringiz yuborildi!", extra_tags='success')
            return render(request, self.template_name)
        messages.error(request, "Xabaringiz yuborilmadi!", extra_tags='danger')
        return render(request, self.template_name, {'form': form})


def create_delete_like_news(request, slug):
    news = get_object_or_404(News, slug=slug)
    user = request.user
    like = Like.objects.filter(author=user, news=news)
    if like.exists():
        like.first().delete()
    else:
        like = Like.objects.create(author=user, news=news)
        like.save()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


class NewsDetailView(View):

    def get(self, request, slug, *args, **kwargs):
        template_name = 'news/single.html'
        try:
            new = News.published.get(slug=slug)
        except News.DoesNotExist:
            return render(request, template_name='404.html')



        hitcontext = {}
        # hit count logic
        hitcount = get_hitcount_model().objects.get_for_object(new)
        hits = hitcount.hits
        hitcontext['hitcount'] = {'pk': hitcount.pk}
        hit_count_response = HitCountMixin.hit_count(request, hitcount)
        if hit_count_response.hit_counted:
            hits += 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
            hitcontext['total_hits'] = hits

        context = {'new': new}
        view_count = HitCount.objects.get_for_object(new)
        context['view_count'] = view_count
        if self.request.user.is_authenticated:
            like = Like.objects.filter(author=self.request.user, news=new)
            context['liked'] = True if like else False
        else:
            context['liked'] = False
        all_news = News.published.all().order_by('-publish_time')
        trending_news = [[news, HitCount.objects.get_for_object(news).hits] for news in all_news]
        trending_news = sorted(trending_news, key=lambda news: news[1])
        trending_news = [news[0] for news in reversed(trending_news)]
        context['trending_news'] = trending_news


        return render(request, template_name, context)

    def post(self, request, slug, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Izoh yozish uchun login qiling!")
            previous_page = request.META.get('HTTP_REFERER')
            return redirect(previous_page)
        form = CommentForm(request.POST)
        try:
            news = News.published.get(slug=slug)
        except News.DoesNotExist:
            return render(request, template_name='404.html')
        if form.is_valid():
            comment_text = form.cleaned_data.get('comment')
            comment = Comment.objects.create(author=request.user, news=news, comment=comment_text)
            comment.save()
        previous_page = request.META.get('HTTP_REFERER')
        return redirect(previous_page)
