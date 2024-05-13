from django import template


register = template.Library()


@register.inclusion_tag('account/recent_activity.html', name='last_activity')
def get_recent_activity(user, posts_count=3):
    return {
        "posts": user.posts.all().order_by('-published')[:posts_count]
    }
