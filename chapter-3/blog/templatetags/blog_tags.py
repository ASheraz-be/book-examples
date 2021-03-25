from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name="mark")
def mark_down(text):
	return mark_safe(markdown.markdown(text))

@register.simple_tag(name="post_count")
def total_posts():
	return Post.draft.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def latest_posts(count=5):
	latest_posts_are = Post.draft.order_by('-publish')[:count]
	return {"latest_posts": latest_posts_are}

@register.simple_tag()
def commented_posts(count=5):
	return Post.draft.annotate(
			total_comments = Count("comments")
		).order_by("-total_comments")[:count]