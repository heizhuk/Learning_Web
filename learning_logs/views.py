from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Topic,Entry
from .forms import TopicForm,EntryForm

def check_topic_owner(request,topic):
    if topic.owner != request.user:
        raise Http404

def index(request):
    return render(request,"learning_logs/index.htm")

@login_required
def topics(request):
    topics=Topic.objects.filter(owner=request.user).order_by("date_added")
    context={"topics":topics}
    return render(request,"learning_logs/topics.htm",context)

@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request,topic)
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic":topic,"entries":entries}
    return render(request,"learning_logs/topic.htm",context)

@login_required
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse("learning_logs:topics"))
    context = {"form":form}
    return render(request,"learning_logs/new_topic.htm",context)

@login_required
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request,topic)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse("learning_logs:topic",
                                                args=[topic.id]))
    context = {"topic":topic,"form":form}
    return render(request,"learning_logs/new_entry.htm",context)

@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request,topic)
    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(request.POST,instance=entry)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("learning_logs:topic",
                                                args=[topic.id]))
    context = {"entry":entry,"topic":topic,"form":form}
    return render(request,"learning_logs/edit_entry.htm",context)
# Create your views here.
