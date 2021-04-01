from django import forms
from .models import Image
import urllib
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ['title', 'url', 'description']
		widgets = {
			'url': forms.HiddenInput,
		}

	#  clean specific fields using the clean_<fieldname>()
	def clean_url(self):
		url = self.cleaned_data['url']
		valid_image_extensions = ['jpg','jpeg']
		link_extension = url.rsplit('.',1)[1].lower()
		if link_extension not in valid_image_extensions:
			raise forms.ValidationError("Given URL doesn't match the valid extension.")

		return url

	def save(self, force_insert=False, force_update=False, commit=True):
		image_url = self.cleaned_data['url']
		extension = image_url.rsplit('.',1)[1].lower()

		image = super().save(commit=False)
		name = slugify(self.cleaned_data['title'])

		image_name = f'{name}.{extension}'

		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		response = urllib.request.Request(url=image_url, headers=headers)

		# ContentFile object: It is instantiated with the downloaded file content
		image.image.save(image_name, ContentFile(urllib.request.urlopen(response).read()), save=False)

		if commit:
			image.save()

		return image