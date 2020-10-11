
from django import forms
from .models import Comments, Post

#creates form for new post inherits from forms.ModelForm class
class NewPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['pic', 'tags']

#creates  form for new comments
class NewCommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ['comment']