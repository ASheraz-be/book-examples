from django.http import HttpResponseBadRequest


'''
	Build custom decorators for your views if you find that you are
	repeating the same checks in multiple views.
'''

# HTTP 400 code if the request is not AJAX
def ajax_required_decorator(f):
	def wrap(request, *args, **kwargs):
		if request.is_ajax():
			return f(request, *args, **kwargs)
		return HttpResponseBadRequest()

	wrap.__doc__ = f.__doc__
	wrap.__name__ = f.__name__
	return wrap
