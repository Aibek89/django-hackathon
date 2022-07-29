from rest_framework import serializers

from cart.models import Order


class OderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        quantity_order = validated_data['quantity']
        product = validated_data['product']
        product_quantity = product.amount

        if quantity_order > product_quantity:
            raise serializers.ValidationError(f'превышенно количество продукта. Доступное кол.{product_quantity}')
        product.amount -= quantity_order
        product.save()
        return super().create(validated_data)