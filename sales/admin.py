from django.contrib import admin

from .models import *


# Register your models here.
class ComponentAdmin(admin.ModelAdmin):
	list_display = ('name', 'code')
	#fields = (('name', 'code'), 'content')
admin.site.register(Component, ComponentAdmin)

class DatabaseAdmin(admin.ModelAdmin):
	list_display = ('name', 'code', 'component')
	#fields = (('name', 'code'), 'content')
admin.site.register(Database, DatabaseAdmin)

class TableAdmin(admin.ModelAdmin):
	list_display = ('name', 'code','database', 'display_level_of_aggregation', 'display_frequency' )
	#fields = (('name', 'code'), 'content')
admin.site.register(Table, TableAdmin)

class LevelOfAggregationAdmin(admin.ModelAdmin):
	list_display = ('name', 'code', 'display_category_of_aggregation')
	#fields = (('name', 'code'), 'content')
admin.site.register(LevelOfAggregation, LevelOfAggregationAdmin)

class CategoryOfaggregationAdmin(admin.ModelAdmin):
	list_display = ('name', 'code')
	#fields = (('name', 'code'), 'content')
admin.site.register(CategoryOfAggregation, CategoryOfaggregationAdmin)

class FrequencyAdmin(admin.ModelAdmin):
	list_display = ('name', 'code')
	#fields = (('name', 'code'), 'content')
admin.site.register(Frequency, FrequencyAdmin)

class FactorAdmin(admin.ModelAdmin):
	list_display = ('f', 'value')
	#fields = (('name', 'code'), 'content')
admin.site.register(Factor, FactorAdmin)

class PeriodAdmin(admin.ModelAdmin):
	list_display = ('name', '__str__', 'factor')
	#fields = (('name', 'code'), 'content')
admin.site.register(Period, PeriodAdmin)

class VariableAdmin(admin.ModelAdmin):
	list_display = ('name', 'code', 'price')
admin.site.register(Variable, VariableAdmin)

class ConcatTableAdmin(admin.ModelAdmin):
	list_display = ('name', 'code', 'concat_price', 'display_variables', 'display_available_years' )
admin.site.register(ConcatTable, ConcatTableAdmin)

class UserRequestAdmin(admin.ModelAdmin):
	list_display = ('user', 'request_time','display_database','code', 'concat_price', 'display_years', 'display_variables', 'display_categories_of_aggregation', 'purchased','period_sum_factor', 'data_price')
admin.site.register(UserRequest, UserRequestAdmin)

class YearsAdmin(admin.ModelAdmin):
	pass
admin.site.register(Years, YearsAdmin)
