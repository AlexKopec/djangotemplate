from django.contrib import admin

# Register your models here.
from .models import *


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['name', 'user', 'servings', 'prep_time', 'cook_time', 'directions', 'description', 'profile_pic', 'main_ingredient']}),
        ('Date Information',    {'fields': ['created_date']})
    ]
    inlines = [IngredientInline]


class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'food', 'recipe', 'amount', 'unit']


class MenuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['id', 'owner']}),
        ('Date Information', {'fields': ['week_of']})
    ]
    inlines = [RecipeInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Unit)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FoodCategory)
admin.site.register(RecipeCategory)
admin.site.register(Menu)
