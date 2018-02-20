from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip, Companion

def index(request):

    return render(request, 'belt_app/index.html')

def register(request):
    userToRegister = User.objects.register(
        name = request.POST['name'],
        username = request.POST['username'],
        password = request.POST['password'],
        confirm_password = request.POST['confirm_password']
    )

    if userToRegister['valid']:
        request.session["user_id"] = userToRegister['user'].id
        return redirect("/travels")
    else: 
        for error in userToRegister['errors']:
            messages.error(request, error)
        return redirect('/')

def login(request):
    response = User.objects.login(
        username = request.POST['username'], 
        password = request.POST['password']
    )

    if response['valid']:
        request.session['user_id'] = response['user'].id
        return redirect('/travels')
    
    if len(response['errors']) > 0:
        for error in response['errors']:
            messages.warning(request, error)
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


def travels(request):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")



# This code loops through all of the trips (alltrips) checking
# the current user's "joinedtrips" to "exclude" those where the 
# user has already joined. The joinedtrips object contains

# all of the trips   
# all of the companion records that the user logged in has already joined.
# loop through the companion.join records and exclude based on trip ID vs all trip ids.
    alltrips = Trip.objects.all()
    joinedtrips = Companion.objects.filter(user_id=request.session["user_id"])
    for join in joinedtrips:
        alltrips = alltrips.exclude(id=join.trip.id)

    data = {
        'user' : User.objects.get(id=request.session["user_id"]),
        'trip' : alltrips,
        'joined': joinedtrips
    }

    return render(request, 'belt_app/travels.html', data)

def travels_add(request):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")
    
    data = {
        'user' : User.objects.get(id=request.session["user_id"]),
        
    }

    return render(request, 'belt_app/add_trip.html', data)

# datetime.strptime(request.POST['date'], '%d-%m-%Y')

def add_trip(request):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")
    print User.objects.get(id=request.session["user_id"])
    
    response = Trip.objects.add_trip(
        request.POST['destination'],
        request.POST['plan'],
        request.POST['start_date'],
        request.POST['end_date'],
        User.objects.get(id=request.session["user_id"])
    )

    if response['valid']:
# This has the user who created the trip join the trip they just created.
        Companion.objects.create(
        user_id = request.session['user_id'],
        trip = response['trip']
        )

        return redirect("/travels")
    else: 
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/travels/add')


def destination(request, id):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")
    # for x in Companion.objects.all():
    #     if str(x.trip.id) == str(id):
    #         print x.trip.planner.name
    
    data = {
        'trip': Trip.objects.get(id=id),
        'comp': Companion.objects.filter(trip_id = id),
    }
    # 
    # myTripComps = Companion.objects.filter(trip_id = id)
    # for comp in myTripComps:
    #     print comp.user.name

    return render(request, 'belt_app/destination.html', data)

def join(request, id):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")

    myTrip = Trip.objects.get(id=id)
    
    print Companion.objects.create(
        user_id = request.session['user_id'],
        trip = myTrip
        )

    print User.objects.get(id=request.session["user_id"])

    return redirect("/travels")


