from rest_framework import serializers
from .models import Client, Product
from django.contrib.auth import get_user_model
User = get_user_model()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id",
                  'name',
                  'email')
        extra_kwargs = {'email': {'required': True}}


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id_product",
                  'id_client')


class FavoriteViewSerializer(serializers.Serializer):
    id_product = serializers.UUIDField()
    title = serializers.CharField()
    image = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    review_score = serializers.DecimalField(max_digits=10, decimal_places=7, required=False)
    create_at = serializers.DateTimeField(required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
