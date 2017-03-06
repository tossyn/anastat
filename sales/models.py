from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
#from multiselectfield import MultiSelectField


class Component(models.Model):    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5, null=True)
    description = models.TextField(default='Database category description goes here')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Components'


class Database(models.Model):    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3, null=True) 
    description = models.TextField(default='description goes here')
    component = models.ForeignKey(Component)

    def __str__(self):
        return self.name

class CategoryOfAggregation(models.Model):  
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5, null=True) 
    description = models.TextField(default='description goes here')
    #level = models.ForeignKey(LevelOfAggregation)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories of Aggregation'

class LevelOfAggregation(models.Model):     
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5, null=True) 
    description = models.TextField(default='description goes here')
    category_of_aggregation = models.ManyToManyField(CategoryOfAggregation)

    def __str__(self):
        return self.name

    def display_category_of_aggregation(self):        
        return ', '.join([ coa.code for coa in self.category_of_aggregation.all()])
    display_category_of_aggregation.short_description = 'Category(ies) of Aggregation'


    class Meta:
        verbose_name_plural = 'Levels of Aggregation'


class Frequency(models.Model):    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5, null=True) 
    description = models.TextField(default='description goes here')
    #price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Frequencies'

class Years(models.Model):    
    yr = models.PositiveSmallIntegerField(default=1960, blank=True, null=True)

    def __str__(self):
        return str(self.yr)

    class Meta:
        verbose_name_plural = 'Years'

class Factor(models.Model):
    f = models.CharField(max_length=15)
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.value)

class Period(models.Model):
    name =  models.CharField(max_length=200, default='1960s', null=True, blank=True)      
    period_from = models.PositiveSmallIntegerField()
    period_to =   models.PositiveSmallIntegerField()         
    description = models.TextField(default='description goes here')
    #factor = models.OneToOneField(Factor)
    factor =   models.PositiveSmallIntegerField(default=1)
   
    def __str__(self):
         return '%s - %s' % (self.period_from,self.period_to)

    # def display_period_span(self):
    # 	return __str__()
    # display_period_span.short_description = 'Period Span'

class Table(models.Model):    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3) 
    description = models.TextField(default='description goes here')
    database = models.ForeignKey(Database)
    level_of_aggregation = models.ManyToManyField(LevelOfAggregation)
    frequency = models.ManyToManyField(Frequency)


    def __str__(self):
        return '%s - %s' % (self.name,self.code)

    def display_level_of_aggregation(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ level.code for level in self.level_of_aggregation.all()])
    display_level_of_aggregation.short_description = 'Level(s) of Aggregation'

    def display_frequency(self):        
        return ', '.join([ frequency.code for frequency in self.frequency.all()])
    display_frequency.short_description = 'Frequency(ies)'

    class Meta:
        verbose_name_plural = 'Tables'

class Variable(models.Model):    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5)
    price = models.IntegerField(default = 0) 
    description = models.TextField(default='description goes here')
   
    def __str__(self):
        return self.name


class ConcatTable(models.Model):
	name =  models.CharField(max_length=200, default='ConcatTable Name')
	table = models.ForeignKey(Table)
	level_of_aggregation= models.ForeignKey(LevelOfAggregation)
	frequency = models.ForeignKey(Frequency)
	# Default value for code through a callable
	
	code = models.CharField(max_length=7, blank =True)
	concat_price = models.PositiveSmallIntegerField()
	description = models.TextField(default='description goes here')
	# avail_from = models.PositiveSmallIntegerField(default = 1990)
	# avail_to = models.PositiveSmallIntegerField(default = 2016)
	avail_yrs = models.ManyToManyField(Years)
	variable = models.ManyToManyField(Variable)
	def __str__(self):
	    return self.code

	def concat_code(self):
		# if table != None and level_of_aggregation != None and frequency != None:
		code = self.table.code + self.level_of_aggregation.code + self.frequency.code
		return code

	def save(self, *args, **kwargs):
		self.code = self.concat_code()
		super(ConcatTable, self).save(*args, **kwargs) # Call the "real" save() method.


	def display_available_years(self):
		yrs = [year.yr for year in self.avail_yrs.all()]
		return '%d - %d' % (min(yrs), max(yrs))
	display_available_years.short_description = 'Available Year(s)'

	# def available_years(self):
	# 	yrs = list(range(self.avail_from, self.avail_to+1))

	def display_variables(self):
		return ', '.join([ variable.code for variable in self.variable.all()])
	display_variables.short_description = 'Variable(s)'

	class Meta:
	    verbose_name_plural = 'Concatenated Table'


