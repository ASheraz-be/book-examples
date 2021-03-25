from django import forms
from .models import Comments


# Form: Allows you to build standard forms
# ModelForm: Allows you to build forms tied to model instances

class SearchForm(forms.Form):
	search_query = forms.CharField()

 # using "base Form class"
class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()

	# default widget can be overridden with the widget attribute
	comments = forms.CharField(max_length=250, required=False, widget=forms.Textarea)

# create form using "Model Form class"
class CommentsForm(forms.ModelForm):
	class Meta:
		model = Comments

		# The fields can be list or tuple as well.
		fields = ['name', 'email', 'body', 'activate']