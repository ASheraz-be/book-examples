from django.shortcuts import render, get_object_or_404
from .models import Post, Comments
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentsForm
from django.core.mail import send_mail

# Import tag model
from taggit.models import Tag

# Below function is to handle form
def post_share(request, post_id):
	post = get_object_or_404(Post, id=post_id, status="draft")
	sent = False
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			send_mail(clean_data['name'], clean_data['comments'], clean_data['email'], [clean_data['to']])
			sent = True

	else:
		form = EmailPostForm()

	return render(request,'blog/post/share.html',{'form':form,'post':post, 'sent':sent})



# class basedlist view
class PostListView(ListView):
	# queryset = Post.draft.all()
	context_object_name = 'posts'
	paginate_by = 2
	template_name = 'blog/post/list.html'
	def get_queryset(self):
		if self.kwargs and self.kwargs['slug_val']:
			tag = get_object_or_404(Tag, slug=self.kwargs['slug_val'])
			return Post.draft.filter(tag__in=[tag])
		return Post.draft.all()


# list view
def post_list(request,slug_val=None):

	posts = Post.draft.all()
	tag = None
	if slug_val:
		tag = get_object_or_404(Tag, slug=slug_val)
		posts = posts.filter(tag__in=[tag])

	
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
	{'page': page,'posts': posts, 'tag': tag})



# detailed view using form created using model
# e save() method is available for ModelForm but not for base Form instances
def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
	status='draft',
	publish__year=year,
	publish__month=month,
	publish__day=day)

	# related_field option in the model used here
	comment = post.comments.filter(activate=True)

	# comment = Comments.objects.filter(activate=True) # we can also use direct filter but it is slow

	new_comment = None

	if request.method == 'POST':
		comment_form = CommentsForm(request.POST)

		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()


	else:
		comment_form = CommentsForm()

	return render(request,
	'blog/post/detail.html',
	{'post': post, 'comments':comment, 'new_comment': new_comment, 'comment_form':comment_form})