class UserRequest(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	table = models.ForeignKey(Table)
	level_of_aggregation = models.ForeignKey(LevelOfAggregation)
	frequency = models.ForeignKey(Frequency)
	code = models.CharField(max_length=7)	
	concat_price = models.PositiveSmallIntegerField()
	years = models.ManyToManyField(Years, help_text="To select multiple hold down ctrl botton on the keyboard or ctrl A to select all")
	variables = models.ManyToManyField(Variable, help_text="To select multiple hold down ctrl botton on the keyboard or ctrl A to select all")
	categories_of_aggregation = models.ManyToManyField(CategoryOfAggregation, help_text="To select multiple hold down ctrl botton on the keyboard or ctrl A to select all")
	period_sum_factor = models.PositiveSmallIntegerField(default=0)	
	comment = models.TextField(default='Write your comments are. Thank you!')
	request_time = models.DateTimeField(default=timezone.now)
	data_price = models.IntegerField(default=0)
	purchased = models.BooleanField(default=False)

	def __str__(self):
	    return self.code

	def __unicode__(self):
	    return self.__str__()

	def display_database(self):
		return self.table.database

	def set_purchased(self):
		self.purchased = True
		return self.purchased


	def display_years(self):
	    """
	    Creates a string for MultipleselectField/ManyToManyField. This is required to display ManyToMany of MultipleselectField in Admin.
	    """
	    return ', '.join([ str(year.yr) for year in self.years.all()])
	display_years.short_description = 'Selected Years'
	# Get a list of the selected years
	def list_years(self):
		list_yrs = [year.yr for year in self.years.all()]
		return list_yrs

	def display_categories_of_aggregation(self):        
	    return ', '.join([ category.code for category in self.categories_of_aggregation.all()])     
	display_categories_of_aggregation.short_description = 'Category(ies) of Aggregation'
	# Get a list of the selected categories
	def list_cat(self):
		list_cats = [ category.code for category in self.categories_of_aggregation.all()]
		return list_cats

	def display_variables(self):        
	    return ', '.join([ variable.code for variable in self.variables.all()])
	display_variables.short_description = 'Variable(s)'
	# Get a list of the selected variables
	def list_var(self):
		list_vars = [ variable.code for variable in self.variables.all()]
		return list_vars
	
	def user_request_code(self):
		# if table != None and level_of_aggregation != None and frequency != None:
		code = self.table.code + self.level_of_aggregation.code + self.frequency.code
		return code
		
	def user_request_concat_price(self):
		# if table != None and level_of_aggregation != None and frequency != None:
		request_code = self.user_request_code()
		data = get_object_or_404(ConcatTable, code=request_code)
		concat_price = data.concat_price
		return concat_price	

	def cal_sum_factor(self):
		sum_factor = 0
		sltd_yrs = self.list_years()
		periods = Period.objects.all()
		for period in periods:
			yrs = list(range(period.period_from, period.period_to))
			for year in sltd_yrs:
				if year in yrs:
					sum_factor += period.factor
		return sum_factor
	
	def select_count(self, multi):
		count = 0
		for item in multi:
			count=count+1
		return count
	
	def cal_data_price(self):
		num_cat = self.select_count(self.list_var())
		num_vars = self.select_count(self.list_cat())
		sum_factor = self.cal_sum_factor()
		concat_price = self.user_request_concat_price()
		data_price = num_cat * num_vars * sum_factor * concat_price
		return data_price

	def save(self, *args, **kwargs):
		self.concat_price = self.user_request_concat_price()
		self.code = self.user_request_code()
		
		super(UserRequest, self).save(*args, **kwargs) # Call the "real" save() method.

	def update_price(self):
		self.period_sum_factor = self.cal_sum_factor()
		self.data_price = self.cal_data_price()





    
















