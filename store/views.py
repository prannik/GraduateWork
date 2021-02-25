from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Product, ProductComment, Like, Category, ProductReview
from .forms import ProductCommentForm


def product_list(request):
    category = Category.objects.all()
    products = Product.objects.filter(date__lte=timezone.now()).order_by('date')
    return render(request, 'store/product_list.html', {'products': products,
                                                   	'category': category})


def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    product.counter += 1
    product.save()
    comments = Comment.objects.filter(product=product_pk)
    comments.counter = len(comments)
    review = Review.objects.filter(product=product_pk)
    sum_mark = 0
    for i in review:
        sum_mark += i.mark
    review_mark = sum_mark/len(review)
    return render(request, 'store/product_detail.html', {'product': product,
                                                         'comments': comments,
                                                         'comments.counter': comments.counter,
                                                         'review_mark': review_mark})


def product_comment(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == 'product':
        form = ProductCommentForm(request.product)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.author = request.user
            comment_form.product = product
            comment_form.save()
            return redirect('product_detail', product_pk=product.pk)
    else:
        comment_form = ProductCommentForm()
        return render(request, 'store/product_comment.html', {'comment_form': comment_form})


def comment_delete(request, product_pk, comment_pk):
    product = get_object_or_404(Product, pk=product_pk)
    comment = get_object_or_404(ProductComment, pk=comment_pk)
    comment.delete()
    product.save()
    return redirect('product_detail', product_pk=product.pk)


def comment_edit(request, product_pk, comment_pk):
    product = get_object_or_404(Product, pk=product_pk)
    comment = get_object_or_404(ProductComment, pk=comment_pk)
    if request.method == 'product':
        form = ProductCommentForm(request.product, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('product_detail', product_pk=product.pk)
    else:
        form = ProductCommentForm(instance=comment)
        return render(request, 'store/comment_edit.html', {'form': form})

#
# def like_or_dislike(request, product_pk, is_like, point):
#     try:
#         product = Product.objects.get(id=product_pk)
#     except:
#         raise Http404("Пост не найден!")
#     old_like = Like.objects.filter(user=request.user, for_product=product)
#     if old_like:
#         like = Like.objects.get(user=request.user, for_product=product)
#         if like.like_or_dislike == 'like' and is_like == 'like':
#             like.delete()
#             product.likes -= 1
#             product.save()
#         elif like.like_or_dislike == 'dislike' and is_like == 'dislike':
#             like.delete()
#             product.dislikes -= 1
#             product.save()
#         elif like.like_or_dislike == 'like' and is_like == 'dislike':
#             like.like_or_dislike = 'dislike'
#             like.save()
#             product.dislikes += 1
#             product.likes -= 1
#             product.save()
#         elif like.like_or_dislike == 'dislike' and is_like == 'like':
#             like.like_or_dislike = "like"
#             like.save()
#             product.dislikes -= 1
#             product.likes += 1
#             product.save()
#     else:
#         new_like = Like(user=request.user, for_product=product, like_or_dislike=is_like)
#         new_like.save()
#         if is_like == 'like':
#             product.likes += 1
#             product.save()
#         elif is_like == 'dislike':
#             product.dislikes += 1
#             product.save()
#     if point == 'product_list':
#         return redirect('product_list')
#     elif point == 'product_detail':
#         return redirect('product_detail', product_pk=product.pk)
