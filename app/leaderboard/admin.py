from django import forms
from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Team, site=admin.site)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Track, site=admin.site)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("location", "name")


@admin.register(models.Championship, site=admin.site)
class ChampionshpipAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Driver, site=admin.site)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "team")

class RaceEntryInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        # Amount of forms
        num_entries = len(self.forms)
        for form in self.forms:
            try:
                if form.cleaned_data:
                    # Validate common
                    if 'finish_position' not in form.cleaned_data or not 0 < form.cleaned_data['finish_position'] <= num_entries:
                        raise forms.ValidationError(f"Finish position {form.cleaned_data['finish_position']} needs to be between 1 and {num_entries} (The number of race entries)")
                    if 'qualifying_position' not in form.cleaned_data or not 0 < form.cleaned_data['qualifying_position'] <= num_entries:
                        raise forms.ValidationError(f"Qualifying position {form.cleaned_data['qualifying_position']} needs to be between 1 and {num_entries} (The number of race entries)")

                    # Bot
                    if form.cleaned_data['bot']:
                        form.cleaned_data['driver'] = None
                        form.cleaned_data['team'] = None
                    else:
                        if not (form.cleaned_data['driver'] and form.cleaned_data['team']):
                            raise forms.ValidationError(f"Not all non-bot entries have a driver or a team.")
                    
            except AttributeError:
                pass

class RaceEntryInline(admin.TabularInline):
    model = models.RaceEntry
    template = "leaderboard/admin/raceentry_tabular_inline.html"
    formset = RaceEntryInlineFormset
    extra = 0
    class Media:
        js = (
            "leaderboard/jquery-3.6.0.min.js",
            "leaderboard/admin/raceentry_tabular.js",
        )

class DNAEntryInline(admin.TabularInline):
    model = models.DNAEntry
    extra = 0
    class Media:
        js = (
            "leaderboard/jquery-3.6.0.min.js",
            "leaderboard/admin/raceentry_tabular.js",
        )

@admin.register(models.Race, site=admin.site)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("__str__", "championship", "track")
    list_filter = ("championship", "track")
    inlines = [
        RaceEntryInline, DNAEntryInline
    ]
    # change_form_template = "leaderboard/admin/race_change_form.html"
