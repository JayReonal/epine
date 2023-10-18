from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from pine.models import *
from pine.forms import *
# Create your views here.
@login_required
def rooms(request):
    rooms = Room.objects.filter(slug="supplier")

    return render(request, 'chat/rooms.html', {'rooms':rooms})
@login_required
def room(request,slug):
    # rooms = Room.objects.all()
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'chat/room.html', {'room':room, 'messages': messages, })

def room_delete(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return redirect('bidding')
    
    if request.method == 'POST':
        room.delete()
        return redirect('bidding')
  
    return render(request, 'chat/room_delete.html', {'room': room})

def bidding(request):
    rooms = Room.objects.exclude(slug="employee")
    bidding_processes = BiddingProcess.objects.all()
    if request.method == 'POST':
        roomform = RoomForm(request.POST)

        if roomform.is_valid():
            roomform.save()
            return redirect('bidding')
        
    else:
        roomform = RoomForm()

    if request.method == 'POST':
        biddingForm = BiddingForm(request.POST)

        if biddingForm.is_valid():
            biddingForm.save()
            return redirect('bidding')
        
    else:
        biddingForm = BiddingForm()


    return render(request, 'chat/bidding.html', {'rooms':rooms, 'roomform': roomform,
                                                 'bidding_processes': bidding_processes,
                                                 'biddingForm': biddingForm})

def bidder_win_list(request):
    bidders_win = BiddingProcess.objects.all()
    for bidding_process in bidders_win:
        bidding_process.total = bidding_process.calculate_total()

    context = {
        'bidders_win': bidders_win
    }
    return render (request, 'chat/bidders_win_list.html', context)