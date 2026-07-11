from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import Category, Education, Experience, HighlightLike, HighlightPost, SubCategory


def home(request):
    categories = Category.objects.all()
    educations = Education.objects.filter(is_published=True)
    experiences = Experience.objects.filter(is_published=True)
    return render(
        request,
        "index.html",
        {
            "categories": categories,
            "educations": educations,
            "experiences": experiences,
        },
    )


@ensure_csrf_cookie
def highlights(request):
    posts = HighlightPost.objects.filter(is_published=True)
    liked_posts = set()
    if request.session.session_key:
        liked_posts = set(
            HighlightLike.objects.filter(session_key=request.session.session_key).values_list("post_id", flat=True)
        )
    return render(request, "highlights.html", {"posts": posts, "liked_posts": liked_posts})


@ensure_csrf_cookie
def highlight_detail(request, pk):
    post = get_object_or_404(HighlightPost, pk=pk, is_published=True)
    liked_posts = set()
    if request.session.session_key:
        liked_posts = set(
            HighlightLike.objects.filter(session_key=request.session.session_key).values_list("post_id", flat=True)
        )
    return render(request, "highlight_detail.html", {"post": post, "liked_posts": liked_posts})


@require_POST
def like_highlight(request, pk):
    post = get_object_or_404(HighlightPost, pk=pk, is_published=True)
    if not request.session.session_key:
        request.session.create()

    liked = False
    try:
        with transaction.atomic():
            HighlightLike.objects.create(post=post, session_key=request.session.session_key)
            HighlightPost.objects.filter(pk=post.pk).update(likes_count=F("likes_count") + 1)
            liked = True
    except IntegrityError:
        pass

    post.refresh_from_db(fields=["likes_count"])
    return JsonResponse({"likes": post.likes_count, "liked": liked})


def product_page(request, slug):
    if slug == "graphic-design":
        category = Category.objects.filter(slug=slug).first()
        subcategories = SubCategory.objects.filter(category=category) if category else SubCategory.objects.none()
        return render(
            request,
            "products/graphic-design.html",
            {"category": category, "subcategories": subcategories},
        )

    category = Category.objects.filter(slug=slug).prefetch_related("product_categories__products").first()
    if category:
        return render(request, "products/category.html", {"category": category})

    subcategory = (
        SubCategory.objects.filter(slug=slug, category__slug="graphic-design")
        .select_related("category")
        .prefetch_related("product_categories__products")
        .first()
    )
    if subcategory:
        return render(request, "products/subcategory.html", {"subcategory": subcategory})

    return render(request, "404.html", status=404)
