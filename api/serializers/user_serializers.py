from rest_framework import serializers
from users.models import    CustomUser, UserProfile

class MinimalUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    
    def get_full_name(self, user):
        return f"{user.first_name} {user.last_name}"
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'user_type', 'user_type_display', 'subscription_status']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'specialization', 'profile_picture', 'topics']

class FullUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'user_type', 
            'user_type_display', 'phone', 'is_verified', 'subscription_status',
            'date_joined', 'last_login', 'profile'
        ]
        
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile fields
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        
        return instance

class CounselorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    specialization = serializers.CharField(source='profile.specialization')
    
    def get_full_name(self, counselor):
        return f"{counselor.first_name} {counselor.last_name}"
    
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'specialization']