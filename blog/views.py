
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Tag, Like, Category
from .forms import PostForm, CommentForm, TagForm


def post_list(request):
    category = Category.objects.all()
    posts = Post.objects.filter(draft=False, date__lte=timezone.now()).order_by('date')
    drafts_counter = len(Post.objects.filter(draft=True))
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'drafts_counter': drafts_counter,
                                                   'category': category})

def cat_post_list(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    posts = Post.objects.filter(category=category,draft=False,  date__lte=timezone.now()).order_by('date')
    return render(request, 'blog/category_post_list.html', {'posts': posts,
                                                            'category': category})

def draft_list(request):
    drafts = Post.objects.filter(draft=True, author=request.user, date__lte=timezone.now()).order_by('date')
    return render(request, 'blog/draft_list.html', {'posts': drafts})

def published_draft(post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.draft = False
    post.date = timezone.now()
    post.save()
    return redirect('post_list')

def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.counter += 1
    post.save()
    comments = Comment.objects.filter(post=post_pk)
    comments.counter = len(comments)
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comments.counter': comments.counter})

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

def tag_post(request, tag_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)
    posts = tag.POSTS.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def tag_add(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            post.tag.add(tag)
            post.save()

            return redirect('post_detail', post_pk=post.pk)
    else:
        form = TagForm()
    return render(request, 'blog/tag_add.html', {'form': form})

def tag_delete(request, post_pk, tag_pk):
    post = get_object_or_404(Post, pk=post_pk)
    tag = get_object_or_404(Tag, pk=tag_pk)
    tag.delete()
    post.save()
    return redirect('post_detail', post_pk=post.pk)

def like_or_dislike(request, post_pk, is_like, point):
    try:
        post = Post.objects.get(id=post_pk)
    except:
        raise Http404("Пост не найден!")
    old_like = Like.objects.filter(user=request.user, for_post=post)
    if old_like:
        like = Like.objects.get(user=request.user, for_post=post)
        if like.like_or_dislike == 'like' and is_like == 'like':
            like.delete()
            post.likes -= 1
            post.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'dislike':
            like.delete()
            post.dislikes -= 1
            post.save()
        elif like.like_or_dislike == 'like' and is_like == 'dislike':
            like.like_or_dislike = 'dislike'
            like.save()
            post.dislikes += 1
            post.likes -= 1
            post.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'like':
            like.like_or_dislike = "like"
            like.save()
            post.dislikes -= 1
            post.likes += 1
            post.save()
    else:
        new_like = Like(user=request.user, for_post=post, like_or_dislike=is_like)
        new_like.save()
        if is_like == 'like':
            post.likes += 1
            post.save()
        elif is_like == 'dislike':
            post.dislikes += 1
            post.save()
    if point == 'post_list':
        return redirect('post_list')
    elif point == 'post_detail':
        return redirect('post_detail', post_pk=post.pk)


