from django.shortcuts import render, redirect
from app_one.models import User, Item
from django.contrib import messages
import bcrypt


# index method :
def index(request):
    # print("hi")
    return render(request, 'index.html')

# login method:
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.get(username=username)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session["UserId"] = user.id
        return redirect('/dashboard')
    else:
        messages.error(request, "User password do not match") 
        return redirect("/")

# register method:
def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, errorMessage in errors.items():
                messages.error(request, errorMessage)
            return redirect("/")
        else:
            name = request.POST["name"]
            username = request.POST["username"]
            password = request.POST["password"]
            date_hired=request.POST['date_hired']
            passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(name=name, username=username,date_hired=date_hired, password=passwordHash)
            request.session["UserId"] = newUser.id
            messages.success(request, "User has been created")
            return redirect("/dashboard")
# logout method
def logout(request):
    request.session.clear()
    messages.success(request, "You have been logged out!")
    return redirect("/")

# if register or login the user will be see the dashboard
def dashboard(request):
    if not 'UserId' in request.session:
        # print("hi from dashboard")
        return redirect('/')
    user = User.objects.get(id=request.session['UserId'])
    items = Item.objects.filter(id=user.id)
    #all users except the user has this id
    other = Item.objects.all().exclude(users__id=user.id)
    context = {
        "user": user,
        "items": items,
        "other": other
    }
    return render(request, 'dashboard.html', context)

# create a new item into the database
def create_item(request):
 if not 'UserId' in request.session:
     return redirect('/')
 if request.method == "POST":
    errors = Item.objects.add_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/add_item')
    user = User.objects.get(id=request.session['UserId'])
    item = Item.objects.create(
        item=request.POST.get('item'),
        added_by=user
    )
    user.items.add(item)
    user.save()
 return redirect('/dashboard')

# Add other user's wish
def add_wish(request):
    item = Item.objects.get(id=request.POST['item_id'])
    user = User.objects.get(id=request.session['UserId'])
    print(f"hi from add_wish {request.session['UserId']}")
    user.items.add(item)
    user.save()
    return redirect('/dashboard')

# information about the item
def show_item(request, id):
    if not 'UserId' in request.session:
        return redirect('/')
    item = Item.objects.get(id=id)
    print(f"hi from show{request.session['UserId']}")
    context = {
        "item": item,
    }
    return render(request, 'show_item.html', context)

def add_item(request):
    if not 'UserId' in request.session:
        return redirect('/')
    return render(request, 'add_item.html')


# Remove items from a list
def remove_wish(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(id=request.session['UserId'])
    item.users.remove(user)
    return redirect('/dashboard')

# Delete items the user created to a list
def delete_wish(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('/dashboard')