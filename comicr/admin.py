from django.contrib import admin
from comicr.models import *

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('author', 'artist', 'colorist',) 

class SoundtrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'composer', 'mp3',)
    filter_horizontal = ('pages',)

#class BTSAdmin(admin.ModelAdmin):
#class PersonAdmin(admin.ModelAdmin):

admin.site.register(Person)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(BTS)
admin.site.register(Soundtrack, SoundtrackAdmin)
