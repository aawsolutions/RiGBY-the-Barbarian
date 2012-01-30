from django.db import models
from django.core.urlresolvers import reverse



class Soundtrack(models.Model):
    title = models.CharField(max_length=100)
    composer = models.ForeignKey('Person', related_name='composer')
    mp3 = models.FileField(upload_to='soundtracks/')
    description = models.TextField(blank=True)
    added = models.DateField(auto_now_add=True)

    pages = models.ManyToManyField('Page', blank=True)

    def __unicode__(self):
        return '%s - by %s' % (self.title, self.composer)

class PersonManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)    

class Person(models.Model):
    """Person model."""

    objects = PersonManager()

    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    first_name = models.CharField(blank=True, max_length=100)
    middle_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    slug = models.SlugField(unique=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    class Meta:
        verbose_name_plural = 'People'
        unique_together = (('first_name','last_name'),)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def natural_key(self):
        return (self.first_name, self.last_name)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    published = models.DateTimeField()

    cover = models.ImageField(upload_to='books/cover_art/', blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return('read_book', (), {
            'book_slug': self.chapter.book.slug,
        })


class Chapter(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    published = models.DateTimeField()

    cover = models.ImageField(upload_to='books/cover_art/', blank=True)
    background = models.ImageField(upload_to='books/backgrounds', blank=True)
    
    book = models.ForeignKey('Book')

    def __unicode__(self):
        return self.title

    class META:
        unique_together = (('book', 'chapter'),)

    @models.permalink
    def get_absolute_url(self):
        return('read_chapter', (), {
            'book_slug': self.book.slug,
            'chapter_slug': self.slug,
        })


class Page(models.Model):
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    legacy_slug = models.SlugField(unique=True, blank=True)
    author = models.ManyToManyField('Person', related_name='author')
    artist = models.ManyToManyField('Person', related_name='artist')
    colorist = models.ManyToManyField('Person', related_name='colorist')
    pnumber = models.IntegerField()

    published = models.DateTimeField()
    chapter = models.ForeignKey('Chapter')

    art = models.ImageField(upload_to='books/art/')
    text = models.TextField(blank=True)

    class META:
        unique_together = (('chapter', 'pnumber'),)

    def __unicode__(self):
        return '%s - %s' % (self.chapter, self.pnumber)

    @models.permalink
    def get_absolute_url(self):
        return('read_page', (), {
            'book_slug': self.chapter.book.slug,
            'chapter_slug': self.chapter.slug,
            'page_number': self.pnumber
        })

    def formatted_published(self):
        return self.published.strftime('%a, %d %b %Y %H:%M:%S GMT')


class BTS(models.Model):
    '''Behind-the-scenes content for pages'''
    title = models.CharField(max_length=255)
    art = models.ImageField(upload_to='books/art/bts/')
    text = models.TextField(blank=True) 
    page = models.ForeignKey('Page')
        

    class Meta:
        verbose_name_plural = 'BTS\'s'

    def __unicode__(self):
        return '%s' % self.page


    
