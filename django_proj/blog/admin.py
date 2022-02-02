from django.contrib import admin

# Register your models here.
from .models import Post,Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Post)
admin.site.register(Category,CategoryAdmin)

