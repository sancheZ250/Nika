from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import etag
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, viewsets

from .models import News, NewsImage, Comment
from .forms import NewsForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

# class NewsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#
# class NewsAPIListCreateView(generics.ListCreateAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer

def add_news(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                news = form.save(commit=False)
                news.author = request.user
                news.save()
                if form.cleaned_data.get('images'):
                    images = request.FILES.getlist('images')
                    for image in images:
                        NewsImage.objects.create(news_id=news, image=image)
                    return redirect('news')
                return redirect('news')
        else:
            form = NewsForm()
        return render(request, 'News/creation_news.html', {'form': form})
    else:
        return HttpResponse('У вас нет прав для добавления новостей!')


class NewsListView(ListView):
    template_name = 'News/news_in_blocks.html'
    context_object_name = 'news'
    paginate_by = 9

    def get_queryset(self):
        queryset = News.objects.filter(is_published=True).order_by('-date_created')
        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = 'News/news_details.html'
    context_object_name = 'news'

    @method_decorator(cache_page(15))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.news_id = self.object
            comment.save()
            return JsonResponse({'success': True})  # Return a JSON response
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


def search_news_view(request):
    search_query = request.GET.get('q', '')

    # Поиск новостей по названию
    news = News.objects.filter(Q(title__icontains=search_query)).order_by('-date_created')

    # Контекст с результатами поиска
    context = {'news': news}

    # Возвращаем HTML-фрагмент
    return render(request, 'News/search_results.html', context)

def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if news.author == request.user:
        news.delete()
        return JsonResponse({'message': 'Новость успешно удалена.'})
    else:
        return JsonResponse({'error': 'Вы не можете удалить эту новость.'})