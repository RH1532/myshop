from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from products.models import Category, Product, Cart
from .serializers import CategorySerializer, ProductSerializer, CartSerializer
from .permissions import IsOwnerOrReadOnly, IsOwnerOfCart


class CategoryList(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        categories = Category.objects.all()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProductList(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        products = Product.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AddToCart(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfCart]

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCart(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfCart]

    def put(self, request, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id, user=request.user)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfCart]

    def delete(self, request, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id, user=request.user)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartDetails(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfCart]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return Response({'cart_items': serializer.data, 'total_quantity': total_quantity, 'total_price': total_price})


class ClearCart(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfCart]

    def delete(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        cart_items.delete()
        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_204_NO_CONTENT)
