from django import db, forms
from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple

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
    formfield_overrides = {
        db.models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(models.Driver, site=admin.site)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "team")

class RaceEntryInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        # Amount of forms
        num_entries = len(self.forms)
        qualifying_positions = set()
        finish_positions = set()
        for form in self.forms:
            try:
                if form.cleaned_data:
                    # Validate common
                    if 'finish_position' not in form.cleaned_data:
                        raise forms.ValidationError("Every entry needs a 'finish position'")
                    if form.cleaned_data['finish_position'] in finish_positions:
                        raise forms.ValidationError("Every 'finish position' needs to be unique ")
                    if not 0 < form.cleaned_data['finish_position'] <= num_entries:
                        raise forms.ValidationError(f"Finish position {form.cleaned_data['finish_position']} needs to be between 1 and {num_entries} (The number of race entries)")
                    if 'qualifying_position' not in form.cleaned_data:
                        raise forms.ValidationError("Every entry needs a 'qualifying position'")
                    if form.cleaned_data['qualifying_position'] in qualifying_positions:
                        raise forms.ValidationError("Every 'qualifying position' needs to be unique ")
                    if not 0 < form.cleaned_data['qualifying_position'] <= num_entries:
                        raise forms.ValidationError(f"Qualifying position {form.cleaned_data['qualifying_position']} needs to be between 1 and {num_entries} (The number of race entries)")

                    qualifying_positions.add(form.cleaned_data['qualifying_position'])
                    finish_positions.add(form.cleaned_data['finish_position'])

                    print(qualifying_positions)
                    print(finish_positions)

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
        RaceEntryInline, DNAEntryInline,
    ]
    # change_form_template = "leaderboard/admin/race_change_form.html"

class RuleEntryInline(admin.TabularInline):
    model = models.RuleEntry
    extra = 0

@admin.register(models.RuleChapter, site=admin.site)
class RulesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    name = "Rules"
    inlines = [RuleEntryInline, ]
