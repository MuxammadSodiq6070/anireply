from django.db import models

class Anime(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.URLField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField(default=0)
    badge = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Episode statistikasi
    total_episodes = models.PositiveIntegerField(default=0, help_text="Anime nechta qismdan iborat")
    dubbed_episodes = models.PositiveIntegerField(default=0, help_text="Nechta qismi dublyaj qilingan")

    # Home uchun flaglar
    is_banner = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_new_episode = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def dubbed_percentage(self):
        if self.total_episodes == 0:
            return 0
        return int((self.dubbed_episodes / self.total_episodes) * 100)


class Episode(models.Model):
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name='episodes'
    )
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True, null=True)
    youtube_link = models.URLField(help_text="YouTube video link")
    image = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['number']
        unique_together = ('anime', 'number')

    def __str__(self):
        return f"{self.anime.title} - Episode {self.number}"

    def embed_url(self):
        """
        Oddiy youtube linkni embed formatga aylantiradi
        """
        if "watch?v=" in self.youtube_link:
            video_id = self.youtube_link.split("watch?v=")[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.youtube_link