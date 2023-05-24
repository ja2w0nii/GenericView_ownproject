from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from users.models import User


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label="이메일")
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password_check = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password_check = self.cleaned_data.get("password_check")
        if password and password_check and password != password_check:
            raise ValidationError("Passwords don't match")
        return password_check

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("id", "email", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password", "profile_img", "username")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    search_fields = (
        "email",
        "username",
    )
    ordering = ("id",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
