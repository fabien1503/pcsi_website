from django.contrib import admin


from .models import Colle, Note, GroupColle


class NoteInLine(admin.TabularInline):
	model = Note


class ColleAdmin(admin.ModelAdmin):
	inlines=[NoteInLine,]
	list_display=["colleur", "date","groupColle", "eleves"]

class GroupColleAdmin(admin.ModelAdmin):
	list_display=["__str__", "listeEleves"]

admin.site.register(Colle, ColleAdmin)
admin.site.register(GroupColle, GroupColleAdmin)