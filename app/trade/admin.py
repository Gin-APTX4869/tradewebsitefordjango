from django.contrib import admin
from .models import Profile, Category, Goods, Seek, Tag

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'nickname', 'grade', 'college',)
	search_fields = ['grade', 'college',]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	pass	

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
	list_display = ('goods_title', 'goods_price', 'kw', 'timestamp', 'updated')
	list_per_page = 30
	search_fields = ['goods_title', 'goods_price',]

@admin.register(Seek)
class SeekAdmin(admin.ModelAdmin):
	list_display = ('name', 'timestamp', 'kw',)
	search_fields = ['name', 'kw']

