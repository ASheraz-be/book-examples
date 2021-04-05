from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView
# login_required: FOR FUNTION BASED VIEW
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
# method_decorator: FOR CLASS BASED VIEW
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Image
from common.decorators import ajax_required_decorator

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from actions.utils import create_action

# import redis
# from django.conf import settings
# # connect to redis
# r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@method_decorator(login_required, name='dispatch')
class ImageView(FormView):
	form_class = ImageForm
	template_name = 'images/image/add_image.html'

	def post(self, request, *args, **kwargs):
		form = ImageForm(data=request.POST)

		if form.is_valid():
			clean_data = form.cleaned_data
			new_entry = form.save(commit=False)
			new_entry.user = request.user
			new_entry.save()
			messages.success(request, 'Image added successfully')

			# redirect to new created item detail view
			return redirect(new_entry.get_absolute_url())

		return render(request, self.template_name, {'section': 'images','form': self.form})

	def get(self, request, *args, **kwargs):
		form = self.form_class(data=request.GET)
		return render(request, self.template_name, {'section': 'images','form': form})

# @login_required
# def ImageView(request):
# 	if request.method == 'POST':
# 		# form is sent
# 		form = ImageForm(data=request.POST)
# 		if form.is_valid():
# 			# form data is valid
# 			cd = form.cleaned_data
# 			new_item = form.save(commit=False)
# 			# assign current user to the item
# 			new_item.user = request.user
# 			new_item.save()
# 			messages.success(request, 'Image added successfully')
# 			# redirect to new created item detail view
# 			return redirect(new_item.get_absolute_url())
# 	else:
# 		# build form with data provided by the bookmarklet via GET
# 		form = ImageForm(data=request.GET)
# 	return render(request,
# 	'images/image/add_image.html',
# 	{'section': 'images',
# 	'form': form})

@login_required
def image_detail(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	# total_views = r.incr(f'image:{image.id}:views')
	return render(request,'images/image/detail.html', {'section': 'images','image': image})


@ajax_required_decorator
@login_required
@require_POST
def ajax_image_like(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')

	try:
		if action and image_id:
			image_obj = Image.objects.get(id=image_id)
			if action == 'like':
				# used manager for "users_image_like" field of Image class model
				image_obj.users_image_like.add(request.user)
				create_action(request.user, 'likes', image)
			else:
				image_obj.users_image_like.remove(request.user)

			return JsonResponse({"status":"ok"})
	except:
		pass

	return JsonResponse({"status":"error"})


# class basedlist view
# class ImageListView(ListView):
# 	# queryset = Post.draft.all()
# 	# context_object_name = 'posts'
# 	model = Image
# 	paginate_by = 2
# 	template_name = 'images/image/list.html'

# 	def get_queryset(self):
# 		if self.kwargs and self.kwargs['slug_val']:
# 			tag = get_object_or_404(Image, slug=self.kwargs['slug_val'])
# 			return Post.draft.filter(tag__in=[tag])
# 		return Post.draft.all()

@login_required
def image_list(request):
	images = Image.objects.all()
	paginator = Paginator(images, 8)
	page = request.GET.get('page')
	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		images = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range
			# return an empty page
			return HttpResponse('')
		# If page is out of range deliver last page of results
		images = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request,'images/image/list_ajax.html',{'section': 'images', 'images': images})
	return render(request,'images/image/list.html',	{'section': 'images', 'images': images})
