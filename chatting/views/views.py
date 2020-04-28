from django.shortcuts import render,redirect
from helpline.models import Report
from ..models import Chatting, Chatting_room

def enter_chatting_room(request, report_id):
    report = Report.objects.get(id=report_id)
    
    author = report.author
    lawyer = report.lawyer
    
    try:
        room = Chatting_room.objects.get(author=author, lawyer=lawyer)
    except:
        room = Chatting_room.objects.create(author=author, lawyer=lawyer)
    
    context = {
        'room': room,
        # 'chatting': room.chatting_set.all(),
        'lawyer': lawyer,
    }
    return render(request, 'chatting/chatting_room.html', context)
