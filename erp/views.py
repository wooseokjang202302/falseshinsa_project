from django.utils import timezone
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Inbound, Outbound

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/product')
    else:
        return redirect('/sign-in')

@login_required
def append_product(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        return render(request, 'erp/append_product.html')
    elif request.method == 'POST':
        code = request.POST.get('code', '')
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        size = request.POST.get('size', '')

        if code == '':
            return render(request, 'erp/append_product.html', {'error': '상품코드를 작성해주세요'})
        elif name == '':
            return render(request, 'erp/append_product.html', {'error': '상품명을 작성해주세요'})
        elif description == '':
            return render(request, 'erp/append_product.html', {'error': '상품설명을 작성해주세요'})
        elif price == '':
            return render(request, 'erp/append_product.html', {'error': '가격을 작성해주세요'})
        elif size == '':
            return render(request, 'erp/append_product.html', {'error': '사이즈를 선택해주세요'})

        exist_product_code = Product.objects.filter(code=code)
        if exist_product_code:
            return render(request, 'erp/append_product.html', {'error': '존재하는 상품코드입니다.'})
        
        exist_product_name = Product.objects.filter(name=name)
        if exist_product_name:
            return render(request, 'erp/append_product.html', {'error': '존재하는 상품명입니다.'})    
        
        new_product = Product(code=code, name=name, description=description, price=price, size=size)
        new_product.save()  # 데이터베이스에 저장하기

        return redirect('/')
    

def product_view(request):
    if request.method == 'GET':
        product_list = Product.objects.all()
        return render(request, 'erp/show_product.html', {'product_list': product_list})
    
@login_required
def product_edit(request, product_code):
    product = get_object_or_404(Product, code=product_code)

    if request.method == 'POST':
        product.name = request.POST.get('name', '')
        product.description = request.POST.get('description', '')
        product.price = request.POST.get('price', '')
        product.size = request.POST.get('size', '')

        if product.name == '':
            return render(request, 'erp/edit_product.html', {'error': '상품명을 작성해주세요'})
        elif product.description == '':
            return render(request, 'erp/edit_product.html', {'error': '상품설명을 작성해주세요'})
        elif product.price == '':
            return render(request, 'erp/edit_product.html', {'error': '가격을 작성해주세요'})
        elif product.size == '':
            return render(request, 'erp/edit_product.html', {'error': '사이즈를 선택해주세요'})
        
        exist_product_name = Product.objects.filter(name=product.name).exclude(id=product.id).exists()
        if exist_product_name:
            return render(request, 'erp/edit_product.html', {'error': '존재하는 상품명입니다.'})

        product.save()

        return redirect('/product/')

    context = {
            'product': product,
    }
    return render(request, 'erp/edit_product.html', context)

@login_required
@transaction.atomic
def product_add(request, product_code):
    product = get_object_or_404(Product, code=product_code)

    if request.method == 'POST':
        add_stock = request.POST.get('add_stock', '')
        current_stock = product.stock

        if add_stock == '':
            return render(request, 'erp/add_product.html', {'error': '입고 수량을 입력해주세요'})

        if add_stock != '0':
            current_stock += int(add_stock)

            # Inbound 객체 생성 및 저장
            inbound = Inbound(
                product=product,
                quantity=int(add_stock),
                inbound_date=timezone.now(),
                price=product.price
            )
            inbound.save()


        product.stock = current_stock
        product.save()

        return redirect('/product/')

    context = {
        'product': product,
    }
    return render(request, 'erp/add_product.html', context)


@login_required
@transaction.atomic
def product_subtract(request, product_code):
    product = get_object_or_404(Product, code=product_code)

    if request.method == 'POST':
        subtract_stock = request.POST.get('subtract_stock', '')
        current_stock = product.stock

        if subtract_stock == '':
            return render(request, 'erp/subtract_product.html', {'error': '출고 수량을 입력해주세요'})

        if subtract_stock != '0':
            if current_stock >= int(subtract_stock):
                current_stock -= int(subtract_stock)
            else:
                return render(request, 'erp/subtract_product.html', {'error': '출고 수량은 현재 수량보다 많을 수 없습니다.'})

        # Inbound 객체 생성 및 저장
        outbound = Outbound(
            product=product,
            quantity=int(subtract_stock),
            outbound_date=timezone.now(),
            price=product.price
        )
        outbound.save()

        product.stock = current_stock
        product.save()

        return redirect('/product/')

    context = {
        'product': product,
    }
    return render(request, 'erp/subtract_product.html', context)