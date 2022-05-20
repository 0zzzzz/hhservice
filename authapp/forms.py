from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import HhUser, HhUserProfile, Skills


class HhUserLoginForm(AuthenticationForm):
    class Meta:
        model = HhUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(HhUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class HhUserRegisterForm(UserCreationForm):
    class Meta:
        model = HhUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = True
        user.save()
        return user


class HhUserEditForm(UserChangeForm):
    class Meta:
        model = HhUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'skills')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class HhUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = HhUserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserSkillsForm(forms.ModelForm):
    class Meta:
        model = HhUser
        fields = ['skills']

    skills = forms.ModelMultipleChoiceField(
        queryset=Skills.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label='Скиллы',
        required=False,
    )
    skills.widget.attrs.update({'class': 'skills_class'})


class SkillCreateForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class SkillEditForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
