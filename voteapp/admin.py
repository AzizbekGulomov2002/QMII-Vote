from django.contrib import admin
from .models import Category, CategoryItem, Vote,Faculty, Kafedra, Professor,VoteItems, Option
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryItem)

admin.site.register(Faculty)
admin.site.register(Kafedra)
admin.site.register(Professor)
admin.site.register(VoteItems)


class VoteItemsInline(admin.TabularInline):
    model = VoteItems
    extra = 1  
    
class VoteAdmin(admin.ModelAdmin):
    inlines = [VoteItemsInline]
admin.site.register(Vote, VoteAdmin)
admin.site.register(Option)
