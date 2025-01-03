from django.contrib import admin
from .models import Brand, Country, Vehicle, Comment, VehicleImage, Client

admin.site.register(Client)

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1  # Número de formularios vacíos para nuevas imágenes
    fields = ['image', 'is_main']
    max_num = 8  # Máximo de imágenes permitidas por vehículo

    def save_new(self, form, commit=True):
        """
        Ensure only one image is marked as 'is_main' per vehicle when adding new images.
        """
        if form.cleaned_data['is_main']:
            VehicleImage.objects.filter(vehicle=form.cleaned_data['vehicle'], is_main=True).update(is_main=False)
        return super().save_new(form, commit)

    def save_existing(self, form, obj, commit=True):
        """
        Ensure only one image is marked as 'is_main' per vehicle when updating existing images.
        """
        if form.cleaned_data['is_main']:
            VehicleImage.objects.filter(vehicle=obj.vehicle, is_main=True).update(is_main=False)
        return super().save_existing(form, obj, commit)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'get_brand_name', 'get_country_name', 'model', 'engine_displacement',
        'fuel_type', 'number_of_doors', 'year_of_manufacture', 'price_in_usd'
    )
    inlines = [VehicleImageInline]  # Incluir las imágenes como inlines

    # Agregar filtros en la barra lateral del admin
    list_filter = ('brand', 'country_of_manufacture', 'fuel_type', 'year_of_manufacture')

    # Agregar cuadro de búsqueda en la parte superior del admin
    search_fields = ('model', 'brand__name', 'country_of_manufacture__name')

    def get_brand_name(self, obj):
        return obj.brand.name
    get_brand_name.short_description = 'Marca'

    def get_country_name(self, obj):
        return obj.country_of_manufacture.name
    get_country_name.short_description = 'País de Fabricación'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_text', 'created_at', 'vehicle')
    list_filter = ('created_at', 'user', 'vehicle')
    search_fields = ('text', 'user__username', 'vehicle__model')

    def short_text(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    short_text.short_description = 'Comment'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
