from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.conf import settings
from django.http import HttpResponse,Http404,JsonResponse,HttpResponseRedirect
from .models import Tweet
from .forms import TweetForm
from rest_framework.response import Response
from .serializers import ( TweetSerializer,TweetActionSerializer,
TweetCreateSerializer)
import random
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated]) #REST APIS
def tweet_create_view(request,*args,**kwargs):  
    serializer = TweetCreateSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data,status=200)
    return Response({},status=400)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return HttpResponse(serializer.data, status=200)


@api_view(['GET'])
def tweet_list_view(request,*args,**kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')# ?username = e-wave
    if username != None:
        qs =qs.filter(user__username__iexact=username)
    serializer = TweetSerializer(qs,many=True)
    
    return Response(serializer.data)


@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request,tweet_id,*args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"you do not have permission to delete this tweet"},status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message":"successfully deleted"},status=200)

    
    # return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args,**kwargs):
    #this function performs the action of like,unlike and retweet
    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({},status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)
        elif action == "retweet":
            #todo
            parent_obj = obj
            new_tweet  = Tweet.objects.create(user=request.user,
            parent=parent_obj,content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data,status=201)

        if request.user in obj.likes.all():
            obj.likes.remove(request.user)
        else:
            obj.likes.add(request.user)
    
    return Response({"message":"successfully deleted"},status=200)



def home_view(request,*args,**kwargs):
    return render(request,'pages/home.html',context = {})
def tweet_list_view_pure_django(request,*args,**kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser":False,
        'response':tweets_list
    }
    return JsonResponse(data)


def tweet_create_view_pure_django(request,*args,**kwargs):
    '''
    REST API  Create VIEW WITH DRF
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({},status = 401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid() and is_safe_url(next_url,ALLOWED_HOSTS):
        obj = form.save(commit=False)
        ##other logics
        obj.user =  user#ananymous users get weeded out
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201)##added content to a page
        if next_url != None:
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors,status=400)
    return render(request,'components/form.html', context={"form":form})


def tweet_detail_view(request,tweet_id,*args,**kwargs):
    '''
    REST API VIEW
    Consume by Javascript or swift or java or IOS/ANDROID
    return json data
    '''
    data_dict = {
        'id':tweet_id
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data_dict['content'] = obj.content
        return f'<h1>Hello {tweet_id}</h1>'
    except:
        data_dict['message'] = 'Not Found'
        status = 404
    return  JsonResponse(data_dict,status=status)

