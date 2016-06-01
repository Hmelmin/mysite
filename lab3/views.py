from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from lab3.models import planes, airlines, departure, destination
from lab3.models import flights as flights_model



# Create your views here.
def flights(request):
    if request.method == "GET":
        query = flights_model.objects.all()
        return render(request, 'lab3/flights.html', {"query": query})
    elif request.method == "POST":
        query = flights_model.objects.all()
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(int(request.POST.get("Delete").split("_")[1]))
            flights_model.objects.filter(id=request.POST.get("Delete").split("_")[1]).delete()
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit").split("_")[1]
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)


def find(request):
    out_list = []
    in_list = []
    date = ""
    plane = ""
    airline = ""


    if request.method =='GET':
         departure_query = departure.objects.all()
         destination_query = destination.objects.all()
         return render(request, 'lab3/find.html', {"departure": departure_query, "destination": destination_query})
    elif request.method =='POST':
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(int(request.POST.get("Delete").split("_")[1]))
            flights_model.objects.filter(id=request.POST.get("Delete").split("_")[1]).delete()
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit").split("_")[1]
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)

        out_list = request.POST.getlist("city_out")
        in_list = request.POST.getlist("city_in")
        plane = request.POST.get("plane")
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        airline = request.POST.get("airline")
        result = flights_model.objects.all()
        if len(out_list)>0:
            out = departure.objects.filter(id__in=[int(x) for x in out_list])
            result = result.filter(departure_id__in=out)
        elif len(in_list)>0:
            list_in = destination.objects.filter(id__in=[int(x) for x in in_list])
            result = result.filter(destination_id__in=list_in)
        elif len(date1) > 0 and len(date2)>0:
            result = result.filter(departure_time__range=[date1,date2])
        elif len(plane) > 0:
            current_plane = planes.objects.get(model=plane)
            result = result.filter(plane_id=current_plane)
        elif len(airline) > 0:
            current_airline = airlines.objects.get(name=airline)
            result = result.filter(airlines_id=current_airline)

        # for key in request.__dict__:
            # print str(key)
        # request.path = "/lab3/flights"
        # request.path_info = "/lab3/flights"
        # url = reverse('flights', kwargs={'query': query})
        return render(request, "lab3/flights.html", {"query": result})

    return render(request, 'lab3/find.html', )


def add(request):
    airline_query = airlines.objects.all()
    departure_query = departure.objects.all()
    destination_query = destination.objects.all()
    plane_query = planes.objects.all()
    if request.method =='GET':

        return render(request, 'lab3/add.html', {"airlines": airline_query, "departure": departure_query , "destination": destination_query, "planes": plane_query})
    elif request.method == 'POST':
        print(request.POST)
        id = flights_model.objects.all().order_by("-id")[0].id + 1
        # db_manager.InsertFlight(id,request.POST.get("avia"),request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),request.POST.get("date_out"))
        new_flight = flights_model.objects.create(id=id,
                                                  airlines_id=airline_query.get(id=int(request.POST.get("avia"))),
                                                  departure_id=departure_query.get(id=int(request.POST.get("city_out"))),
                                                  destination_id=destination_query.get(id=int(request.POST.get("city_in"))),
                                                  plane_id=plane_query.get(id=int(request.POST.get("plane"))),
                                                  departure_time=request.POST.get("date_out"))
        new_flight.save()
        return HttpResponseRedirect("flights")
    return render(request, 'lab3/add.html', )

def edit(request, id):
    query = flights_model.objects.get(id=int(id))
    airline_query = airlines.objects.all()
    departure_query = departure.objects.all()
    destination_query = destination.objects.all()
    plane_query = planes.objects.all()
    if request.method =='GET':
        #query = db_manager.SelectFlightById(id)
        return render(request, 'lab3/edit.html', {"airlines": airline_query, "departure": departure_query,"destination": destination_query, "planes": plane_query, "query": query})
    elif request.method == 'POST':
        print(request.POST)
         # db_manager.EditFlight(id,request.POST.get("avia"),request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),request.POST.get("date_out"))

        query.airlines_id = airline_query.get(id=int(request.POST.get("avia")))
        query.departure_id = departure_query.get(id=int(request.POST.get("city_out")))
        query.destination_id = destination_query.get(id=int(request.POST.get("city_in")))
        query.plane_id = plane_query.get(id = int(request.POST.get("plane")))
        query.departure_time = request.POST.get("date_out")
        query.save()
        return HttpResponseRedirect("../flights")
    return render(request, 'lab3/edit.html', )

