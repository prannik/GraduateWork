from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Product, ProductCategory, ProductReview, ProductReviewLike, ProductInBasket
from .forms import ProductReviewForm


def product_list(request):
    category = ProductCategory.objects.all()
    products = Product.objects.filter(status=False, date__lte=timezone.now()).order_by('date')
    return render(request, 'store/product_list.html', {'products': products, 'category': category})

def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    reviews = ProductReview.objects.filter(product=product_pk)
    if reviews:
        sum_mark = 0
        for i in reviews:
            sum_mark += int(i.mark)
        product.rating = sum_mark / len(reviews)
    product.save()
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews})

def product_review(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review_form = form.save(commit=False)
            review_form.author = request.user
            review_form.product = product
            review_form.save()
            return redirect('product_detail', product_pk=product.pk)
    else:
        review_form = ProductReviewForm()
        return render(request, 'store/product_review.html', {'review_form': review_form})

def review_delete(request, product_pk, review_pk):
    product = get_object_or_404(Product, pk=product_pk)
    review = get_object_or_404(ProductReview, pk=review_pk)
    review.delete()
    product.save()
    return redirect('product_detail', product_pk=product.pk)

def review_edit(request, product_pk, review_pk):
    product = get_object_or_404(Product, pk=product_pk)
    review = get_object_or_404(ProductReview, pk=review_pk)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('product_detail', product_pk=product.pk)
    else:
        form = ProductReviewForm(instance=review)
        return render(request, 'store/review_edit.html', {'form': form})

def review_like_or_dislike(request, product_pk, review_pk, is_like):
    product = get_object_or_404(Product, pk=product_pk)
    review = get_object_or_404(ProductReview, pk=review_pk)
    old_like = ProductReviewLike.objects.filter(user=request.user, for_review=review)
    if old_like:
        like = ProductReviewLike.objects.get(user=request.user, for_review=review)
        if like.like_or_dislike == 'like' and is_like == 'like':
            like.delete()
            review.likes -= 1
            review.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'dislike':
            like.delete()
            review.dislikes -= 1
            review.save()
        elif like.like_or_dislike == 'like' and is_like == 'dislike':
            like.like_or_dislike = 'dislike'
            like.save()
            review.dislikes += 1
            review.likes -= 1
            review.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'like':
            like.like_or_dislike = "like"
            like.save()
            review.dislikes -= 1
            review.likes += 1
            review.save()
    else:
        new_like = ProductReviewLike(user=request.user, for_review=review, like_or_dislike=is_like)
        new_like.save()
        if is_like == 'like':
            review.likes += 1
            review.save()
        elif is_like == 'dislike':
            review.dislikes += 1
            review.save()
    return redirect('product_detail', product_pk=product.pk)

def basket(request):
    products = ProductInBasket.objects.filter(basket=request.user.id)

    sum_price = sum([product.product.price for product in products])
    return render(request, 'store/basket.html', {'products': products, 'sum_price': sum_price})

def main_page(request):
    return render(request, 'store/main.html')
