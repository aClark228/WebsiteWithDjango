from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import  Album, Song, Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404


class HomeView(generic.ListView):  #home page generic code
    template_name = 'music/home.html'
    def get_queryset(self):
        return Album.objects.all()

class IndexView(generic.ListView):
    model = Album  #album page generic code
    template_name = 'music/index.html'
    context_object_name = 'albums'
 # TIP because .ListView is used this is returned  in the variable object_list which is used in line 17 in index.html
class DetailView(generic.DetailView):
    model = Album
    template_name='music/detail.html'

class AlbumCreate(generic.CreateView):
    model = Album #the type of thing your trying to create is an album
    fields = ['artist', 'album_title', 'genre', 'album_logo', 'Format'] #things user is to fill in

    def form_valid(self, album):
        album.instance.key = self.request.user
        return super().form_valid(album)

class AlbumUpdate(UpdateView):
    model=Album
    fields = ['artist', 'album_title', 'genre', 'album_logo', 'Format']

    def form_valid(self, album):
        album.instance.key = self.request.user
        return super().form_valid(album)

class AlbumDelete(DeleteView):
    model=Album
    success_url = reverse_lazy('music:index')

class SongCreate(CreateView):
    model = Song
    fields= ['album', 'date_released', 'song_title', 'length', 'Box', 'Track_num']

    def form_valid(self, song):
        song.instance.album = self.request.album
        return super().form_valid(song)

class ProfileUpdate(UpdateView):
    model=Profile
    fields = '__all__'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            username = form.cleaned_data.get('username')
            user.save()
            if user is not None:
                if user.is_active:
                    request.user.username
                    login(request, user)
                    return redirect('music:home')
    else:
        form = UserRegisterForm()
    return render(request, 'music/registration_form.html', {'form': form})


#MAKE PROFILE FORM
@login_required(login_url='/music/login/')
def profile(request):
    #Checks to see wherher button method is POST
    if request.method == 'POST':
        #sets user form and profile
        u_form=UserUpdateForm(request.POST, instance=request.user)
        p_form=ProfileUpdateForm(request.POST,
            request.FILES,
            instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('music:home')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'music/edit_profile.html', context)
