from django import forms
from selling.models import Post, Images

class PostCreationForm(forms.ModelForm):
    title = forms.CharField(label='Titre de la publication', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'})
                                )

    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'class': 'form-control mt-2', 'rows':'5'})
                            )

    book_author = forms.CharField(label='Auteur du livre', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    phone_contact = forms.CharField(label='Numéro de téléphone (non requis)', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    price = forms.DecimalField(label='Prix', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2','placeholder':'Example: 100.00'}
    ))

    postal_code = forms.CharField(label="Code postal ou le nom de l'endroit où vous voulez faire l'échange. Ça peut être à ton école", widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    isbn = forms.DecimalField(label='ISBN', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2'}
    ))

    main_img = forms.ImageField(label='Image du haut', widget=forms.FileInput(
        attrs={'class':'form-control mt-2', 'type':'file'}
    ))

    class Meta:
        model = Post
        fields = ['title', 'description', 'book_author', 'phone_contact', 'price', 'postal_code', 'isbn', 'main_img']

class WantPostCreationForm(forms.ModelForm):
    title = forms.CharField(label='Titre de la publication', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'})
                            )

    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'class': 'form-control mt-2', 'rows': '5'})
                                  )

    book_author = forms.CharField(label='Auteur du livre', widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    phone_contact = forms.CharField(label='Numéro de téléphone (non requis)', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}
    ))

    price = forms.DecimalField(label='Prix', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2', 'placeholder': 'Example: 100.00'}
    ))

    postal_code = forms.CharField(
        label="Code postal ou le nom de l'endroit où vous voulez faire l'échange. Ça peut être à ton école",
        widget=forms.TextInput(
            attrs={'class': 'form-control mt-2'}
        ))

    isbn = forms.DecimalField(label='ISBN', widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2'}
    ))

    main_img = forms.ImageField(label='Image du haut', widget=forms.FileInput(
        attrs={'class': 'form-control mt-2', 'type': 'file'}
    ))

    class Meta:
        model = Post
        fields = ['title', 'description', 'book_author', 'phone_contact', 'price', 'postal_code', 'isbn', 'main_img']

#Enables adding multiple images
class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Images supplémentaires (non requis)', widget=forms.FileInput(
        attrs={'class':'form-control mb-3 mt-2', 'type':'file'}
    ))

    class Meta:
        model = Images
        fields = ['image']