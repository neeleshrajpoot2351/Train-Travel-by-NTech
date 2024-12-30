from django.shortcuts import render,redirect
from .models import User
from .forms import UserRegistrationForm
from django.conf import settings
import requests
from .models import Train, Station
# Create your views here.
def home(request):
    return render(request,'project3/PrecticeWebsiteHome.html')
def about(request):
    return render(request,'project3/PrecticeWebsiteAbout.html')
def PNR(request):
    return render(request,'project3/PrecticeWebsitePNRStatus.html')
def contects(request):
    return render(request,'project3/PrecticeWebsiteContects.html')
def PNR1(request):
    return render(request,'project3/PrecticeWebsitePNRStatus1.html')
def HomeFindTrain(request):
    return render(request,'project3/PrecticeWebsiteHome1.html')

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'project3/Rajester_login.html', {'form': form})

def success(request):
    users = User.objects.all().order_by('-first_name')[:3]
    return render(request, 'project3/Rajester_login_Success.html',{'users':users})

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
                return render(request, "project3/PrecticeWebsitePNRStatus1.html", {"data": api_data["data"]})
            else:
                return render(request, "project3/PrecticeWebsitePNRStatus1.html", {"error": "PNR status not found."})
        else:
            return render(request, "project3/PrecticeWebsitePNRStatus1.html", {"error": "Failed to fetch PNR status. Try again later."})
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
            return render(request, "project3/LiveTrainStatusResult.html", {"data": api_data})
        else:
            return render(request, "project3/LiveTrainStatusResult.html", {"error": "Unable to fetch train status. Please try again later."})

    return render(request, "project3/LiveTrainStatus.html")



def train_details(request):
    train_data = request.session.get('train_data', {})
    return render(request, 'project3/PrecticeWebsiteHome1.html', {'train_data': train_data})

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
            return render(request, 'project3/PrecticeWebsiteHome.html', {
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
        # Check for trains where origin, destination, or passing stations match
        trains = Train.objects.filter(
            origin=from_station,
            destination=to_station
        ) | Train.objects.filter(
            stations=from_station,
            destination=to_station
        )

    context = {
        'from_station': from_station_name,
        'to_station': to_station_name,
        'trains': trains
    }

    return render(request, 'project3/PrecticeWebsiteHome2.html', context)