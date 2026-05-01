from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, Passenger, Booking, Airport

def index(request):
    flights = Flight.objects.select_related("origin", "destination").all()
    airports = Airport.objects.all().order_by("city")
    show_promo_banner = request.session.pop("show_promo_banner", False)
    promo_code = request.session.get("promo_code")
    return render(request, "flights/index.html", {
        "flights": flights,
        "airports": airports,
        "show_promo_banner": show_promo_banner,
        "promo_code": promo_code,
    })

def flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    booked_passengers = flight.bookings.count()
    seats_left = flight.capacity - booked_passengers
    can_view_passengers = request.user.is_authenticated and request.user.is_staff
    return render(request, "flights/flight.html", {
        "flight": flight,
        "seats_left": seats_left,
        "booked_passengers": booked_passengers,
        "can_view_passengers": can_view_passengers,
    })

def airport(request, airport_id):
    airport = get_object_or_404(Airport, pk=airport_id)
    return render(request, "flights/airport.html", {
        "airport": airport,
    })

@login_required
def book_flight(request, id):
    flight = Flight.objects.get(id=id)

    seats_left = flight.capacity - flight.bookings.count()

    if seats_left <= 0:
        return render(request, "full.html")

    if request.method == "POST":
        name = request.user.get_full_name() or request.user.username
        email = request.user.email or f"{request.user.username}@example.com"

        passenger, created = Passenger.objects.get_or_create(
            email=email,
            defaults={"name": name}
        )
        if not created and passenger.name != name:
            passenger.name = name
            passenger.save(update_fields=["name"])
        Booking.objects.create(
            passenger=passenger,
            user=request.user,
            flight=flight
        )

        return redirect("flight", flight_id=id)

    return render(request, "flights/book_flight.html", {
        "flight": flight,
        "seats_left": seats_left
    })

def bookings(request):
    if not request.user.is_authenticated:
        return redirect("login")

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related("flight", "flight__origin", "flight__destination")

    return render(request, "flights/bookings.html", {
        "bookings": bookings,
        "email": request.user.email
    })

def check_booking(request):

    if request.method == "POST":
        code = request.POST.get("code")

        try:
            booking = Booking.objects.select_related(
                "flight",
                "flight__origin",
                "flight__destination",
                "passenger"
            ).get(booking_code=code)

            return render(request, "flights/booking_result.html", {
                "booking": booking
            })

        except Booking.DoesNotExist:
            return render(request, "flights/booking_not_found.html")

    return redirect("index")


def api_flights(request):
    flights = Flight.objects.select_related("origin", "destination").all()
    data = [
        {
            "id": flight.id,
            "origin": flight.origin.code,
            "destination": flight.destination.code,
            "duration": flight.duration,
            "capacity": flight.capacity,
        }
        for flight in flights
    ]
    return JsonResponse(data, safe=False)


def api_flight_detail(request, id):
    flight = get_object_or_404(Flight.objects.select_related("origin", "destination"), pk=id)
    data = {
        "id": flight.id,
        "origin": {"code": flight.origin.code, "city": flight.origin.city},
        "destination": {"code": flight.destination.code, "city": flight.destination.city},
        "duration": flight.duration,
        "capacity": flight.capacity,
        "booked_seats": flight.bookings.count(),
    }
    return JsonResponse(data)