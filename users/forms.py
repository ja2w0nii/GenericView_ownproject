from django import forms
from users.models import User


# 로그인
class SigninForm(forms.Form):
    email = forms.EmailField(label="이메일 주소", max_length=255)
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password wrong"))
        except User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User not exist"))


# 프로필 수정
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "profile_img"]
