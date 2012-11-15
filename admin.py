from django.contrib import admin


from common.admin import CommonPostAdmin, CommonCategoryAdmin
from . models import GuidebookCategory, GuidebookPost

class GuidebookCategoryAdmin( CommonCategoryAdmin ):
    pass

class GuidebookPostAdmin( CommonPostAdmin ):
    list_display = ( 'title', 'author', 'date_edit', 'date_add', 'status', 'country', 'city', )

admin.site.register( GuidebookCategory, GuidebookCategoryAdmin )
admin.site.register( GuidebookPost, GuidebookPostAdmin )
