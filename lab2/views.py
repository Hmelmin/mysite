from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from db import DatabaseManager

db_manager = DatabaseManager()
db_manager.prepare()

# Create your views here.
def flights(request):
    if request.method == "GET":



        query = db_manager.SelectAllFlights()



        return render(request, 'lab2/flights.html', {"query": query})
    elif request.method == "POST":
        query = db_manager.SelectAllFlights()
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(int(request.POST.get("Delete").split("_")[1]))
            db_manager.DeleteFlight(request.POST.get("Delete").split("_")[1])
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit").split("_")[1]
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)
        elif request.POST.get("event") is not None:
            db_manager.event(request.POST.get("long"), request.POST.get("period"))
            return HttpResponseRedirect("flights")
        elif request.POST.get("trigger") is not None:
            db_manager.trigger()
            return HttpResponseRedirect("flights")



def find(request):
    # out_list = []
    # in_list = []
    # date = ""
    # plane = ""
    # airline = ""


    if request.method =='GET':
         airport_query = db_manager.SelectAllAirports()
         return render(request, 'lab2/find.html', {"airports": airport_query})
    elif request.method =='POST':
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(int(request.POST.get("Delete").split("_")[1]))
            db_manager.DeleteFlight(request.POST.get("Delete").split("_")[1])
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit").split("_")[1]
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)
        elif request.POST.get("event") is not None:
            db_manager.event()
            return HttpResponseRedirect("flights")
        elif request.POST.get("trigger") is not None:
            return HttpResponseRedirect("flights")

        out_list = request.POST.getlist("city_out")
        in_list = request.POST.getlist("city_in")
        plane = request.POST.get("plane")
        model = request.POST.get("model")
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        airline = request.POST.get("airline")
        query = db_manager.SearchSelect(out_list, in_list, date1,date2, plane, airline )
        # for key in request.__dict__:
            # print str(key)
        # request.path = "/lab3/flights"
        # request.path_info = "/lab3/flights"
        # url = reverse('flights', kwargs={'query': query})
        return render(request, "lab2/flights.html", {"query": query})

    # return render(request, 'lab3/find.html', )


def add(request):
    if request.method =='GET':
        airline_query = db_manager.SelectAllAirlines()
        airport_query = db_manager.SelectAllAirports()
        plane_query = db_manager.SelectAllPlanes()
        return render(request, 'lab2/add.html', {"airlines": airline_query, "airports": airport_query, "planes": plane_query})
    elif request.method == 'POST':
        print(request.POST)
        id = db_manager.GetLastIdFromFlights() +1
        db_manager.InsertFlight(id,request.POST.get("avia"),request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),request.POST.get("date_out"))
        # insert
        return HttpResponseRedirect("flights")
    return render(request, 'lab3/add.html', )

def edit(request, id):
    if request.method =='GET':
        query = db_manager.SelectFlightById(id)
        airline_query = db_manager.SelectAllAirlines()
        airport_query = db_manager.SelectAllAirports()
        plane_query = db_manager.SelectAllPlanes()
        return render(request, 'lab2/edit.html', {"airlines": airline_query, "airports": airport_query, "planes": plane_query, "query": query})
    elif request.method == 'POST':
        print(request.POST)
        db_manager.EditFlight(id,request.POST.get("avia"),request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),request.POST.get("date_out"))
        return HttpResponseRedirect("../flights")
    return render(request, 'lab2/edit.html', )

