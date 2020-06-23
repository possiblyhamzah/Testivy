from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from random import random
from .models import Test, Chapter
import json
from django.http import JsonResponse
# Create your views here.
context = {
    "tests":Test.objects.all(),
    "chapters":Chapter.objects.all(),
    #"user" : "gus"
}

def index(request):
    if request.method == "POST":
        firstname="firstname" #request.POST.get("firstname")
        lastname="lastname" #request.POST.get("lastname")
        username=request.POST.get("username")
        email= "firstname@lastname.com" #request.POST.get("email")
        password=request.POST.get("password")
        user = User.objects.create_user(username,email,password)
        user.first_name=firstname
        user.last_name=lastname
        user.save()
        return render(request, "testapp/login.html")
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("tests"))    
    return render(request, "testapp/register.html")
    

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #context["user"]=username
            return HttpResponseRedirect(reverse("tests"))
        else:
            return render(request, "testapp/login.html", {"message": "Invalid credentials."})
    request.session["login"]=True
    return render(request, "testapp/login.html")

def tests(request):
    if request.method == "POST":
        name=request.POST.get("name")
        chapter=request.POST.get("chapter")
        number=int(request.POST.get("number"))
        #return JsonResponse({"name":name, "id":chapter})
        questions = json.loads(Chapter.objects.filter(user=request.user.username, name=chapter)[0].questions)
        choices = json.loads(Chapter.objects.filter(user=request.user.username, name=chapter)[0].choices)
        answers = json.loads(Chapter.objects.filter(user=request.user.username, name=chapter)[0].answers)
        scores = json.loads(Chapter.objects.filter(user=request.user.username, name=chapter)[0].questionScores)
        testQuestions=[]
        testChoices=[]
        testAnswers=[]
        testScores=[]
        used = []
        i = 0
        while i<number: #allow use to choose number of questions
            randomNumber = int((random()*10))%len(questions)
            if randomNumber not in used:
                testQuestions.append(questions[randomNumber])
                testChoices.append(choices[randomNumber])
                testAnswers.append(answers[randomNumber])
                testScores.append(scores[randomNumber])
                used.append(randomNumber)
                i = i+1
                userScore = ["0"]*number
        test = Test(user=request.user.username, name=name, chapter=chapter, questions=json.dumps(testQuestions), answers=json.dumps(testAnswers), choices=json.dumps(testChoices), questionScores=json.dumps(testScores), userScores=json.dumps(userScore))
        test.save()
        #context["tests"]=Test.objects.all()
        return JsonResponse({"name":name, "id":test.id})
        #test_id = Test.objects.last().id
    data={
        "tests":Test.objects.filter(user=request.user.username,isCompleted=False), 
        "chapters":Chapter.objects.filter(user=request.user.username)
    }
    
    return render(request, "testapp/tests.html", data)

def test(request, test_id):
    
    if request.method == "POST":
        #test.isCompleted = True
        Test.objects.filter(pk=test_id).update(isCompleted=True)
    test = Test.objects.filter(pk=test_id)[0]
    questions = json.loads(test.questions)
    userScores = json.loads(test.userScores)
    questionScores = json.loads(test.questionScores)
    percentage = 0
    userScore = 0
    questionScore=0
    if test.isCompleted:
        for i in range(len(userScores)):
            userScore = userScore + int(userScores[i])
            questionScore = questionScore + int(questionScores[i])
        percentage = round(userScore*100/questionScore,2)
    Test.objects.filter(pk=test_id).update(userPercentage=percentage)
    data={
        "questions":questions,
        "test_id":test_id,
        "score":userScore,
        "total":questionScore,
        "percentage":percentage,
        "isCompleted":test.isCompleted
    }
    
    return render(request, "testapp/test.html", data)

def question(request, test_id, question_id):
    tests = Test.objects.filter(pk=test_id)[0]
    if request.method == "POST":
        answer = request.POST.get("answer")
        
        userScores=json.loads(tests.userScores)
        questionScores=json.loads(tests.questionScores)
        if answer == json.loads(tests.answers)[question_id]:
            userScores[question_id]=questionScores[question_id]
            #Test.objects.filter(pk=test_id).update(userScores=json.dumps(userScores))
        Test.objects.filter(pk=test_id).update(userScores=json.dumps(userScores))
        return JsonResponse({})

    questions = json.loads(tests.questions)
    choices = json.loads(tests.choices)
    data={
        "question":questions[question_id],
        "choices":choices[question_id],
        "test_id":test_id,
        "question_id":question_id
    }
    #if request.method == "POST":
        
    return render(request, "testapp/question.html", data)

def chapters(request):
    if request.method == "POST":
        name = request.POST.get("name")
        chapter = Chapter(user = request.user.username, name = name, questions = '[]', answers = '[]', choices = '[]', questionScores = '[]')
        chapter.save()
        #context["chapters"] = Chapter.objects.all()
        return JsonResponse({"name": name, "id":Chapter.objects.last().id})
    data={
        "tests":Test.objects.filter(user=request.user.username,isCompleted=False), 
        "chapters":Chapter.objects.filter(user=request.user.username)
    }
    return render(request, "testapp/chapters.html", data)

def chapter(request, chapter_id):
    chapters = Chapter.objects.filter(pk=chapter_id)[0]  
    questions = json.loads(chapters.questions)
    if request.method == "POST":
        answers = json.loads(chapters.answers)
        choices = json.loads(chapters.choices)
        questionScores = json.loads(chapters.questionScores)
        name=request.POST.get("name")
        answer = request.POST.get("answer")
        questionChoices=[]
        for i in range(4):
            choice = request.POST.get("choice"+str(i+1))
            questionChoices.append(choice)
        
        questionScore = request.POST.get("score")

        questions.append(name)
        answers.append(answer)
        choices.append(questionChoices)
        questionScores.append(questionScore)
        #jsonquestion=json.dumps(questions)
        Chapter.objects.filter(pk=chapter_id).update(questions=json.dumps(questions), answers=json.dumps(answers), choices=json.dumps(choices), questionScores=json.dumps(questionScores))
        chapters=Chapter.objects.filter(pk=chapter_id)[0]
        return JsonResponse({"question":name})

    data={
        "questions":questions, 
        "chapters":chapters
    }
    
    return render(request, "testapp/chapter.html", data)

def records(request):
    tests = Test.objects.filter(user=request.user.username,isCompleted=True)
    data={
        "tests":tests
    }
    return render(request, "testapp/records.html", data)

def form(request,k):
    return render(request, "testapp/form.html")

def check(request):
    if request.method == "POST":
        return JsonResponse({})    
