from django import forms

class NameForm(forms.Form):
	FirstName = forms.CharField(label='First name', max_length=100)
	LastName = forms.CharField(label='Last name', max_length=100)

	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=False)

class ArticleForm(forms.Form):
	title = forms.CharField()
	pub_date = forms.DateField()
