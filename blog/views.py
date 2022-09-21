from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Tag, PostLike, CommentLike, Category
from .forms import PostForm, CommentForm, TagForm


def post_list(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(draft=False, date__lte=timezone.now()).order_by('date')
    drafts_counter = len(Post.objects.filter(draft=True))
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'drafts_counter': drafts_counter,
                                                   'categories': categories})


def cat_post_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, draft=False, date__lte=timezone.now()).order_by('date')
    categories = Category.objects.all()
    drafts_counter = len(Post.objects.filter(draft=True))
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'categories': categories,
                                                   'drafts_counter': drafts_counter,
                                                   'category': category})


def draft_list(request):
    drafts = Post.objects.filter(draft=True, author=request.user, date__lte=timezone.now()).order_by('date')
    categories = Category.objects.all()
    drafts_counter = 0
    return render(request, 'blog/post_list.html', {
        'posts': drafts,
        'drafts_counter': drafts_counter,
        'categories': categories})


def published_draft(slug):
    post = get_object_or_404(Post, slug=slug)
    post.draft = False
    post.date = timezone.now()
    post.save()
    return redirect('post_list')


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    categories = Category.objects.all()
    comments = Comment.objects.filter(post=post)
    comments.counter = len(comments)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tags = Tag.objects.filter(text=tag)
            if len(tags) == 0:
                tag.save()
                post.tag.add(tag)
            else:
                post.tag.add(tags[0])
            post.save()

            return redirect('post_detail', slug=slug)
    else:
        form = TagForm()

    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'categories': categories,
                                                     'comments': comments,
                                                     'form': form,
                                                     'comments.counter': comments.counter})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = post.title
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
        return render(request, 'blog/edit.html', {'form': form})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=slug)

    else:
        form = PostForm(instance=post)
        return render(request, 'blog/edit.html', {'form': form})


def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post_list')


def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.author = request.user
            comment_form.post = post
            comment_form.save()
            return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()
        return render(request, 'blog/edit.html', {'form': comment_form})


def comment_delete(request, slug, comment_pk):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    post.save()
    return redirect('post_detail', slug=slug)


def comment_edit(request, slug, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'blog/edit.html', {'form': form})


def tag_post(request, tag_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)
    posts = tag.POSTS.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def tag_delete(request, slug, tag_pk):
    post = get_object_or_404(Post, slug=slug)
    tag = get_object_or_404(Tag, pk=tag_pk)
    tag.delete()
    post.save()
    return redirect('post_detail', slug=slug)


def post_like_or_dislike(request, slug, is_like, point):
    post = get_object_or_404(Post, slug=slug)
    old_like = PostLike.objects.filter(user=request.user, for_post=post)

    if old_like:
        like = PostLike.objects.get(user=request.user, for_post=post)
        if like.like_or_dislike == 'like' and is_like == 'like':
            like.delete()
            post.post_likes -= 1
            post.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'dislike':
            like.delete()
            post.post_dislikes -= 1
            post.save()
        elif like.like_or_dislike == 'like' and is_like == 'dislike':
            like.like_or_dislike = 'dislike'
            like.save()
            post.post_dislikes += 1
            post.post_likes -= 1
            post.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'like':
            like.like_or_dislike = "like"
            like.save()
            post.post_dislikes -= 1
            post.post_likes += 1
            post.save()
    else:
        new_like = PostLike(user=request.user, for_post=post, like_or_dislike=is_like)
        new_like.save()
        if is_like == 'like':
            post.post_likes += 1
            post.save()
        elif is_like == 'dislike':
            post.post_dislikes += 1
            post.save()
    if point == 'post_list':
        return redirect('post_list')
    elif point == 'post_detail':
        return redirect('post_detail', slug=slug)


def comment_like_or_dislike(request, slug, comment_pk, is_like):
    comment = get_object_or_404(Comment, pk=comment_pk)

    old_like = CommentLike.objects.filter(user=request.user, for_com=comment)

    if old_like:
        like = CommentLike.objects.get(user=request.user, for_com=comment)
        if like.like_or_dislike == 'like' and is_like == 'like':
            like.delete()
            comment.comment_likes -= 1
            comment.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'dislike':
            like.delete()
            comment.comment_dislikes -= 1
            comment.save()
        elif like.like_or_dislike == 'like' and is_like == 'dislike':
            like.like_or_dislike = 'dislike'
            like.save()
            comment.comment_dislikes += 1
            comment.comment_likes -= 1
            comment.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'like':
            like.like_or_dislike = "like"
            like.save()
            comment.comment_dislikes -= 1
            comment.comment_likes += 1
            comment.save()
    else:
        new_like = CommentLike(user=request.user, for_com=comment, like_or_dislike=is_like)
        new_like.save()
        if is_like == 'like':
            comment.comment_likes += 1
            comment.save()
        elif is_like == 'dislike':
            comment.comment_dislikes += 1
            comment.save()
    return redirect('post_detail', slug=slug)
