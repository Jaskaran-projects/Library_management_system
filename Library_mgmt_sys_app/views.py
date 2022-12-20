from Library_mgmt_sys_app.constants import *
from Library_mgmt_sys_app.responses import *
from Library_mgmt_sys_app.exceptions import *
from Library_mgmt_sys_app.utils import *
from Library_mgmt_sys_app.models import *
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Q

class SearchView(View):
    def __init__(self):
        self.response = init_response()
        
    def get(self , request , *args , **kwargs):
        params = request.GET.dict()
        try:
            author_name = params.get('author_name')
            publisher_name = params.get('publisher_name')
            book_id = params.get('book_id')
            books = Books.objects.exclude(status == 'd').filter(Q(authors_name = author_name) | Q(publishers_name = publisher_name) | Q(books_name = book_name)).distinct()
            book_list = [book.as_dict() for book in books]
            self.response['res_data'] = book_list
            self.response['res_str'] = SEARCHED_BOOKS
            return send_200(self.response)
        except ObjectNotFound as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            return send_400(self.response)

class AuthorsView(View):
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['name'])
            author_id = params.get('author_id')
            if author_id:
                author_obj = Authors.objects.get(pk=author_id)
                self.response['res_data'] = author_obj.as_dict()
                self.response['res_str'] = GOT_AUTHOR_NAME
                return send_200(self.response)
            else:
                authors = Authors.objects.all()
                authors_list=[author.as_dict() for author in authors]
            self.response['res_data'] = authors_list
            self.response['res_str'] = GOT_AUTHOR_NAMES
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            validate_schema(params,['author_name'])
            validateJSON(meta_data)
            author_name = params.get('author_name')
            description = params.get('description')
            meta_data = params.get('meta_data')
            author_obj = Authors.objects.create(author_name = author_name , meta_data = meta_data , description = description)
            self.response['res_data'] = author_obj.as_dict()
            self.response['res_str'] = AUTHOR_NAME_CREATED
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def put(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:      
            author_id = params['author_id']
            author_name = params['author_name']
            author_obj = Authors.objects.get(pk=author_id)
            author_obj.author_name = author_name
            author_obj.save(update_fields=['author_name'])
            self.response['res_str'] = AUTHOR_NAME_UPDATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def delete(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            author_id = params['author_id']
            author_obj = Authors.objects.get(pk = author_id)
            if author_obj.status == 'd':
                self.response['res_str'] = AUTHOR_STATUS_INACTIVE
                return send_200(self.response)
            author_obj.status = 'd'
            author_obj.save(update_fields = ['status'])
            self.response['res_str'] = AUTHOR_STATUS_INACTIVATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

class LanguagesView(View):
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['language_name'])
            language_id = params.get('language_id')
            if language_id:
                language_obj = Languages.objects.get(pk = language_id)
                self.response['res_data'] = language_obj.as_dict()
                self.response['res_str'] = GOT_LANGUAGE_NAME
                return send_200(self.response)
            else:
                language_obj = Language.objects.all()
                data = [language.as_dict() for language in language_obj]
            self.response['res_data'] = data
            self.response['res_str'] = GOT_LANGUAGE_NAMES
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            validate_schema(params,['lanugage_name'])
            language_name = params.get('language_name')
            script = params.get('script')
            about = params.get('about')
            language_obj = Languages.objects.create(language_name = language_name , script = script , about = about)
            self.response['res_data'] = language_obj.as_dict()
            self.response['res_str'] =LANGUAGE_NAME_CREATED
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def put(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            language_id = params['language_id']
            language_name = params['language_name']
            language_obj = Languages.objects.get(pk = language_id)
            language_obj.language_name = language_name
            language_obj.save(update_fields=['language_name'])
            self.response['res_str'] = LANGUAGE_NAME_UPDATED
            return send_200(self.response)
        except ObjectNotFound as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def delete(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            language_id = params['language_id']
            language_obj = Languages.objects.get(pk = language_id)
            if language_obj.status == 'd':
                self.response['res_str'] = LANGUAGE_STATUS_INACTIVE
                return send_400(self.response)
            language_obj.status = 'd'
            language_obj.save(update_fields = ['status'])
            self.response['res_str'] = LANGUAGE_STATUS_INACTIVATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

class PublishersView(View):
    def __init__(self):
        self.response = init_response()    

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['publisher_name'])
            publisher_id = params.get('publisher_id')
            if publisher_id:
                publisher_obj = Publishers.objects.get(pk = publisher_id)
                self.response['res_data'] = publisher_obj.as_dict()
                self.response['res_str'] = GOT_PUBLISHER_NAME
                return send_200(self.response)
            else:
                publisher_obj = Publishers.objects.all()
                data = [publisher.as_dict() for publisher in publisher_obj]
            self.response['res_data'] = data
            self.response['res_str'] = GOT_PUBLISHER_NAMES
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            validate_schema(params,['publisher_name'])
            ValidateJSON(meta_data)
            publisher_name = params.get('publisher_name')
            meta_data = params.get('meta_data')
            publisher_obj = Publishers.objects.create(publisher_name = publisher_name , meta_data = meta_data)
            self.response['res_data'] = publisher_obj.as_dict()
            self.response['res_str'] = PUBLISHER_NAME_CREATED
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def put(self, request, *args, **kwargs):
        try:
            params = json.loads(request.body)
            publisher_id = params['publisher_id']
            publisher_name = params['publisher_name']
            publisher_obj = Publishers.objects.get(pk=pub_id)
            publisher_obj.publisher_name = publisher_name
            publisher_obj.save(update_fields = ['publisher_name'])
            self.response['res_str'] = PUBLISHER_NAME_UPDATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def delete(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            publisher_id = params['publisher_id']
            publisher_obj = Publishers.objects.get(pk = publisher_id)
            if publisher_obj.status == 'd':
                self.response['res_str'] = PUBLISHER_STATUS_INACTIVE
                return send_400(self.response)
            publisher_obj.status = 'd'
            publisher_obj.save(update_fields = ['status'])
            self.response['res_str'] = PUBLISHER_STATUS_INACTIVATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

class BooksView(View):
    def __init__(self):
        self.response = init_response()
        
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['publisher_name','book_type'])
            book_id = params.get('book_id')
            if book_id:
                book_obj = Books.objects.get(pk = book_id)
                self.response['res_data'] = book_obj.as_dict()
                self.response['res_str'] = GOT_BOOK_NAME
                return send_200(self.response)
            else:
                books = Books.objects.all()
                data = [book.as_dict() for book in books]
            self.response['res_data'] = data
            self.response['res_str'] = GOT_BOOK_NAMES
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            validate_schema(params,['book_name','publisher','book_type'])
            book_name = params.get('book_name')
            book_type = params.get('book_type')
            extra_details = params.get('extra_details')
            language_id = params.get('language_id')
            author_id = params.get('author_id')
            publisher_id = params.get('publisher_id')
            language_obj = Languages.objects.filter(pk = language_id)
            publisher_obj = Publishers.objects.filter(pk = publisher_id)
            author_obj = Authors.objects.filter(pk = author_id)
            book_obj = Books.objects.create(book_name = book_name , language_name = language_obj.language_name , author_name = author_obj.author_name , publisher_name = publisher_obj.publisher_name , extra_details = extra_details , book_type = book_type)
            self.response['res_data'] = book_obj.as_dict()
            self.response['res_str'] = BOOK_NAME_CREATED
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def put(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            book_id = params['book_id']
            book_name = params['book_name']
            book_obj = Books.objects.get(pk = book_id)
            book_obj.book_name = book_name
            book_obj.save(update_fields=['book_name'])
            self.response['res_str'] =BOOK_NAME_UPDATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def delete(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            book_id = params['book_id']
            book_obj = Books.objects.get(pk = book_id)
            if book_obj.status == 'd':
                self.response['res_str'] =BOOK_STATUS_INACTIVE
                return send_400(self.response)
            book_obj.status = 'd'
            book_obj.save()
            self.response['res_str'] = BOOK_STATUS_INACTIVATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

class UsersView(View):
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['first_name','mobile','email_id'])
            user_id = params.get('user_id')
            if user_id:
                user_obj = Users.objects.get(pk = user_id)
                self.response['res_data'] = user_obj.as_dict()
                self.response['res_str'] = GOT_USER_NAME
                return send_200(self.response)
            else:
                data = [user.as_dict() for user in Users.objects.all()]
                self.response['res_data'] = data
                self.response['res_str'] = GOT_USER_NAMES
                return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            validate_schema(params,['first_name','mobile','email_id'])
            ValidateJSON(meta_data)
            first_name = params.get('first_name')
            last_name = params.get('last_name')
            mobile = params.get('mobile')
            email_id = params.get('email_id')
            meta_data = params.get('meta_data')
            subscription = params.get('subscription')
            favorites = params.get('favorites')
            user_obj = Users.objects.create(first_name = first_name , mobile = mobile , email_id = email_id , meta_data = meta_data , subscription = subscription , favorites = favorites)
            self.response['res_data'] = user_obj.as_dict()
            self.response['res_str'] = USER_NAME_CREATED
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def put(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['user_id','first_name'])
            user_id = params['user_id']
            first_name = params['first_name']
            user_obj = Users.objects.get(pk = user_id)
            user_obj.first_name = first_name
            user_obj.save(update_fields=['first_name'])
            self.response['res_str'] = USER_NAME_UPDATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def delete(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['user_id'])
            user_id = params['user_id']
            user_obj = Users.objects.get(pk = user_id)
            if user_obj.status == 'd':
                self.response['res_str'] =USER_STATUS_INACTIVE
                return send_400(self.response)
            user_obj.status = 'd'
            user_obj.save(update_fields = ['status'])
            self.response['res_str'] = USER_STATUS_INACTIVATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

class EbooksView(View):
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['book','book_location'])
            ebook_id = params.get('ebook_id')
            if ebook_id:
                ebook_obj = Ebooks.objects.get(pk = ebook_id)
                self.response['res_data'] = ebook_obj.as_dict()
                self.response['res_str'] = GOT_EBOOK_NAME
                return send_200(self.response)
            else:
                ebook_obj = Ebooks.objects.all()
                data = [ebook.as_dict() for ebook in ebook_obj]
            self.response['res_data'] = data
            self.response['res_str'] = GOT_EBOOK_NAMES
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            validate_schema(params,['book','book_location'])
            book_name = params.get('book_name')
            ebook_obj = Ebooks.objects.create(book_name = book_name)
            self.response['res_data'] = ebook_obj.as_dict()
            self.response['res_str'] = EBOOK_NAME_CREATED
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def put(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['ebook_id','book_location'])
            ebook_id = params['ebook_id']
            book_location = params['book_location']
            book_obj = Ebooks.objects.get(pk = ebook_id)
            book_obj.book_location = book_location
            book_obj.save(update_fields=['book_location'])
            self.response['res_str'] = EBOOK_LOCATION_UPDATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def delete(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['user_id'])
            ebook_id = params['ebook_id']
            ebook_obj = Users.objects.get(pk = ebook_id)
            if ebook_id.status == 'd':
                self.response['res_str'] = EBOOK_STATUS_INACTIVE
                return send_200(self.response)
            ebook_id.status = 'd'
            ebook_id.save(update_fields = ['status'])
            self.response['res_str'] = EBOOK_STATUS_INACTIVATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

class HardCopysView(View):
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['hard_copy_id'])
            hard_copy_id = params.get('hard_copy_id')
            if hard_copy_id:
                hard_copy_obj = HardCopys.objects.get(pk = hard_copy_id)
                self.response['res_data'] = hard_copy_obj.as_dict()
                self.response['res_str'] = GOT_HARDCOPY_NAME
                return send_200(self.response)
            else:
                hard_copy_obj = HardCopys.objects.all()
                data=[hard_copy.as_dict() for hard_copy in hard_copy_obj]
            self.response['res_data'] = data
            self.response['res_str'] = GOT_HARDCOPY_NAMES
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            validate_schema(params,['book_id','lentTo'])
            book_id = params.get('book_id')
            is_lent = params.get('is_lent')
            lent_to = params.get('lent_to')
            hard_copy_obj = HardCopys.objects.create(book_id = book_id , is_lent = is_lent , lent_to = lent_to)
            self.response['res_data'] = hard_copy_obj.as_dict()
            self.response['res_str'] = HARDCOPY_NAME_CREATED
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def put(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['hard_copy_id','book_id'])
            hard_copy_id = params['hard_copy_id']
            book_id = params['book_id']
            hard_copy_obj = HardCopys.objects.get(pk = hard_copy_id)
            hard_copy_obj.book_id = book_id
            hard_copy_obj.save(update_fields=['book_id'])
            self.response['res_str'] = HARDCOPY_NAME_UPDATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)

    def delete(self, request, *args, **kwargs):
        params = request.GET.dict()
        try:
            validate_schema(params,['user_id'])
            hard_copy_id = params['hard_copy_id']
            hard_copy_obj = HardCopys.objects.get(pk = hard_copy_id)
            if hard_copy_obj.status == 'd':
                self.response['res_str'] =HARDCOPY_STATUS_INACTIVE
                return send_400(self.response)
            hard_copy_obj.status = 'd'
            hard_copy_obj.save(update_fields = ['status'])
            self.response['res_str'] = HARDCOPY_STATUS_INACTIVATED
            return send_200(self.response)
        except ObjectDoesNotExist as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)