from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag

from .models import Post
from django.core.paginator import Paginator
from .forms import EmailSender, CommentForm
from django.conf import settings
from django.views.decorators.http import require_POST


def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts, "tag": tag})


def post_detail(request, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailSender(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n{cd['name']}'s comment.html:\n {cd['message']}"
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[cd['email_field_to']])
            sent = True
    else:
        form = EmailSender()
    return render(request, 'blog/post/share.html', {"post": post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})
