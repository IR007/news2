from modeltranslation.translator import translator, TranslationOptions
from .models import News, Category


class NewsTranslationOption(TranslationOptions):
    fields = ['title', 'summary', 'body']


translator.register(News, NewsTranslationOption)


class CategoryTranslationOption(TranslationOptions):
    fields = ['name']


translator.register(Category, CategoryTranslationOption)
