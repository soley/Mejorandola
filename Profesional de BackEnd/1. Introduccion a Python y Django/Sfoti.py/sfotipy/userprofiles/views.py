from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.http import HttpResponse

from .forms import UserCreationEmailForm, EmailAuthenticationForm
# Create your views here.
def signup(request):
	form = UserCreationEmailForm(request.POST or None)

	if form.is_valid():
		form.save()
		#Logear inmediatamente despues de guardar el usuario

	return render(request, 'signup.html', {'form': form})

def signin(request):
	form = EmailAuthenticationForm(request.POST or None)

	if form.is_valid():
		login(request, form.get_user())

	return render(request, 'signin.html', {'form': form})

class LoginView(TemplateView):
	
	#def get(self, request, *args, **kwargs):
		#return HttpResponse('LoginView!!')

	template_name = 'login.html'

	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		is_auth = False
		name=None

		if self.request.user.is_authenticated():
			is_auth = True
			name = self.request.user.username

		data = {
			'is_auth': is_auth,
			'name': name,
		}

		context.update(data)

		return context

class ProfileView(TemplateView):
	template_name = 'profile.html'

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)

		if self.request.user.is_authenticated():
			context.update({'userprofile': self.get_userprofile()})

		return context

	def get_userprofile(self):
		return self.request.user.userprofile