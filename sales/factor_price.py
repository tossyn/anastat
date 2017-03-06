sum_factor = 0
for period in Period.objects.all():
	yrs = list(range(period.period_from, period.period_to))
	for year in years:
		if year in yrs:
			sum_factor += period.factor.value

OR

def cal_sum_factor(self):
    	sum_factor = 0
    	periods = Period.objects.all()
    	for period in periods:
    		yrs = list(range(period.period_from, period.period_to))
    		for year in self.years:
    			if year in yrs:
    				sum_factor += period.factor.value
    	return sum_factor
	period_sum_factor = models.PositiveSmallIntegerField(default= self.cal_sum_factor)

r = ConcatTable.objects.get(code=code):
price = r.price