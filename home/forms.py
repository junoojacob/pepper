from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		# The fields that will be visible in the form
		fields = ['name', 'email', 'image']