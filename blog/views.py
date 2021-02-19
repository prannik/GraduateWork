
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.filter(date__lte=timezone.now()).order_by('date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.counter += 1
    post.save()
    comments = Comment.objects.filter(post=post_pk)
    comments.counter = len(comments)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_new.html', {'form': form})


def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_pk=post.pk)

    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('post_list')


def post_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.likes += 1
    post.save()
    return redirect('post_detail', post_pk=post.pk)


def post_dislike(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.dislikes += 1
    post.save()
    return redirect('post_detail', post_pk=post.pk)


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.author = request.user
            comment_form.post = post
            comment_form.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        comment_form = CommentForm()
        return render(request, 'blog/post_comment.html', {'comment_form': comment_form})


def comment_delete(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    post.save()
    return redirect('post_detail', post_pk=post.pk)


def comment_edit(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'blog/comment_edit.html', {'form': form})
