from django import forms
from .models import Post, Images

class PostCreationForm(forms.ModelForm):
    title = forms.CharField(label='Post title', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'})
                                )

    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'class': 'form-control mt-2', 'rows':'5'})
                            )

    book_author = forms.CharField(label='Book author', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    phone_contact = forms.CharField(label='Phone number (not required)', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    price = forms.DecimalField(label='Price', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2','placeholder':'Example: 100.00'}
    ))

    postal_code = forms.CharField(label='Postal code or the name of the place you wish to make the exchange. It can be at your school.', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    isbn = forms.DecimalField(label='ISBN', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2'}
    ))

    main_img = forms.ImageField(label='Top image', widget=forms.FileInput(
        attrs={'class':'form-control mt-2', 'type':'file'}
    ))

    class Meta:
        model = Post
        fields = ['title', 'description', 'book_author', 'phone_contact', 'price', 'postal_code', 'isbn', 'main_img']

class WantPostCreationForm(forms.ModelForm):
    title = forms.CharField(label='Post title', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'})
                                )

    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'class': 'form-control mt-2', 'rows':'5'})
                            )

    book_author = forms.CharField(label='Book author', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    phone_contact = forms.CharField(label='Phone number (not required)', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    price = forms.DecimalField(label='Price', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2','placeholder':'Example: 100.00'}
    ))

    postal_code = forms.CharField(label='Postal code or the name of the place you wish to make the exchange. It can be at your school.', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    isbn = forms.DecimalField(label='ISBN', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2'}
    ))

    main_img = forms.ImageField(label='Top image', widget=forms.FileInput(
        attrs={'class':'form-control mt-2', 'type':'file'}
    ))

    class Meta:
        model = Post
        fields = ['title', 'description', 'book_author', 'phone_contact', 'price', 'postal_code', 'isbn', 'main_img']

#Enables adding multiple images
class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Additional image (not required)', widget=forms.FileInput(
        attrs={'class':'form-control mb-3 mt-2', 'type':'file'}
    ))

    class Meta:
        model = Images
        fields = ['image']