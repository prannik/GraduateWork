from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductReview, ProductReviewLike
from .forms import ProductReviewForm
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    cart_product_form = CartAddProductForm()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'cart_product_form': cart_product_form,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()
    reviews = ProductReview.objects.filter(product=get_object_or_404(Product, slug=slug, available=True))
    if reviews:
        sum_mark = 0
        for i in reviews:
            sum_mark += int(i.mark)
            product.rating = sum_mark / len(reviews)
    else:
        product.rating = 0
    product.save()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'categories': categories,
        'reviews': reviews
    }
    return render(request, 'shop/product/detail.html', context)


def review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review_form = form.save(commit=False)
            review_form.author = request.user
            review_form.product = product
            review_form.save()
            return redirect('product_detail', slug)
    else:
        review_form = ProductReviewForm()
        return render(request, 'blog/edit.html', {'form': review_form})


def review_delete(request, slug, review_pk):
    product = get_object_or_404(Product, slug=slug)
    review = get_object_or_404(ProductReview, pk=review_pk)
    review.delete()
    product.save()
    return redirect('product_detail', slug)


def review_edit(request, slug, review_pk):
    review = get_object_or_404(ProductReview, pk=review_pk)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('product_detail', slug)
    else:
        form = ProductReviewForm(instance=review)
        return render(request, 'blog/edit.html', {'form': form})


def review_like_or_dislike(request, slug, review_pk, is_like):
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
    return redirect('product_detail', slug)
