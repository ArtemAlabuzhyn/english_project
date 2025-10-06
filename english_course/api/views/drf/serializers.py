from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.templatetags.rest_framework import items

from english_course.api.views.drf.utils import validate_tranlsation
from english_course.models import User, UserWord, Word


class UserProfileSerializer(serializers.ModelSerializer):
    words = serializers.SerializerMethodField()
    total_words = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'email', 'words', 'total_words']

    def get_words(self, obj):
        last_words = UserWord.objects.filter(user=obj).order_by('-id')[:10]

        return [
            {
                'word': uw.word.word,
                'translation': uw.translation
            }

            for uw in last_words
        ]

    def get_total_words(self, obj):
        return UserWord.objects.filter(user=obj).count()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if user is None:
            raise serializers.ValidationError('Invalid username or password')

        data['user'] = user
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match')
        return data

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def create(self, validated_data):

        request = self.context.get('request')
        creator = request.user

        if creator.role == 'teacher' and validated_data.get('role') != 'student':
            raise serializers.ValidationError('Teachers can only create students')

        teacher = None
        if creator.role == 'teacher':
            teacher = request.user

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            teacher=teacher

        )
        return user


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'email']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class WordSerializer(serializers.ModelSerializer):

    word = serializers.CharField(source='word.word')
    class Meta:
        model = UserWord
        fields = ['id', 'word', 'translation']

    def validate(self, data):
        data['word'] = data['word'].strip().capitalize()
        data['translation'] = validate_tranlsation(data['translation'])
        return data


class EditWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWord
        fields = ['translation']

        def validate_translation(self, value):
            return validate_tranlsation(value)


class CreateWordSerializer(serializers.ModelSerializer):
    word_text = serializers.CharField(write_only=True, allow_blank=False)
    translation = serializers.CharField(allow_blank=False)

    class Meta:
        model = UserWord
        fields = ['word_text', 'translation']

    def create(self, validated_data):
        user = self.context['request'].user
        word_text = validated_data['word_text']
        translation = validated_data['translation']

        word_obj, _ = Word.objects.get_or_create(word=word_text)
        user_word_qs = UserWord.objects.filter(user=user, word=word_obj)

        if user_word_qs.exists():
            user_word = user_word_qs.first()

            existing = set(user_word.translation.split('; '))
            new = set(translation.split('; '))
            combined = sorted(existing.union(new))
            user_word.translation = '; '.join(combined)
            user_word.save()
            return user_word
        return UserWord.objects.create(user=user, word=word_obj, translation=translation)

    def validate_word_text(self, data):
        return data.strip().capitalize()

    def validate_translation(self, value):
        return validate_tranlsation(value)

    def validate(self, data):
        user = self.context['request'].user
        word_text = data['word_text']
        translation = data['translation']

        try:
            word = Word.objects.get(word=word_text)
            user_word = UserWord.objects.filter(user=user, word=word).first()

            if user_word:
                existing_translation = set(user_word.translation.split('; '))
                incoming_translation = set(translation.split('; '))

                if incoming_translation.issubset(existing_translation):
                    raise serializers.ValidationError('Word with translation already exists')
        except Word.DoesNotExist:
            pass

        return data
