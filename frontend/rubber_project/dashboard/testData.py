from dashboard.models import Order

o1 = Order(
product_brand='Butterfly',
rubber_name='Tenergy-05',
overall_score=4.2,
comment='good control',
unit_price=80
)
o1.save()
