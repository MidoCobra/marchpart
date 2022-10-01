from django.contrib.admin import SimpleListFilter


class DuplicatSlugFilter(SimpleListFilter):
    """
    This filter is being used in django admin panel.
    """

    title = "Duplicates"
    parameter_name = "slug"

    def lookups(self, request, model_admin):
        return (("duplicates", "Duplicates"),)

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == "duplicates":
            return queryset.filter().exclude(
                id__in=[slug.id for slug in queryset.distinct("slug").order_by("slug")]
            )
