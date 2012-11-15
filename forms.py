from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
#from django.forms.models import inlineformset_factory

from common.forms import CommonPostEditForm
from . models import GuidebookPost, GuidebookCategory, GuidebookPostImages

class GuidebookEditForm( CommonPostEditForm ):
    category = forms.ModelMultipleChoiceField( 
        queryset = GuidebookCategory.objects.all(),
        required = False,
        widget = FilteredSelectMultiple( 
            'categories',
            False,
        )
    )

    class Meta( CommonPostEditForm.Meta ):
        fields = ( 
            'title',
            'content',
            'category',
            'country',
            'city',
            'source',
            'tags',
        )
        model = GuidebookPost


class ImageUploadForm( forms.ModelForm ):
    post = forms.ModelChoiceField( 
        queryset = GuidebookPost.objects.all(),
        widget = forms.HiddenInput()
    )

    class Meta:
        model = GuidebookPostImages
