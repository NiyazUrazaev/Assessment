from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from test360.models import PollQuestion, PollAnswer, Poll, PollDelegation


class QuestionInLine(admin.StackedInline):
    """Запрещаем редактирование"""
    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super(QuestionInLine, self).has_change_permission(request, obj=obj)

    def has_add_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super(QuestionInLine, self).has_change_permission(request, obj=obj)

    model = PollAnswer
    fields = ['answer', ]
    add_fields = ('answer', )
    extra = 1


@admin.register(PollQuestion)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine, ]


class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('profile', 'question', 'answer')


admin.site.register(PollAnswer, AnswerAdmin)
admin.site.register(PollDelegation)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    change_form_template = "admin_test/change_form.html"

    def _response_post_save(self, request, obj):
        if "_delegation" in request.POST:
            test_delegation = PollDelegation(
                poll=obj
            )
            test_delegation.save()
            return redirect(reverse("admin:test360_polldelegation_change",
                            args=(test_delegation.pk, )))
        return super(PollAdmin, self)._response_post_save(request, obj)

