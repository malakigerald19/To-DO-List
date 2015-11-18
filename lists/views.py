from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from lists.models import Item,List
from django.shortcuts import redirect

# Create your views here.
def home_page(request):
	
	return render(request, 'home.html')
	#	new_item_text = request.POST['item_text']
	#	Item.objects.create(text=new_item_text)
	#else:
	#	new_item_text =''
	#item = Item()
	#item.text = request.POST.get('item_text', '')
	#item.save()
	items = Item.objects.all()
	return render(request,'home.html', {'items' : items})

def new_list(request):
	list_ = List.objects.create()
	item = Item(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request,'home.html', {"error": error})
	return redirect('/lists/%d/' % (list_.id,))

def view_list(request,list_id):
	list_ = List.objects.get(id=list_id)
	return render(request, 'list.html', {'list': list_})

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))
