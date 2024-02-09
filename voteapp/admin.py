from django.contrib import admin
from .models import Category, CategoryItem, Vote,Faculty, Kafedra, Professor,VoteItems
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryItem)

admin.site.register(Vote)
admin.site.register(VoteItems)
admin.site.register(Faculty)
admin.site.register(Kafedra)
admin.site.register(Professor)
