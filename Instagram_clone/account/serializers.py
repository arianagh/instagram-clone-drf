from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from account.models import Profile, FollowerUser, FollowerTable


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['age', 'image', 'bio', 'user']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:

            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class FollowerListSerializer(serializers.ModelSerializer):
    """
    serializer to get follower list
    """
    user = serializers.CharField(read_only=True, source="following.user.username")
    follower = serializers.CharField(read_only=True, source='follower.username')

    class Meta:
        model = FollowerUser
        fields = ['id', 'user', 'follower']


class FollowerRequestSerializer(serializers.ModelSerializer):
    """
    serializer for requesting to follow
    """
    class Meta:
        model = FollowerUser
        exclude = ["following"]
        extra_kwargs = {
            "status": {
                "read_only": True
            }
        }

    def create(self, validated_data):
        # kesi ke mikhad follow kne
        darkhast_dahande = self.context["follower_request"]
        # mikhad follower e felan user beshe
        darkhast_shavande = validated_data["follower"].followers_table
        return FollowerUser.objects.create(follower=darkhast_dahande, following=darkhast_shavande, status="p")


class FollowingListSerializer(serializers.ModelSerializer):
    """
    serializer to get following list
    """
    user = serializers.CharField(source='follower.username')
    following = serializers.CharField(source='following.user.username')

    class Meta:
        model = FollowerUser
        fields = ["id", "user", "following"]


class FollowerListNestedSerializer(serializers.ModelSerializer):
    """
    serializer to get follower list from FollowerTable with nested serializer
    """
    username = serializers.CharField(source='user.username')
    followers = FollowerListSerializer(many=True)

    class Meta:
        model = FollowerTable
        fields = ["username", "followers", 'follower_count']


class FollowingListNestedSerializer(serializers.ModelSerializer):
    """
    serializer to get following list from User with nested serializer
    """
    followings = FollowerListSerializer(many=True)
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'followings', 'following_count']

    def get_following_count(self, obj):
        return obj.followings.count()
