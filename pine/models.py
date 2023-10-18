from django.db import models
from django.contrib.auth.models import User, Group

class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True, unique=True)
	def __str__(self):
		return self.name
     
class PinePrice(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
     name = models.CharField(max_length=200, null=True)
     price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

     def __str__(self):
          return self.name
     
class PineValue(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
     value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
     date = models.DateField(auto_now_add=False, null=True)

class BadValuePine(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
     value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
     date = models.DateField(auto_now_add=False, null=True)
     
class Crop(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
     number_planted = models.PositiveIntegerField(null=True)
     plant_date = models.DateField(auto_now_add=False, null=True)
     price = models.ForeignKey(PinePrice, on_delete=models.SET_NULL, null=True)

     
class Yield(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
     number_yield = models.PositiveIntegerField(null=True)
     harvest_date = models.DateField(auto_now_add=False, null=True)
     value = models.ForeignKey(PineValue, on_delete=models.SET_NULL, null=True)
     calculated_value = models.FloatField(null=True)

class BadPine(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
     number_yield = models.PositiveIntegerField(null=True)
     harvest_date = models.DateField(auto_now_add=False, null=True)
     value = models.ForeignKey(BadValuePine, on_delete=models.SET_NULL, null=True)
     calculated_value = models.FloatField(null=True)

class WorkerPays(models.Model):
      name = name = models.CharField(max_length=200, null=True)
      price_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
      workers = models.DecimalField(max_digits=10, decimal_places=2, null=True)
      date = models.DateField(auto_now_add=False, null=True)

      def __str__(self):
            return self.name
      
class PestOnFarm(models.Model):
      category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
      types_of_pest = models.CharField(max_length=200, null=True)

class BiddingProcess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_buy_pine = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateField(auto_now_add=True, null=True)

    def calculate_total(self):
        if self.bid_price is not None and self.total_buy_pine is not None:
            return self.bid_price * self.total_buy_pine
        else:
            return None

    @classmethod
    def assign_user_from_group(cls, buyer):
        try:
            group = Group.objects.get(name=buyer)  # Replace 'group_name' with the name of your group
            user_to_assign = group.user_set.first()  # Assign the first user in the group
            bidding_process = cls(user=user_to_assign)
            bidding_process.save()
            return bidding_process
        except Group.DoesNotExist:
            return None  # Handle the case where the group doesn't exist

    def __str__(self):
        return str(self.user)
      