from django.db import models

class Product(models.Model):
    code = models.CharField(max_length = 32, verbose_name="상품코드")
    name = models.CharField(max_length = 32, verbose_name="상품명")
    description = models.TextField(verbose_name="상품설명")
    price = models.IntegerField(verbose_name="상품가격")
    stock = models.IntegerField(verbose_name="재고", default=0)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X-Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=2, verbose_name="사이즈")


    def __str__(self):
        return self.code

    class Meta:
        db_table = "falseshinsa_product"
        verbose_name = "상품"
        verbose_name_plural = "상품"


class Inbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    inbound_date = models.DateField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.code} ({self.inbound_date})'
    
    class Meta:
        db_table = "falseshinsa_inbound"
        verbose_name = "입고"
        verbose_name_plural = "입고"

class Outbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    outbound_date = models.DateField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.code} ({self.outbound_date})'
    
    class Meta:
        db_table = "falseshinsa_outbound"
        verbose_name = "출고"
        verbose_name_plural = "출고"