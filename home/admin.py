from django.contrib import admin
from .models import Blog,Product,Productsimage,Category,ProductColors,ProductSizes

class BlogAdmin(admin.ModelAdmin):
    list_display = ['creator','title','created_at']
    list_filter = ['title']
    search_fields = ('creator','title')
    fieldsets = (
        ('Blogs',{'fields':('title','info','icon')}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # فقط وقتی داره ساخته میشه، creator رو ست می‌کنیم
            obj.creator = request.user
        obj.save()

class ProductsimageInline(admin.TabularInline):
    model = Productsimage
    extra = 1  # How many empty image slots to show by default

# سایزهای محصول
class ProductSizesInline(admin.TabularInline):
    model = ProductSizes
    extra = 1

# رنگ‌های محصول
class ProductColorsInline(admin.TabularInline):
    model = ProductColors
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'price')  # Show in list view
    inlines = [ProductsimageInline,ProductColorsInline,ProductSizesInline]    # Allow inline image adding/editing


class ProductsimageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Show title in the admin list view
    search_fields = ('title',) 


@admin.register(ProductColors)
class ProductColorsAdmin(admin.ModelAdmin):
    search_fields = ['color']

@admin.register(ProductSizes)
class ProductSizesAdmin(admin.ModelAdmin):
    search_fields = ['size']


admin.site.register(Blog,BlogAdmin)
admin.site.register(Product,ProductAdmin)
# admin.site.register(Productsimage,ProductsimageAdmin)
# admin.site.register(Category,CategoryAdmin)
# admin.site.register(ProductSizes,SizeAdmin)
# admin.site.register(ProductColors,ColorAdmin)