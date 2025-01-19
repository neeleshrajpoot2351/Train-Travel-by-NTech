from django.shortcuts import render,redirect , HttpResponse , get_object_or_404
from .models import User
from .forms import UserRegistrationForm
from django.conf import settings
import requests
from .models import Train, Station ,TrainStation
from django.urls import reverse
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'Train_Travel_templates/PrecticeWebsiteHome.html')
def about(request):
    return render(request,'Train_Travel_templates/PrecticeWebsiteAbout.html')
def PNR(request):
    return render(request,'Train_Travel_templates/PrecticeWebsitePNRStatus.html')
def contects(request):
    return render(request,'Train_Travel_templates/PrecticeWebsiteContects.html')
def PNR1(request):
    return render(request,'Train_Travel_templates/PrecticeWebsitePNRStatus1.html')
def HomeFindTrain(request):
    return render(request,'Train_Travel_templates/PrecticeWebsiteHome1.html')

from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        email = request.POST.get('email')  # Extract email from form data
        if User.objects.filter(email=email).exists():
            # Show warning message for duplicate email
            messages.warning(request, "You are already registered with this email.")
        elif form.is_valid():
            # Save the new user if form is valid and email is unique
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('success')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'Train_Travel_templates/Rajester_login.html', {'form': form})


def success(request):
    users = User.objects.all().order_by('-first_name')[:3]
    return render(request, 'Train_Travel_templates/Rajester_login_Success.html',{'users':users})

def fetch_pnr_status(request):
    """
    Fetch PNR status and display the result.
    """
    if request.method == "POST":
        pnr_number = request.POST.get("pnr_number")  # Get PNR from form input
        
        url = f"https://irctc-indian-railway-pnr-status.p.rapidapi.com/getPNRStatus/{pnr_number}"

        headers = {
            "x-rapidapi-host": "irctc-indian-railway-pnr-status.p.rapidapi.com",
            "x-rapidapi-key": "7e89795bffmshf7266d1d67468e4p119f0ejsn190094580583",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            api_data = response.json()
            if api_data.get("success"):
                return render(request, "Train_Travel_templates/PrecticeWebsitePNRStatus1.html", {"data": api_data["data"]})
            else:
                return render(request, "Train_Travel_templates/PrecticeWebsitePNRStatus1.html", {"error": "PNR status not found."})
        else:
            return render(request, "Train_Travel_templates/PrecticeWebsitePNRStatus1.html", {"error": "Failed to fetch PNR status. Try again later."})
    else:
        return redirect("PNR") 
    


def live_train_status(request):
    """
    Fetch and display live train status using the RapidAPI service.
    """
    if request.method == "POST":
        train_number = request.POST.get("train_number")
        departure_date = request.POST.get("departure_date")  # Format: YYYYMMDD

        url = f"https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status?departure_date={departure_date}&isH5=true&client=web&train_number={train_number}"

        headers = {
            "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
            "x-rapidapi-key": "7e89795bffmshf7266d1d67468e4p119f0ejsn190094580583",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            api_data = response.json()
            return render(request, "Train_Travel_templates/LiveTrainStatusResult.html", {"data": api_data})
        else:
            return render(request, "Train_Travel_templates/LiveTrainStatusResult.html", {"error": "Unable to fetch train status. Please try again later."})

    return render(request, "Train_Travel_templates/LiveTrainStatus.html")

def train_details(request):
    train_data = request.session.get('train_data', {})
    return render(request, 'Train_Travel_templates/PrecticeWebsiteHome1.html', {'train_data': train_data})

def fetch_train_info(request):
    if request.method == "POST":
        train_number = request.POST.get('train_number')
        url = f"https://indian-railway-irctc.p.rapidapi.com/api/trains-search/v1/train/{train_number}?isH5=true&client=web"
        headers = {
            'x-rapid-api': 'rapid-api-database',
            'x-rapidapi-host': 'indian-railway-irctc.p.rapidapi.com',
            'x-rapidapi-key': settings.RAPIDAPI_KEY,
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            request.session['train_data'] = data  # Store data in session
            return redirect('train_details')
        else:
            return render(request, 'Train_Travel_templates/PrecticeWebsiteHome.html', {
                'error': 'Unable to fetch train data. Please try again later.'
            })
    return redirect('home')



def find_trains(request):
    from_station_name = request.GET.get('from_station', '').strip()
    to_station_name = request.GET.get('to_station', '').strip()

    # Find the stations
    from_station = Station.objects.filter(name__iexact=from_station_name).first()
    to_station = Station.objects.filter(name__iexact=to_station_name).first()

    trains = []
    if from_station and to_station:
        # Fetch the direct trains from the origin to the destination
        direct_trains = Train.objects.filter(
            origin=from_station,
            destination=to_station
        ).distinct()

        # Fetch trains that pass through the origin and destination stations
        via_trains = Train.objects.filter(
            stations=from_station,
        ).filter(stations=to_station).distinct()

        # Combine both direct and via trains
        trains = direct_trains | via_trains

        train_details = []
        for train in trains:
            train_details.append({
                'train': train
            })

        context = {
            'from_station': from_station_name,
            'to_station': to_station_name,
            'train_details': train_details
        }
    else:
        context = {
            'from_station': from_station_name,
            'to_station': to_station_name,
            'train_details': []
        }

    return render(request, 'Train_Travel_templates/PrecticeWebsiteHome2.html', context)


def train_details(request, train_number):
    # Fetch the train based on train_number
    train = Train.objects.filter(train_number=train_number).first()
    if not train:
        return HttpResponse("Train not found.", status=404)

    # Get "from" and "to" stations
    from_station_name = request.GET.get('from_station', '').strip()
    to_station_name = request.GET.get('to_station', '').strip()

    from_station = Station.objects.filter(name__iexact=from_station_name).first()
    to_station = Station.objects.filter(name__iexact=to_station_name).first()

    if not from_station or not to_station:
        return HttpResponse("Invalid stations.", status=404)

    # Get the train's stops and order them by stop_number
    stops = TrainStation.objects.filter(train=train).order_by('stop_number')

    # Filter stops between "from" and "to" stations
    valid_stops = []
    passed_from_station = False
    for stop in stops:
        if stop.station == from_station:
            passed_from_station = True
        if passed_from_station:
            valid_stops.append(stop)
        if stop.station == to_station:
            break

    # Prepare stop details for the template
    stop_details = []
    for stop in valid_stops:
        stop_details.append({
            'station': stop.station.name,
            'stop_number': stop.stop_number,
            'arrival_time': stop.arrival_time or 'Not Available',
            'departure_time': stop.departure_time or 'Not Available',
            'platform': stop.platform_number or 'Not Available'
        })

    context = {
        'train': train,
        'stop_details': stop_details
    }

    return render(request, 'Train_Travel_templates/PrecticeWebsiteHome3.html', context)
