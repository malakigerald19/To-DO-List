from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from lists.models import Item,List
from django.shortcuts import redirect
from lists.forms import ItemForm, ExistingListItemForm


# Create your views here.
def home_page(request):
	
	return render(request, 'home.html',{'form': ItemForm()})
	items = Item.objects.all()
	return render(request,'home.html', {'items' : items})

def new_list(request):
	form = ItemForm(data=request.POST)
	if form.is_valid():
		list_ = List.objects.create()
		Item.objects.create(text=request.POST['text'], list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html', {"form": form})
	# list_ = List.objects.create()
	# item = Item(text=request.POST['text'], list=list_)
	# try:
	# 	item.full_clean()
	# 	item.save()
	# except ValidationError:
	# 	#list_.delete()
	# 	error = "You can't have an empty list item"
	# 	return render(request,'home.html', {"error": error})
	# return redirect('view_list', list_.id)

def view_list(request,list_id):
	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list=list_)
	if request.method == 'POST':
		form = ExistingListItemForm(for_list=list_, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(list_)
	return render(request, 'list.html', {'list': list_, 'form': form})

# def add_item(request, list_id):
# 	list_ = List.objects.get(id=list_id)
# 	I
# 	return redirect('/lists/%d/' % (list_.id,))
