from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from datetime import date

BANGLADESH_DISTRICTS = [
    ('Bagerhat', 'Bagerhat'),
    ('Bandarban', 'Bandarban'),
    ('Barguna', 'Barguna'),
    ('Barisal', 'Barisal'),
    ('Bhola', 'Bhola'),
    ('Bogra', 'Bogra'),
    ('Brahmanbaria', 'Brahmanbaria'),
    ('Chandpur', 'Chandpur'),
    ('Chittagong', 'Chittagong'),
    ('Chuadanga', 'Chuadanga'),
    ('Comilla', 'Comilla'),
    ('Cox\'s Bazar', 'Cox\'s Bazar'),
    ('Dhaka', 'Dhaka'),
    ('Dinajpur', 'Dinajpur'),
    ('Faridpur', 'Faridpur'),
    ('Feni', 'Feni'),
    ('Gaibandha', 'Gaibandha'),
    ('Gazipur', 'Gazipur'),
    ('Gopalganj', 'Gopalganj'),
    ('Habiganj', 'Habiganj'),
    ('Jamalpur', 'Jamalpur'),
    ('Jessore', 'Jessore'),
    ('Jhalokathi', 'Jhalokathi'),
    ('Jhenaidah', 'Jhenaidah'),
    ('Joypurhat', 'Joypurhat'),
    ('Khagrachhari', 'Khagrachhari'),
    ('Khulna', 'Khulna'),
    ('Kishoreganj', 'Kishoreganj'),
    ('Kurigram', 'Kurigram'),
    ('Kushtia', 'Kushtia'),
    ('Lakshmipur', 'Lakshmipur'),
    ('Lalmonirhat', 'Lalmonirhat'),
    ('Madaripur', 'Madaripur'),
    ('Magura', 'Magura'),
    ('Manikganj', 'Manikganj'),
    ('Meherpur', 'Meherpur'),
    ('Moulvibazar', 'Moulvibazar'),
    ('Munshiganj', 'Munshiganj'),
    ('Mymensingh', 'Mymensingh'),
    ('Naogaon', 'Naogaon'),
    ('Narail', 'Narail'),
    ('Narayanganj', 'Narayanganj'),
    ('Narsingdi', 'Narsingdi'),
    ('Natore', 'Natore'),
    ('Netrokona', 'Netrokona'),
    ('Nilphamari', 'Nilphamari'),
    ('Noakhali', 'Noakhali'),
    ('Pabna', 'Pabna'),
    ('Panchagarh', 'Panchagarh'),
    ('Patuakhali', 'Patuakhali'),
    ('Pirojpur', 'Pirojpur'),
    ('Rajbari', 'Rajbari'),
    ('Rajshahi', 'Rajshahi'),
    ('Rangamati', 'Rangamati'),
    ('Rangpur', 'Rangpur'),
    ('Satkhira', 'Satkhira'),
    ('Shariatpur', 'Shariatpur'),
    ('Sherpur', 'Sherpur'),
    ('Sirajganj', 'Sirajganj'),
    ('Sunamganj', 'Sunamganj'),
    ('Sylhet', 'Sylhet'),
    ('Tangail', 'Tangail'),
    ('Thakurgaon', 'Thakurgaon')
]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    
    day = forms.ChoiceField(choices=[(i, i) for i in range(1, 32)], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    month = forms.ChoiceField(choices=[(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=[(i, i) for i in range(1900, date.today().year + 1)], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    country = forms.ChoiceField(choices=[('Bangladesh', 'Bangladesh')], required=True, help_text="Select your country.")
    district = forms.ChoiceField(choices=BANGLADESH_DISTRICTS, required=True, help_text="Select your district.")
    #phone_number = forms.CharField(required=True, help_text="Enter your phone number without country code", widget=forms.TextInput(attrs={'placeholder': '2036281978'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "day", "month", "year", "country", "district")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            #'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        day = int(cleaned_data.get('day'))
        month = int(cleaned_data.get('month'))
        year = int(cleaned_data.get('year'))

        dob = date(year, month, day)
        if dob > date.today():
            self.add_error('year', "Date of Birth cannot be in the future.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.profile.date_of_birth = date(
                int(self.cleaned_data['year']),
                int(self.cleaned_data['month']),
                int(self.cleaned_data['day'])
            )
            user.profile.country = self.cleaned_data['country']
            user.profile.district = self.cleaned_data['district']
            #user.profile.phone_number = self.cleaned_data['phone_number']
            user.profile.save()
        return user


# Add this below the CustomUserCreationForm class
class CustomAuthenticationForm(AuthenticationForm):
    #email =  forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))