from datetime import timedelta

from django.db import migrations
from django.utils import timezone


POSTS = [
    (
        "Creative Process",
        "A behind-the-scenes look at how concepts turn into polished visual stories.",
        "New",
        24,
        1,
        timedelta(hours=2),
    ),
    (
        "Brand Identity",
        "Recent work focused on typography, color systems, and digital storytelling.",
        "Featured",
        41,
        2,
        timedelta(days=1),
    ),
    (
        "Visual Experiments",
        "Exploring new formats and bold compositions for future campaigns.",
        "Trending",
        17,
        3,
        timedelta(days=3),
    ),
]


def seed_highlight_posts(apps, schema_editor):
    HighlightPost = apps.get_model("portfolio_app", "HighlightPost")
    now = timezone.now()

    for title, description, tag, likes_count, order, age in POSTS:
        post, created = HighlightPost.objects.update_or_create(
            title=title,
            defaults={
                "description": description,
                "tag": tag,
                "likes_count": likes_count,
                "order": order,
                "is_published": True,
            },
        )
        if created:
            HighlightPost.objects.filter(pk=post.pk).update(created_at=now - age)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0012_highlightpost_highlightlike"),
    ]

    operations = [
        migrations.RunPython(seed_highlight_posts, migrations.RunPython.noop),
    ]
