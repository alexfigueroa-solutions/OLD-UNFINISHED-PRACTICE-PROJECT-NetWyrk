from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from feed.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Profile, FriendRequest
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import random
from .models import Project
import feed

User = get_user_model()



#creates recommended users list.
@login_required
def users_list(request):
    #excludes selected user from the list and stores all users in there
    users = Profile.objects.exclude(user = request.user)
    #stores friend requests sent by self user in an object
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    
    #creates empty for users that were already sent friend requests
    sent_to = []
    #creates empty array for users that are already my friend
    friends = []

    #if youre already friends with someone
    for user in users:
        #gets all friends of selected user
        friend = user.friends.all()
        #for every friend of selected user:
        for f in friend:
            #if f is already your friend
            if f in friends:
                #exclude 
                friend = friend.exclude(user=f.user)
        #add already friends,to the friends array
        friends += friend 
    #my friends
    my_friends = request.user.profile.friends.all()
    #iterates through all my friends
    for i in my_friends:
        #if their friends are already my friends,
        #then remove them from the list
        if i in friends:
            friends.remove(i)
    #if selected user is in list, remove them 
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    
    #creates random list of users
    random_list = random.sample(list(users), min(len(list(users)),10))
    #iterates thru random list
    for r in random_list:
        #if were already friends, remove them
        if r in friends:
            random_list.remove(r)
    friends+=random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    #iterates through sent friend requests
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context={
        'users': friends,
        'sent':sent_to
    }
    return render(request, "users/users_list.html", context)












#displays all friends of requested user
def friend_list(request):
    #requested profile
    p = request.user.profile
    #gets all friends from user
    friends=p.friends.all()
    #sets context for friends
    context={
        'friends':friends
    }
    #renders html friend_list
    return render(request, "users/friend_list.html", context)




#sends friend request by requesting user id
@login_required
def send_friend_request(request, id):
    #gets user or returns 404
    user = get_object_or_404(User, id=id)
    #creates friend request object between me and selected user
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    #redirects you to users page
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))
    



#cancels friend request
@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user = request.user,
        to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))
    


#accept friend requests
@login_required
def accept_friend_request(request, id):
    #stores the sending user in an object 
    from_user = get_object_or_404(User, id=id)
    #stores friend request in object
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    #person receiving request
    user1 = frequest.to_user
    #person who sent the request
    user2 = from_user
    #add each other as friends
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    #delete all other requess between the two
    if(FriendRequest.objects.filter(from_user=request.user, to_user=request.user)).first():
        #stores reverse request
        request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user)
        #delete reverse friend request
        request_rev.delete()
    #deletes friend request after is been accepted
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))




#deletes friend request
@login_required
def delete_friend_request(request, id):
    #stores sender
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user = from_user, to_user = request.user).first()
    #deletes friend request
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


@login_required
#deletes friend
def delete_friend(request, id):
    #gets users profile
    user_profile = request.user.profile
    #gets friends profile
    friend_profile = get_object_or_404(Profile, id=id)
    #remove both profiles as friends
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    #redirects back o friends page
    return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))


#creates a view for a profile
@login_required
def profile_view(request, slug):
    #gets the profile with the requested slug
    user_profile = Profile.objects.filter(slug=slug).first()
    #gets the user that the profile is associated with
    associated_user = user_profile.user
    #gets friend requests sent from user
    sent_friend_requests = FriendRequest.objects.filter(from_user = associated_user)
    #gets list of received friend requests
    rec_friend_requests = FriendRequest.objects.filter(to_user = associated_user)
    #gets list of users posts
    user_posts = Post.objects.filter(user_name = associated_user)
    friends = user_profile.friends.all()
    projects = Project.objects.filter(by_user = associated_user)


    #checks if associated user is our friend 
    #sets button status to none beforehand
    button_status = 'none'
    #if associated user profile is not in my list of friends
    if user_profile not in request.user.profile.friends.all(): 
        #set button status to not friend
        button_status = 'not_friend'

        #if associated user is not our friend, but we sent him a friend request
        if len(FriendRequest.objects.filter(from_user = request.user).filter(to_user = associated_user)) == 1:
            button_status = 'friend_request_sent'
    
    #sets context for django
    context ={
        'associated_user':associated_user,
        'button_status':button_status,
        'sent_friend_requests':sent_friend_requests,
        'rec_friend_requests':rec_friend_requests,
        'post_count':user_posts.count,
        'friend_count':friends.count,
        'projects_count':projects.count,
    }
    #renders profile html
    return render(request, "users/profile.html", context)

#registers user if they try to post
def register(request):
    #if user tries to post
    if request.method == 'POST':
        #create user register form on request to post
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #sends account creation success message
            messages.success(request, f'You have successfully created your account. Have fun expanding your horizons.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request , 'users/register.html',{'form':form})


#allows users to edit their profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated successfully.')
            return redirect('my_profile')
        #reload old forms
    else:
        user_form = UserUpdateForm(instance = request.user )
        profile_form = ProfileUpdateForm(instance = request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form}
    return render(request, 'users/edit_profile.html', context)

#views own profile
@login_required
def my_profile(request):
    my_profile = request.user.profile
    my_user = my_profile.user
    #gets sent friend requests
    sent_friend_requests = FriendRequest.objects.filter(from_user = my_user)
    #gets received friend reqs
    rec_friend_requests = FriendRequest.objects.filter(to_user = my_user)
    #gets my posts
    my_posts = Post.objects.filter(user_name = my_user)
    #gets my friends
    my_friends = my_profile.friends.all()
    
    button_status = 'this_is_me'

    #creates context for Django to relate objects
    context = {
        'my_user':my_user,
        'my_profile':my_profile,
        'friends_list':my_friends,
        'sent_friend_requests':sent_friend_requests,
        'rec_friend_requests':rec_friend_requests,
        'post_count':my_posts.count,
        'friends_count':my_friends.count

    }
    #renders profile html
    return render(request, "users/profile.html", context)

 
#searches for users
@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains = query)
    context = {
        'users':object_list
    }
    return render(request, "users/search_users.html",context)
