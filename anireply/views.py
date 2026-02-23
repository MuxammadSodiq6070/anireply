from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Anime, Episode

# Home page
from django.shortcuts import render, redirect
from .models import Anime
def home_page(request):
    # Bannerlar, mashhurlar va yangi qismlar uchun filterlar
    banners = Anime.objects.filter(is_banner=True)
    popular = Anime.objects.filter(is_popular=True)
    new_episodes = Anime.objects.filter(is_new_episode=True)

    # Janrlar: distinct janrlarni olish
    genres = Anime.objects.values_list('genre', flat=True).distinct()

    context = {
        'banners': banners,
        'popular_animes': popular,
        'new_episodes_animes': new_episodes,
        'genres_list': genres,
    }
    return render(request, 'home.html', context)
    # Banner animelar
    banners = Anime.objects.filter(is_banner=True)
    
    # Popular animelar
    popular_animes = Anime.objects.filter(is_popular=True)
    
    # Yangi qismlar
    new_episodes = Anime.objects.filter(is_new_episode=True)
    
    # Janrlar (unique values)
    genres = Anime.objects.values_list('genre', flat=True).distinct()
    
    context = {
        'banners': banners,
        'popular_animes': popular_animes,
        'new_episodes': new_episodes,
        'genres': genres,
    }
    
    return render(request, 'home.html', context)
    # Banner uchun
    banners = Anime.objects.filter(is_banner=True)
    
    # Popular animelar
    popular = Anime.objects.filter(is_popular=True)
    
    # Yangi qismlar
    new_episodes = Anime.objects.filter(is_new_episode=True)
    
    # Janrlar (unique values)
    genres = Anime.objects.values_list('genre', flat=True).distinct()
    
    context = {
        'banners': banners,
        'popular_animes': popular,
        'new_episodes': new_episodes,
        'genres': genres,
    }
    
    return render(request, 'home.html', context)
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Barcha animelarni bazadan o'qish, so'nggi qo'shilgan 1 tasi banner uchun
    latest_anime = Anime.objects.order_by('-created_at').first()  # banner
    return render(request, 'home.html', {'latest_anime': latest_anime})

def anime_list(request):
    animes = Anime.objects.order_by('-created_at')  # barcha animelar
    return render(request, "animelar.html", {"animes": animes})
    animes = Anime.objects.all()  # Barcha animelarni chiqarish
    return render(request, "animelar.html", {"animes": animes})



def animelar_page(request):
    animes = Anime.objects.all()
    return render(request, 'animelar.html', {'animes': animes})



# Login
def login_page(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        data['error'] = "Username yoki parol xato"
    return render(request, 'login.html', context=data)


# Register
def register_page(request):
    data = {}
    if request.method == "POST":
        ism = request.POST.get("first_name")
        familya = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            data['error'] = "Bu foydalanuvchi mavjud!"
        else:
            user = User.objects.create(
                first_name=ism,
                last_name=familya,
                username=username
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', context=data)


# Logout
def logout_page(request):
    logout(request)
    return redirect("login")






from .models import Anime, Episode
import re
from django.shortcuts import render, get_object_or_404
from .models import Anime, Episode  # o'z modellaringizni import qiling


# anireply/views.py faylining boshida (eng yuqorida)
from django.shortcuts import render, get_object_or_404
import re
from .models import Anime, Episode   # o'zingizning modellaringiz

# anireply/views.py faylining boshida (eng yuqorida)
from django.shortcuts import render, get_object_or_404
import re
from .models import Anime, Episode   # o'zingizning modellaringiz

def extract_youtube_id(url: str) -> str:
    if not url:
        return ""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:[?&]|$)',
        r'(?:youtu\.be\/|embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""

def anime_detail(request, pk, episode_number=None):
    anime = get_object_or_404(Anime, pk=pk)
    episodes = anime.episodes.order_by('number').all()

    if episode_number is not None:
        current_episode = get_object_or_404(
            Episode,
            anime=anime,
            number=episode_number
        )
    else:
        current_episode = episodes.first()

    context = {
        "anime": anime,
        "episodes": episodes,
        "current_episode": current_episode,
    }

    if current_episode:
        youtube_url = current_episode.youtube_link  # field nomini o'zingiznikiga moslashtiring
        context['youtube_id'] = extract_youtube_id(youtube_url)

    return render(request, "anime_detail.html", context)


def anime_detail(request, pk, episode_number=None):
    # Anime obyektini olish
    anime = get_object_or_404(Anime, pk=pk)
    
    # Animega tegishli barcha qismlarni olish (tartiblangan bo'lsa yaxshi)
    episodes = anime.episodes.order_by('number').all()  # number bo'yicha tartiblash tavsiya etiladi
    
    # Joriy qismni aniqlash
    if episode_number is not None:
        current_episode = get_object_or_404(
            Episode,
            anime=anime,
            number=episode_number
        )
    else:
        # Default — birinchi mavjud qism (yoki None bo'lishi mumkin)
        current_episode = episodes.first()
    
    # Context ga qo'shimcha ma'lumotlar
    context = {
        "anime": anime,
        "episodes": episodes,
        "current_episode": current_episode,
    }
    
    # Agar joriy qism bo'lsa → youtube_id ni oldindan hisoblab qo'yamiz
    if current_episode:
        youtube_url = getattr(current_episode, 'youtube_link', '')  # field nomi to'g'ri ekanligiga ishonch hosil qiling
        context['youtube_id'] = extract_youtube_id(youtube_url)
    
    return render(request, "anime_detail.html", context)





# Faqat bir marta ishlatib, keyin o'chirib tashlang!
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'parol123')