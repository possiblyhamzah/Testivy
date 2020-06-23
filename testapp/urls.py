from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:k>", views.form, name="form"),
    path("check", views.check, name="check"),
    path("login_view", views.login_view, name="login_view"),
    path("tests", views.tests, name="tests"),
    path("records", views.records, name="records"),
    path("test/<int:test_id>/", views.test, name="test"),
    path("chapter/<int:chapter_id>", views.chapter, name="chapter"),
    path("test/<int:test_id>/<int:question_id>/", views.question, name="question"),
    path("chapters", views.chapters, name="chapters")
]
