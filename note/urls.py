from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/(?P<folder_id>\d+)/$', views.upload, name='upload'),
    url(r'^book/(?P<book_id>\d+)/$', views.get_question_page, name='question_page'),
    url(r'^get_questions/(?P<book_id>\d+)/$', views.get_question, name='get_question'),
    url(r'^post_answer/$', views.post_answer_sheet, name='post_answer'),
    url(r'^operate/(?P<book_id>\d+)/$', views.operate, name='op'),
    url(r'^view_sheet/(?P<sheet_id>\d+)/$', views.view_sheet, name='sheet'),
    url(r'^sort_out/(?P<sheet_id>\d+)/$', views.sort_out, name='sort_out'),
    url(r'^edit_desc/(?P<book_id>\d+)/$', views.edit_desc, name='edit_desc'),
    url(r'^refactor/$', views.refactor, name='refactor'),
    url(r'^change_public_status/(?P<book_id>\d+)/$', views.change_public_status, name='change')
]
