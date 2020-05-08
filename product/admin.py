from django.contrib import admin
from .models import Product, Specification, Photo, ValueSpecification, Comment


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'body', 'created', 'active')
    list_filter = ('active', 'created', 'user')
    # search_fields = ('user', '', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Specification)
admin.site.register(Photo)
admin.site.register(ValueSpecification)
