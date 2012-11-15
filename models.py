from django.db import models
from django.conf import settings

import uuid

from smart_selects.db_fields import ChainedForeignKey

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust, SmartResize, ResizeToFit

from common.models import CommonCategory, CommonPost, CommonPostImage
from location.models import Country, City

# Create your models here.

def image_upload_to( instance, filename ):
    ext = filename.split( '.' )[-1]
    filename = "%s.%s" % ( uuid.uuid4(), ext.lower() )
    id = str( instance.post.id )
    return 'guidebook/%s/%s/%s' % ( id[:1], id, filename )

class GuidebookCategory( CommonCategory ):
    pass

class GuidebookPost( CommonPost ):
    category = models.ManyToManyField( GuidebookCategory )
    country = models.ForeignKey( Country, null = True, )
    city = ChainedForeignKey( 
        City,
        chained_field = "country",
        chained_model_field = "country",
        blank = True,
        null = True,
        show_all = False,
        auto_choose = False
    )
    source = models.URLField( 
        blank = True,
        verbose_name = u'Source URL',
        help_text = u'source web site full URL',
    )
    is_featured = models.BooleanField( default = 0 )
    featured_untill = models.DateTimeField( blank = True )

class GuidebookPostImages( CommonPostImage ):
    post = models.ForeignKey( GuidebookPost, default = '', blank = True, null = True, )
    image = models.ImageField( upload_to = image_upload_to )
