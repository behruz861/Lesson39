from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from .forms import PostCreateModelForm
from .models import Post, Tag
from django.core.cache import cache
from django.core.cache.backends.filebased import FileBasedCache


file_cache = FileBasedCache('file_cache', {})

def post_list_view(request):
    post_list = file_cache.get('post_list')
    tag_list = file_cache.get('tag_list')
    tag_count = file_cache.get('tag_count')

    if post_list is None:
        post_list = Post.objects.all()
        tag_list = Tag.objects.all()
        tag_count = Tag.objects.all().count()

        # Сохраните данные в файловый кэш
        file_cache.set('post_list', post_list, 10)
        file_cache.set('tag_list', tag_list, 10)
        file_cache.set('tag_count', tag_count, 10)

    context = {'post_list': post_list, 'tag_list': tag_list, 'tag_count': tag_count}
    return render(request, 'blogapp/post_list.html', context)

def post_list_by_tag_view(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    context = {'post_list': Post.objects.filter(tags=tag.pk), 'tag_list': Tag.objects.all()}
    return render(request, 'blogapp/post_list.html', context)


def post_detail(request, slug):
    context = {'post': get_object_or_404(Post, slug=slug)}
    return render(request, 'blogapp/post_detail.html', context)

def crete_post(request):
    context = {'form': PostCreateModelForm()}

    if request.method == 'POST':
        form = PostCreateModelForm(request.POST)
        if form.is_valid():
            form.save()

            # Сбросьте соответствующие ключи в файловом кэше после создания нового поста
            file_cache.delete('post_list')
            file_cache.delete('tag_list')
            file_cache.delete('tag_count')

            return redirect('post_list')
        else:
            context['form'] = form
    return render(request, 'blogapp/post_create.html', context)
