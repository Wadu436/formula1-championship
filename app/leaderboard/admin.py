from django import db, forms
from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple

from . import models


class ModelAdminWithoutRelatedEdits(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return form


# Register your models here.
@admin.register(models.Team, site=admin.site)
class TeamAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("name",)


@admin.register(models.Track, site=admin.site)
class TrackAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("location", "name")


class ConstructorMultiplierInline(admin.TabularInline):
    model = models.ConstructorMultiplier
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in formset.form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset


class ChampionshipDriverInline(admin.TabularInline):
    model = models.ChampionshipDriver
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in formset.form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset


@admin.register(models.Championship, site=admin.site)
class ChampionshpipAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("name",)
    inlines = [ChampionshipDriverInline, ConstructorMultiplierInline]


@admin.register(models.Driver, site=admin.site)
class DriverAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("name", "nickname", "team", "country", "number")


class RaceEntryInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        # Amount of forms
        num_entries = len(self.forms)
        qualifying_positions = set()
        finish_positions = set()
        drivers = set()
        for form in self.forms:
            try:
                if form.cleaned_data:
                    # Validate common
                    if not form.cleaned_data["driver"]:
                        form.instance.driver = None
                        form.instance.team = None
                        form.instance.bot = True

                    elif not form.cleaned_data["bot"]:
                        if (
                            "finish_position" not in form.cleaned_data
                            or form.cleaned_data["finish_position"] is None
                        ):
                            raise forms.ValidationError(
                                "Every entry needs a 'finish position'"
                            )
                        else:
                            if form.cleaned_data["finish_position"] in finish_positions:
                                raise forms.ValidationError(
                                    "Every 'finish position' needs to be unique "
                                )
                            if (
                                not 0
                                < form.cleaned_data["finish_position"]
                                <= num_entries
                            ):
                                raise forms.ValidationError(
                                    f"Finish position {form.cleaned_data['finish_position']} needs to be between 1 and {num_entries} (The number of race entries)"
                                )

                            finish_positions.add(form.cleaned_data["finish_position"])

                        if (
                            "qualifying_position" in form.cleaned_data
                            and form.cleaned_data["qualifying_position"] is not None
                        ):
                            if (
                                form.cleaned_data["qualifying_position"]
                                in qualifying_positions
                            ):
                                raise forms.ValidationError(
                                    "Every 'qualifying position' needs to be unique "
                                )
                            if (
                                not 0
                                < form.cleaned_data["qualifying_position"]
                                <= num_entries
                            ):
                                raise forms.ValidationError(
                                    f"Qualifying position {form.cleaned_data['qualifying_position']} needs to be between 1 and {num_entries} (The number of race entries)"
                                )

                            qualifying_positions.add(
                                form.cleaned_data["qualifying_position"]
                            )

                        if not form.cleaned_data["driver"]:
                            raise forms.ValidationError(
                                f"Not all non-bot entries have a driver or a team."
                            )
                        else:
                            if form.cleaned_data["driver"] in drivers:
                                raise forms.ValidationError(
                                    f"A driver can only have one entry per race ({form.cleaned_data['driver'].name})."
                                )
                            drivers.add(form.cleaned_data["driver"])

                    # Bot
                    else:
                        form.instance.driver = None
                        form.instance.team = None

            except AttributeError:
                pass
        # Pass 2
        leftover_quali = sorted(
            list(set(range(1, num_entries + 1)).difference(qualifying_positions))
        )
        i = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    # Bot quali position
                    if form.instance.bot:
                        if form.cleaned_data["qualifying_position"] is None:
                            form.instance.qualifying_position = leftover_quali[i]
                            i += 1

            except AttributeError:
                pass

class SprintRaceEntryInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        # Amount of forms
        num_entries = len(self.forms)
        qualifying_positions = set()
        finish_positions = set()
        drivers = set()
        for form in self.forms:
            try:
                if form.cleaned_data:
                    # Validate common
                    if not form.cleaned_data["driver"]:
                        form.instance.driver = None
                        form.instance.team = None
                        form.instance.bot = True

                    elif not form.cleaned_data["bot"]:
                        if (
                            "finish_position" not in form.cleaned_data
                            or form.cleaned_data["finish_position"] is None
                        ):
                            raise forms.ValidationError(
                                "Every entry needs a 'finish position'"
                            )
                        else:
                            if form.cleaned_data["finish_position"] in finish_positions:
                                raise forms.ValidationError(
                                    "Every 'finish position' needs to be unique "
                                )
                            if (
                                not 0
                                < form.cleaned_data["finish_position"]
                                <= num_entries
                            ):
                                raise forms.ValidationError(
                                    f"Finish position {form.cleaned_data['finish_position']} needs to be between 1 and {num_entries} (The number of race entries)"
                                )

                            finish_positions.add(form.cleaned_data["finish_position"])

                        if not form.cleaned_data["driver"]:
                            raise forms.ValidationError(
                                f"Not all non-bot entries have a driver or a team."
                            )
                        else:
                            if form.cleaned_data["driver"] in drivers:
                                raise forms.ValidationError(
                                    f"A driver can only have one entry per race ({form.cleaned_data['driver'].name})."
                                )
                            drivers.add(form.cleaned_data["driver"])

                    # Bot
                    else:
                        form.instance.driver = None
                        form.instance.team = None

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

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in formset.form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset


class DNAEntryInline(admin.TabularInline):
    model = models.DNAEntry
    extra = 0

    class Media:
        js = (
            "leaderboard/jquery-3.6.0.min.js",
            "leaderboard/admin/raceentry_tabular.js",
        )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in formset.form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset


class SprintRaceEntryInline(admin.TabularInline):
    model = models.SprintRaceEntry
    template = "leaderboard/admin/raceentry_tabular_inline.html"
    formset = SprintRaceEntryInlineFormset
    extra = 0

    class Media:
        js = (
            "leaderboard/jquery-3.6.0.min.js",
            "leaderboard/admin/raceentry_tabular.js",
        )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in formset.form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset


class SprintDNAEntryInline(admin.TabularInline):
    model = models.SprintDNAEntry
    extra = 0

    class Media:
        js = (
            "leaderboard/jquery-3.6.0.min.js",
            "leaderboard/admin/raceentry_tabular.js",
        )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in formset.form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset


@admin.register(models.Race, site=admin.site)
class RaceAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("__str__", "championship", "track")
    list_filter = ("championship", "track")
    inlines = [
        RaceEntryInline,
        DNAEntryInline,
    ]
    # change_form_template = "leaderboard/admin/race_change_form.html"

@admin.register(models.SprintRace, site=admin.site)
class SprintRaceAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("__str__", "championship", "track")
    list_filter = ("championship", "track")
    inlines = [
        SprintRaceEntryInline,
        SprintDNAEntryInline,
    ]
    # change_form_template = "leaderboard/admin/race_change_form.html"


class RuleEntryInline(admin.TabularInline):
    model = models.RuleEntry
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in formset.form.base_fields.values():
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset


@admin.register(models.RuleChapter, site=admin.site)
class RulesAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("name",)
    name = "Rules"
    inlines = [
        RuleEntryInline,
    ]


@admin.register(models.FAQ, site=admin.site)
class RulesAdmin(ModelAdminWithoutRelatedEdits):
    list_display = ("question",)
    name = "FAQ"
