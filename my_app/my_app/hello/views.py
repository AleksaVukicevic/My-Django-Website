from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import FridgeItem
from .forms import CreateUserForm


#User stuff
def register(request):
	if request.user.is_authenticated:
		return redirect('/')
	else: 
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was creater for ' + user)
				return redirect('/login/')
	context = {'form':form}
	return render(request,'register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else: 
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/')
			else:
				messages.info(request, 'Username or password are incorect')
	context = {}
	return render(request,'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('/login/')



#Pages stuff
def indexPage(request):
	return render(request,'index.html')

def game(request):
	return render(request,'game.html')

@login_required(login_url='/login/')
def home(request):
	all_items = FridgeItem.objects.all()
	return render(request,'home.html',
		{'all_items':all_items})

@login_required(login_url='/login/')
def edit(request, id):
	item_to_edit = FridgeItem.objects.get(id=id)
	return render(request,'edit.html',
		{'item_to_edit':item_to_edit})



#Actions
@login_required(login_url='/login/')
def add(request):
	new_item = FridgeItem(text = request.POST['text'])
	new_item.save()
	return redirect('/home/')

@login_required(login_url='/login/')
def delete(request, id):
	item_to_delete = FridgeItem.objects.get(id=id)
	item_to_delete.delete()
	#item_to_delete.text = 'a'
	#item_to_delete.save()
	return redirect('/home/')

@login_required(login_url='/login/')
def changeItem(request, id):
	item_to_change = FridgeItem.objects.get(id=id)
	item_to_change.text = request.POST['text']
	item_to_change.save()
	return redirect('/home/')
	