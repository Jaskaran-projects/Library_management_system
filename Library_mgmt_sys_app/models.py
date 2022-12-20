from __future__ import unicode_literals
from django.db import models
from .constants import *
from django.core.exceptions import *
import uuid

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status_choices = (
        ('a','active'),
        ('i','inactive'),
        ('d','deleted')
    )
    status = models.CharField(choices = status_choices , default = 'i' , max_length = 1)
    
    class Meta:
        abstract = True

class Authors(BaseModel):
    author_id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    author_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 70 , null = True , blank = True)
    meta_deta = models.JSONField(default = {} , blank = True)
    
    def __str__(self):
        return self.name
    
    def as_dict(self):
        params = {}
        params['author_id'] = self.author_id
        params['author_name'] = self.author_name
        params['description'] = self.description
        params['meta_data'] = self.meta_data
        return params

class Languages(BaseModel):
    language_id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    language_name = models.CharField(max_length = 50 , unique = True)
    script = models.CharField(max_length = 50 , blank = True)
    about = models.CharField(max_length = 50 , null = True , blank = True)
    
    def __str__(self):
        return self.name
    
    def as_dict(self):
        params = {}
        params['language_id'] = self.language_id
        params['language_name'] = self.language_name
        params['script'] = self.script
        params['about'] = self.about
        return params

class Publishers(BaseModel):
    publisher_id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    publisher_name = models.CharField(max_length = 50)
    meta_data = models.JSONField(default = {} , blank = True)
    
    def __str__(self):
        return self.name
    
    def as_dict(self):
        params = {}
        params['publisher_id'] = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
        params['publisher_name'] = self.publisher_name
        params['meta_data'] = self.meta_data
        return params

class Books(BaseModel):
    book_choices = (
        ('eb','Ebook'),
        ('ne','Nebook')
    )
    book_id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    book_name = models.CharField(max_length = 50)
    language = models.ManyToManyField(Languages)
    authors = models.ManyToManyField(Authors)
    publishers = models.ForeignKey(Publishers , on_delete = models.CASCADE)
    extra_details = models.JSONField(default = {} , blank = True)
    book_type = models.CharField(max_length = 2 , choices = book_choices)
    
    def __str__(self):
        return self.name
    
    def as_dict(self):
        params = {}
        params['book_id'] = self.book_id
        params['book_name'] = self.book_name
        params['language'] = [language.as_dict() for language in self.languages.all()]
        params['authors'] = [author.as_dict() for author in self.authors.all()]
        params['publisher'] = self.publisher.as_dict()
        params['extra_details'] = self.extra_details
        params['book_type'] = self.book_type
        return params
    
class Users(BaseModel):
    user_roles = (
        ('s','superadmin'),
        ('l', 'librarian'),
        ('u','user')
    )
    role = models.CharField(max_length = 1 , choices = user_roles , default = 'u')
    user_id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    first_name = models.CharField(max_length = 50)
    middle_name = models.CharField(max_length = 50 , null = True , blank = True) 
    last_name = models.CharField(max_length = 50, null = True , blank = True)
    mobile = models.CharField(max_length = 50)
    email_id = models.EmailField(max_length = 50 , unique=True)
    meta_data = models.JSONField(default = {} , blank = True)
    subscription = models.BooleanField(default = False)
    favorites = models.ManyToManyField(Books , related_name = 'favorites')

    def __str__(self):
        return self.first_name
    
    def as_dict(self):
        params = {}
        params['role'] = self.role
        params['usr_id'] = self.usr_id
        params['first_name'] = self.first_name
        params['last_name'] = self.last_name
        params['mobile'] = self.mobile
        params['email_id'] = self.email_id
        params['meta_data'] = self.meta_data
        params['subscription'] = self.subscription
        params['favorites'] = [book.as_dict() for book in self.favorites.all()]
        return params

class Ebooks(models.Model):
    book_name = models.ForeignKey(Books , on_delete = models.CASCADE, related_name = "ebook")
    ebook_id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    book_location = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.ebook_id)

    def as_dict(self):
        params = {}
        params['book'] = self.book.as_dict()
        params['ebook_id'] = self.ebook_id
        params['book_location'] = self.book_location
        return params
    
class HardCopys(models.Model):
    book_id = models.ForeignKey(Books , on_delete = models.CASCADE)
    hard_copy_id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    is_lent = models.BooleanField(default = False)
    lent_to = models.ForeignKey(Users , on_delete = models.CASCADE)

    def __str__(self):
        return str(self.hard_copy_id)

    def as_dict(self):
        params = {}
        params['book_id'] = self.book_id.as_dict()
        params['hard_copy_id'] = self.hard_copy_id
        params['is_lent'] = self.is_lent
        params['lent_to'] = self.lent_to.as_dict()
        return params