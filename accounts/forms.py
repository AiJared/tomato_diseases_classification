from django import forms
from accounts.models import User, Profile

class ProfileForm(forms.ModelForm):
    
    full_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    # town = forms.CharField(max_length=50)
    # county = forms.CharField(max_length=50)

    password1 = forms.CharField(
        required=False, label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",required=False,
        widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user:
            # self.fields['phone'].initial = user.phone
            self.fields['full_name'].initial = user.full_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
            # self.fields['town'].initial = user.town
            # self.fields['county'].initial = user.county
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs.update({'class':'form-control'})
            # self.fields[field].widget.attrs.update({'style': 'width: 350px;'})
        # Set email field as read-only
        self.fields['full_name'].widget.attrs.update({'readonly':True})
        self.fields['email'].widget.attrs.update({'readonly':True})
        self.fields['profile_picture'].widget.attrs.update({'class':'account-settings-fileinput'})

    class Meta:
        model = Profile
        fields = ['email','password1','password2','full_name','bio','profile_picture', 'username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        print(f"Hello {password2}")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")

        return password2
# def convert_phone_number(phone_number):
#     parsed_number = phonenumbers.parse(phone_number, "KE")  # Assuming the phone number is from Kenya (change the country code accordingly)
#     formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
#     return formatted_number