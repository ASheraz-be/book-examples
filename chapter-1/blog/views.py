from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


# class basedlist view
class PostListView(ListView):
	queryset = Post.draft.all()
	context_object_name = 'posts'
	paginate_by = 2
	template_name = 'blog/post/list.html'


# list view
def post_list(request):
	posts = Post.draft.all()
	paginator = Paginator(posts, 2) # 1 posts in each page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)

	return render(request,
	'blog/post/list.html',
	{'page': page,'posts': posts})

# detailed view
def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
	status='published',
	publish__year=year,
	publish__month=month,
	publish__day=day)

	return render(request,
	'blog/post/detail.html',
	{'post': post})