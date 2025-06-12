from rest_framework import serializers
from .models import Collection, Product, Review, Cart, CartItem, Customer

# pylint: disable=no-member

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
        
    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description',  'unit_price','collection','inventory']
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name','description', ]
        
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price' ]
        
    id = serializers.IntegerField(read_only=True )
    product = CartProductSerializer()
    
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_total_price(self, cartItem:CartItem):
        return cartItem.product.unit_price * cartItem.quantity

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
    
    items = CartItemSerializer(many=True, read_only=True)
        

        
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_total_price(self, cart:Cart):
        total = 0
        
        for item in cart.items.all():
            total += item.quantity * item.product.unit_price
        return total
    

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity'] 
        
        try:
            cart_item = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id','quantity']
        
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']  

