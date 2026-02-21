from django.urls import path
from minamo import views
app_name = 'minamo'
urlpatterns = [
    path('', views.BookListView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('new/', views.new_book, name='new_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('book/<int:book_id>/rename/', views.rename_book, name='rename_book'),
    path('book/<int:book_id>/export/', views.export_book, name='export_book'),
    path('book/<int:book_id>/cross_search/', views.cross_search, name='cross_search'),
    path('book/<int:book_id>/chapters/new/', views.new_chapter, name='new_chapter'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/delete/', views.delete_chapter, name='delete_chapter'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/rename/', views.rename_chapter, name='rename_chapter'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/swap/<int:direction>/', views.swap_chapter, name='swap_chapter'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/sections/new/', views.new_section, name='new_section'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/sections/<int:section_id>/', views.section_detail, name='section_detail'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/sections/<int:section_id>/edit/', views.edit_section, name='edit_section'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/sections/<int:section_id>/edit/<str:return_url>/', views.edit_section, name='edit_section_return'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/sections/<int:section_id>/delete/', views.delete_section, name='delete_section'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/sections/<int:section_id>/rename/', views.rename_section, name='rename_section'),
    path('book/<int:book_id>/chapters/<int:chapter_id>/sections/<int:section_id>/swap/<int:direction>/', views.swap_section, name='swap_section'),
    path('settings/', views.settings, name='settings'),
]