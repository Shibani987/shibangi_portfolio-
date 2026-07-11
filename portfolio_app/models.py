from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_page", kwargs={"slug": self.slug})


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Sub category"
        verbose_name_plural = "Sub categories"

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_page", kwargs={"slug": self.slug})


class ProductCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="product_categories",
        blank=True,
        null=True,
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="product_categories",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(category__isnull=False, subcategory__isnull=True)
                    | models.Q(category__isnull=True, subcategory__isnull=False)
                ),
                name="product_category_has_one_parent",
            ),
            models.UniqueConstraint(
                fields=["category", "name"],
                condition=models.Q(category__isnull=False),
                name="unique_product_category_per_category",
            ),
            models.UniqueConstraint(
                fields=["subcategory", "name"],
                condition=models.Q(subcategory__isnull=False),
                name="unique_product_category_per_subcategory",
            ),
        ]

    def __str__(self):
        parent = self.subcategory or self.category
        if parent:
            return f"{self.name} ({parent.name})"
        return self.name

    def clean(self):
        super().clean()
        if bool(self.category) == bool(self.subcategory):
            raise ValidationError("Select either a category or a sub category, not both.")
        if self.category and self.category.slug == "graphic-design":
            raise ValidationError("Graphic Design products must be added under a Graphic Design sub category.")


class ProductItem(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="portfolio_products/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["category", "name"], name="unique_product_item_per_category"),
        ]

    def __str__(self):
        return self.name


class SiteProfile(models.Model):
    name = models.CharField(max_length=120, default="Shibangi Khan")
    about_image = models.ImageField(upload_to="about_images/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return self.name


class Education(models.Model):
    STATUS_ONGOING = "ongoing"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
    ]

    degree_name = models.CharField(max_length=160, blank=True)
    field_of_study = models.CharField(max_length=160, blank=True)
    institution_name = models.CharField(max_length=180, blank=True)
    university_board = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=160, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    is_ongoing = models.BooleanField(default=False)
    cgpa_percentage = models.CharField("CGPA / Percentage", max_length=80, blank=True)
    description = models.TextField(blank=True)
    certificate_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-start_date", "-created_at"]

    def __str__(self):
        return self.degree_name or self.institution_name or "Education entry"

    @property
    def display_period(self):
        start = self.start_date.year if self.start_date else ""
        end = self.end_date.year if self.end_date else ("Current" if self.is_ongoing else "")
        if start and end:
            return f"{start} - {end}"
        return str(start or end)

    @property
    def meta_line(self):
        parts = [part for part in [self.university_board, self.display_period, self.cgpa_percentage] if part]
        return " | ".join(parts)


class Experience(models.Model):
    FULL_TIME = "full_time"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"
    CONTRACT = "contract"
    PART_TIME = "part_time"
    EMPLOYMENT_TYPE_CHOICES = [
        (FULL_TIME, "Full-time"),
        (INTERNSHIP, "Internship"),
        (FREELANCE, "Freelance"),
        (CONTRACT, "Contract"),
        (PART_TIME, "Part-time"),
    ]

    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"
    WORK_MODE_CHOICES = [
        (REMOTE, "Remote"),
        (ONSITE, "Onsite"),
        (HYBRID, "Hybrid"),
    ]

    job_title = models.CharField(max_length=160, blank=True)
    company_name = models.CharField(max_length=180, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True)
    location = models.CharField(max_length=160, blank=True)
    work_mode = models.CharField("Remote / Onsite / Hybrid", max_length=20, choices=WORK_MODE_CHOICES, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)
    company_logo = models.ImageField(upload_to="experience_logos/", blank=True, null=True)
    company_website = models.URLField(blank=True)
    project_link = models.URLField(blank=True)
    certificate_offer_letter = models.FileField(upload_to="experience_documents/", blank=True, null=True)
    experience_summary = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    technologies_used = models.CharField(max_length=240, blank=True)
    achievements = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-start_date", "-created_at"]

    def __str__(self):
        return self.job_title or self.company_name or "Experience entry"

    @property
    def display_period(self):
        start = self.start_date.year if self.start_date else ""
        end = "Current" if self.currently_working else (self.end_date.year if self.end_date else "")
        if start and end:
            return f"{start} - {end}"
        return str(start or end)

    @property
    def meta_line(self):
        parts = [
            self.display_period,
            self.get_employment_type_display() if self.employment_type else "",
            self.get_work_mode_display() if self.work_mode else "",
            self.location,
        ]
        return " | ".join(part for part in parts if part)


class HighlightPost(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    tag = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to="highlight_images/", blank=True, null=True)
    document = models.FileField(upload_to="highlight_documents/", blank=True, null=True)
    external_link = models.URLField("Link", blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("highlight_detail", kwargs={"pk": self.pk})

    @property
    def time_ago(self):
        delta = timezone.now() - self.created_at
        seconds = max(int(delta.total_seconds()), 0)
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if seconds < 60:
            return "just now"
        if minutes < 60:
            return f"{minutes}m ago"
        if hours < 24:
            return f"{hours}h ago"
        if days < 7:
            return f"{days}d ago"
        weeks = days // 7
        if weeks < 5:
            return f"{weeks}w ago"
        months = days // 30
        if months < 12:
            return f"{months}mo ago"
        years = days // 365
        return f"{years}y ago"


class HighlightLike(models.Model):
    post = models.ForeignKey(HighlightPost, on_delete=models.CASCADE, related_name="likes")
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "session_key"], name="unique_highlight_like_per_session"),
        ]

    def __str__(self):
        return f"{self.post.title} liked by {self.session_key}"
