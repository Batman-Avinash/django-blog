from django.urls import path
from blog.views import post_list, post_detail, post_share


app_name = 'blog'


urlpatterns = [
	# path('', PostListView.as_view(), name='blog-home'),
	path('', post_list, name='blog-home'),
	path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/',
		post_detail, name='post_detail'),
	path('<int:post_id>/share/', post_share, name='post_share')
]