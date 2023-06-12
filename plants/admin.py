from django.contrib import admin
from .models import Plant_details
# Register your models here.

class Plant_detailsAdmin(admin.ModelAdmin):
    list_display = ('common_names', 'edible_parts', 'gbif_id', 'name_authority', 'propagation_methods', 'synonyms', 'taxonomy', 'url', 'wiki_description', 'wiki_image', 'user')
    list_filter = ('common_names', 'edible_parts', 'gbif_id', 'name_authority', 'propagation_methods', 'synonyms', 'taxonomy', 'url', 'wiki_description', 'wiki_image', 'user')
    search_fields = ('common_names', 'edible_parts', 'gbif_id', 'name_authority', 'propagation_methods', 'synonyms', 'taxonomy', 'url', 'wiki_description', 'wiki_image', 'user')

admin.site.register(Plant_details, Plant_detailsAdmin)