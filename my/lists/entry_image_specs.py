# Based on ImageKit docs at http://bitbucket.org/jdriscoll/django-imagekit/wiki/Home

from imagekit.specs import ImageSpec
from imagekit import processors

# first we define our thumbnail resize processor
class ResizeSidebarThumb(processors.Resize):
    width = 150
    height = 150
    crop = True
    upscale = True

class ResizeMainThumb(processors.Resize):
    width = 510
    height = 190
    crop = True
    upscale = True

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
    width = 510
    height = 765
    upscale = False

# now lets create an adjustment processor to enhance the image at small sizes
class EnhanceSidebarThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

class BlurMainThumb(processors.Adjustment):
    brightness = 1.2 # 4.0
    color = 1.5 # 4.0
    contrast = 1.0 # 0.5
    sharpness = 0.5 # 0.5

# now we can define our thumbnail spec
class SidebarThumbnail(ImageSpec):
    pre_cache = True
    processors = [ResizeSidebarThumb, EnhanceSidebarThumb]

class MainThumbnail(ImageSpec):
    pre_cache = True
    processors = [ResizeMainThumb, BlurMainThumb]

# and our display spec
class Display(ImageSpec):
    increment_count = True
    processors = [ResizeDisplay]
