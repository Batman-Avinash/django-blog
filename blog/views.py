from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count


from blog.models import Post, Comment
from blog.forms import EmailPostForm, CommentForm
from taggit.models import Tag


# class PostListView(ListView):
# 	queryset = Post.published.all()
# 	context_object_name = 'posts'
# 	paginate_by = 3
# 	template_name = 'blog/post/list.html'
		


def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])

	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an Integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of result
		posts = paginator.page(paginator.num_pages)

	context = {'page': page,
				'posts': posts,
				'tag': tag}
	return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
									status='published',
									publish__year=year,
									publish__month=month,
									publish__day=day)
	
	# List of active comments for this post
	comments = post.comments.filter(active=True)

	new_comment = None

	if request.method == 'POST':
		# A comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Create comment object but don't save it to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to comment
			new_comment.post = post
			# Save the comment to database
			new_comment.save()
	else:
		comment_form = CommentForm()

	context = {
		'post': post,
		'comments': comments,
		'new_comment': new_comment,
		'comment_form': comment_form
	}
	return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
	# Retrive Post by ID
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False

	if request.method == 'POST':
		# Form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Form field passes validation
			cd = form.cleaned_data
			# ... now send e-mail
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], 
				cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, 
				cd['name'], cd['comment'])
			send_mail = (subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	context = {'post': post,'form': form, 'sent': sent}
	return render(request, 'blog/post/share.html', context)