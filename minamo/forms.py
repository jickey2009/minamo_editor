from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book, Chapter, Section, Configuration, CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email','first_name','last_name','password1','password2')

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username','password')

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title','description')

class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ('title',)

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ('title','content')

class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration
        fields = ('dark_mode','UD_Digi','text_size','textarea_height','textarea_width','text_vertical_align')
        labels = {
            'dark_mode': 'ダークモード',
            'UD_Digi': 'UD書体を使用する(Windowsのみ)',
            'text_size': '文字サイズ',
            'textarea_height': 'テキストエリアの高さ（文字数）',
            'textarea_width': 'テキストエリアの幅（文字数）',
            'text_vertical_align': '縦書き',
        }