from hitcount.models import HitCount

from news_app.models import Category, News


def context_categories(request):
    context = {'categories': Category.objects.all()}
    return context


def context_popular_news(request):
    news_all = News.published.all()
    news_likes_lists = [[news, news.likes.count()] for news in news_all]
    sorted_new_list = sorted(news_likes_lists, key=lambda news: news[1], reverse=True)
    popular_news = [news[0] for news in sorted_new_list]

    trending_news = [[news, HitCount.objects.get_for_object(news).hits] for news in news_all]
    trending_news = sorted(trending_news, key=lambda news: news[1])
    most_viewed_news = [news[0] for news in reversed(trending_news)]
    context = {
        'popular_news': popular_news[:5],
        'most_viewed_news': most_viewed_news[:3]
    }
    return context

