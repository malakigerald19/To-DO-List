from django.http import HttpResponse
from django.shortcuts import render
from lists.models import Item
from django.shortcuts import redirect

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/lists/the-only-list-in-the-world/')
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

def view_lists(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items' : items})