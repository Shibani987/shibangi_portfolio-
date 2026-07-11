from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Education, Experience, HighlightPost, ProductCategory, ProductItem, SiteProfile, SubCategory


class DirectProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1
    fields = ("name", "description", "order")
    fk_name = "category"


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ("name", "slug", "description", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "image_preview")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    readonly_fields = ("image_preview",)
    fields = ("name", "slug", "description", "image", "image_preview", "order")

    def get_inline_instances(self, request, obj=None):
        if obj and obj.slug == "graphic-design":
            inline_classes = (SubCategoryInline,)
        else:
            inline_classes = (DirectProductCategoryInline,)
        return [inline(self.model, self.admin_site) for inline in inline_classes]

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 72px; border-radius: 6px;" />', obj.image.url)
        return "-"


class SubCategoryProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1
    fields = ("name", "description", "order")
    fk_name = "subcategory"


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug", "order")
    list_filter = ("category",)
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description", "category__name")
    fields = ("category", "name", "slug", "description", "order")
    inlines = (SubCategoryProductCategoryInline,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(slug="graphic-design")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1
    fields = ("name", "description", "image", "order")


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_name", "order")
    list_filter = ("category", "subcategory")
    list_editable = ("order",)
    search_fields = ("name", "description", "category__name", "subcategory__name")
    fields = ("category", "subcategory", "name", "description", "order")
    inlines = (ProductItemInline,)

    @admin.display(description="Parent")
    def parent_name(self, obj):
        return obj.subcategory or obj.category

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.exclude(slug="graphic-design")
        if db_field.name == "subcategory":
            kwargs["queryset"] = SubCategory.objects.filter(category__slug="graphic-design")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order", "image_preview")
    list_filter = ("category__category", "category__subcategory", "category")
    list_editable = ("order",)
    search_fields = (
        "name",
        "description",
        "category__name",
        "category__category__name",
        "category__subcategory__name",
    )
    readonly_fields = ("image_preview",)
    fields = ("category", "name", "description", "image", "image_preview", "order")

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 72px; border-radius: 6px;" />', obj.image.url)
        return "-"


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "cv_url", "about_image_preview", "updated_at")
    readonly_fields = ("about_image_preview", "updated_at")
    fields = ("name", "about_image", "about_image_preview", "cv_url", "updated_at")

    def has_add_permission(self, request):
        if SiteProfile.objects.exists():
            return False
        return super().has_add_permission(request)

    @admin.display(description="About image preview")
    def about_image_preview(self, obj):
        if obj.about_image:
            return format_html('<img src="{}" style="height: 96px; border-radius: 8px;" />', obj.about_image.url)
        return "-"


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree_name", "institution_name", "university_board", "current_status", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("current_status", "is_ongoing", "is_published", "university_board")
    search_fields = ("degree_name", "field_of_study", "institution_name", "university_board", "location")
    readonly_fields = ("created_at", "updated_at")
    fields = (
        "degree_name",
        "field_of_study",
        "institution_name",
        "university_board",
        "location",
        "start_date",
        "end_date",
        "current_status",
        "is_ongoing",
        "cgpa_percentage",
        "description",
        "certificate_url",
        "order",
        "is_published",
        "created_at",
        "updated_at",
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("job_title", "company_name", "employment_type", "currently_working", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("employment_type", "work_mode", "currently_working", "is_published")
    search_fields = ("job_title", "company_name", "location", "technologies_used", "experience_summary")
    readonly_fields = ("logo_preview", "created_at", "updated_at")
    fields = (
        "job_title",
        "company_name",
        "employment_type",
        "location",
        "work_mode",
        "start_date",
        "end_date",
        "currently_working",
        "company_logo",
        "logo_preview",
        "company_website",
        "project_link",
        "certificate_offer_letter",
        "experience_summary",
        "responsibilities",
        "technologies_used",
        "achievements",
        "order",
        "is_published",
        "created_at",
        "updated_at",
    )

    @admin.display(description="Logo preview")
    def logo_preview(self, obj):
        if obj.company_logo:
            return format_html('<img src="{}" style="height: 48px; border-radius: 6px;" />', obj.company_logo.url)
        return "-"


@admin.register(HighlightPost)
class HighlightPostAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "has_image", "has_document", "likes_count", "order", "is_published", "created_at")
    list_editable = ("order", "is_published")
    search_fields = ("title", "description", "tag")
    list_filter = ("is_published", "tag", "created_at")
    readonly_fields = ("image_preview", "likes_count", "created_at", "updated_at")
    fields = (
        "title",
        "description",
        "tag",
        "image",
        "image_preview",
        "document",
        "external_link",
        "order",
        "is_published",
        "likes_count",
        "created_at",
        "updated_at",
    )

    @admin.display(boolean=True, description="Image")
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(boolean=True, description="Document")
    def has_document(self, obj):
        return bool(obj.document)

    @admin.display(description="Image preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 96px; border-radius: 8px;" />', obj.image.url)
        return "-"
