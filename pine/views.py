from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Sum
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='login')
def category(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        cat_form = CategoryForm()

    context = {'cat_form': cat_form,'category': category }
    return render(request, 'crop_yield/category.html', context)

def cat_delete(request, pk):
	categorys = Category.objects.get(id=pk)
	if request.method == 'POST':
		categorys.delete()
		# messages.success(request, 'Deleted Succesfully')

		return redirect('category')
	return render(request, 'crop_yield/category_delete.html')

def calculate_total_price(queryset):
    total_value = 0
    for item in queryset:
        if item.value is not None:
            total_value += item.value
    return total_value

@login_required(login_url='login')
def crop(request):
    category_filter = request.GET.get('category')
    all_categories = Category.objects.all()
    crops = Crop.objects.all()
    if category_filter:
        crops = crops.filter(category__name=category_filter)
    # rooms = Room.objects.all()
    pine_price = PinePrice.objects.first()

    total_planted = Crop.objects.aggregate(total_planted=models.Sum('number_planted'))['total_planted']
    cost = None

    hawaii_crop = (
        Crop.objects.filter(category__name='Hawaii')
        .values('plant_date')
        .annotate(total_planted=Sum('number_planted'))
        .order_by('plant_date')
    )
    pormosa_crop = (
        Crop.objects.filter(category__name='Pormosa')
        .values('plant_date')
        .annotate(total_planted=Sum('number_planted'))
        .order_by('plant_date')
    )

    hawaii_pine_crop = PinePrice.objects.filter(category='2').first()
    pormosa_pine_crop = PinePrice.objects.filter(category='1').first()

    for item in hawaii_crop:
        item['price'] = float(item['total_planted']) * (float(hawaii_pine_crop.price) if hawaii_pine_crop else 0)

    for item in pormosa_crop:
        item['price'] = float(item['total_planted']) * (float(pormosa_pine_crop.price) if pormosa_pine_crop else 0)

    if total_planted is not None and pine_price is not None:
            cost = total_planted * pine_price.price

    if request.method == 'POST':
        form = CropForm(request.POST)  

        if form.is_valid():
            category = form.cleaned_data['category']
            number_planted = form.cleaned_data['number_planted']
            plant_date = form.cleaned_data['plant_date']

            existing_crop = Crop.objects.filter(category=category, plant_date=plant_date).first()

            if existing_crop:
                existing_crop.number_planted += number_planted
                existing_crop.price = pine_price
                existing_crop.product = existing_crop.number_planted * pine_price.price
                existing_crop.save()
            else:
                new_crop = form.save(commit=False)
                new_crop.price = pine_price
                new_crop.product = new_crop.number_planted * pine_price.price 
                new_crop.save()

            return redirect('crop')
    else:
        form = CropForm()

    context = {'crops': crops, 
               'form': form, 
               'pine_price': pine_price, 
               'hawaii_crop': hawaii_crop,
               'pormosa_crop': pormosa_crop,
               'all_categories': all_categories,
               'total_cost': cost, 
            #    'rooms': rooms, 
               'room_name': "broadcast"}
    return render(request, 'crop_yield/crop.html', context)



@login_required(login_url='login')
def crop_update(request, pk):
    crop = Crop.objects.get(id=pk)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crop')
    else:
        form = CropForm(instance=crop)
    context = {'form': form}
    return render(request, 'crop_yield/crop_update.html', context)

def crop_delete(request, pk):
    crop = Crop.objects.get(id=pk)
    crops = Crop.objects.all
    if request.method == 'POST':
        crop.delete()
        return redirect('crop')

    return render(request, 'crop_yield/crop_delete.html', {'crops':crops})

from django.db.models import Count
@login_required(login_url='login')
def yields(request):
    category_filter = request.GET.get('category')
    all_categories = Category.objects.all()
    yields = Yield.objects.all()
    if category_filter:
        yields = yields.filter(category__name=category_filter)

        
    pine_value = PineValue.objects.first()
    total_yield = Yield.objects.aggregate(total_yield=models.Sum('number_yield'))['total_yield']
    value = None

    # x = Yield.objects.values('harvest_date').annotate(item_count=Count('id'))
    hawaii_yields = (
        Yield.objects.filter(category__name='Hawaii')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )
    pormosa_yields = (
        Yield.objects.filter(category__name='Pormosa')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )

    hawaii_pine_value = PineValue.objects.filter(category='2').first()
    pormosa_pine_value = PineValue.objects.filter(category='1').first()

    # Calculate the value for each category and each date
    for item in hawaii_yields:
        item['value'] = float(item['total_yield']) * (float(hawaii_pine_value.value) if hawaii_pine_value else 0)

    for item in pormosa_yields:
        item['value'] = float(item['total_yield']) * (float(pormosa_pine_value.value) if pormosa_pine_value else 0)

    if total_yield is not None and pine_value is not None:
        value = total_yield * pine_value.value 

    if request.method == 'POST':
        yield_form = YieldForm(request.POST)

        if yield_form.is_valid():
            category = yield_form.cleaned_data['category']
            number_yield = yield_form.cleaned_data['number_yield']
            harvest_date = yield_form.cleaned_data['harvest_date']

            # Check if there is an existing yield record for the same date and category
            existing_yield = Yield.objects.filter(category=category, harvest_date=harvest_date).first()

            if existing_yield:
                existing_yield.number_yield += number_yield
                existing_yield.value = pine_value
                existing_yield.product = existing_yield.number_yield * pine_value.value
                existing_yield.save()
            else:
                new_yield = yield_form.save(commit=False)
                new_yield.value = pine_value
                new_yield.product = new_yield.number_yield * pine_value.value
                new_yield.save()

            return redirect('yield')
    else:
        yield_form = YieldForm()

    context = {
        # 'x':x,
        'yields': yields, 
        'yield_form': yield_form, 
        'pine_value': pine_value, 
        'total_cost': value,
        'hawaii_yields': hawaii_yields,
        'pormosa_yields': pormosa_yields,
        'all_categories': all_categories,
    }

    return render(request, 'crop_yield/yield.html', context)


@login_required(login_url='login')
def yield_update(request, pk):
    crop = Yield.objects.get(id=pk)
    if request.method == 'POST':
        form = YieldForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('yield')
    else:
        form = YieldForm(instance=crop)
    context = {'form': form}
    return render(request, 'crop_yield/yield_update.html', context)

def yield_delete(request, pk):
    try:
        yield_obj = Yield.objects.get(id=pk)
        yield_obj.delete()
        return JsonResponse({'success': True})
    except Yield.DoesNotExist:
        return JsonResponse({'success': False})
    

def pine_bad(request):
    category_filter = request.GET.get('category')
    all_categories = Category.objects.all()
    bad_quality = BadPine.objects.all()
    if category_filter:
        bad_quality = bad_quality.filter(category__name=category_filter)

        
    pine_value = BadValuePine.objects.first()
    total_yield = BadPine.objects.aggregate(total_yield=models.Sum('number_yield'))['total_yield']
    value = None

    # x = Yield.objects.values('harvest_date').annotate(item_count=Count('id'))
    hawaii_yields = (
        BadPine.objects.filter(category__name='Hawaii')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )
    pormosa_yields = (
        BadPine.objects.filter(category__name='Pormosa')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )

    hawaii_pine_value = BadValuePine.objects.filter(category='5').first()
    pormosa_pine_value = BadValuePine.objects.filter(category='6').first()

    # Calculate the value for each category and each date
    for item in hawaii_yields:
        item['value'] = float(item['total_yield']) * (float(hawaii_pine_value.value) if hawaii_pine_value else 0)

    for item in pormosa_yields:
        item['value'] = float(item['total_yield']) * (float(pormosa_pine_value.value) if pormosa_pine_value else 0)

    if total_yield is not None and pine_value is not None:
        value = total_yield * pine_value.value 

    if request.method == 'POST':
        yield_form = BadPineForm(request.POST)

        if yield_form.is_valid():
            category = yield_form.cleaned_data['category']
            number_yield = yield_form.cleaned_data['number_yield']
            harvest_date = yield_form.cleaned_data['harvest_date']

            # Check if there is an existing yield record for the same date and category
            existing_yield = BadPine.objects.filter(category=category, harvest_date=harvest_date).first()

            if existing_yield:
                existing_yield.number_yield += number_yield
                existing_yield.value = pine_value
                existing_yield.product = existing_yield.number_yield * pine_value.value
                existing_yield.save()
            else:
                new_yield = yield_form.save(commit=False)
                new_yield.value = pine_value
                new_yield.product = new_yield.number_yield * pine_value.value
                new_yield.save()

            return redirect('bad_pine')
    else:
        yield_form = BadPineForm()

    context = {
        # 'x':x,
        'bad_quality': bad_quality, 
        'yield_form': yield_form, 
        'pine_value': pine_value, 
        'total_cost': value,
        'hawaii_yields': hawaii_yields,
        'pormosa_yields': pormosa_yields,
        'all_categories': all_categories,
    }

    return render(request, 'crop_yield/badpine.html', context)

def bad_pine_update(request, pk):
    crop = BadPine.objects.get(id=pk)
    if request.method == 'POST':
        form = BadPineForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('bad_pine')
    else:
        form = BadPineForm(instance=crop)
    context = {'form': form}
    return render(request, 'crop_yield/bad_pine_update.html', context)

def yield_delete(request, pk):
    try:
        yield_obj = BadPine.objects.get(id=pk)
        yield_obj.delete()
        return JsonResponse({'success': True})
    except BadPine.DoesNotExist:
        return JsonResponse({'success': False})