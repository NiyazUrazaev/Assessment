from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from skilltests.models import SkillTestQuestion, SkillTestAnswer, SkillTest, \
    SkillTestDelegation, SkillQuestBlock, SkillTestQuestBlock, \
    SkillTestDelegationResult


class QuestionInline(admin.StackedInline):
    model = SkillTestAnswer
    extra = 2


class BlockInline(admin.TabularInline):
    model = SkillTestQuestBlock
    extra = 1


class DelegationProfileInline(admin.StackedInline):
    model = SkillTestDelegation.profiles.through
    fields = ["profile", "result"]
    readonly_fields = ("result", )
    extra = 1


@admin.register(SkillQuestBlock)
class QuestBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'count_questions')


@admin.register(SkillTestQuestion)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, ]


@admin.register(SkillTestDelegation)
class DelegationAdmin(admin.ModelAdmin):
    list_display = ('test',)
    add_fields = ('profiles', 'test')
    fields = ('test',)
    inlines = (DelegationProfileInline,)

    def get_fields(self, request, obj=None):
        if not obj:
            return self.add_fields
        return super().get_fields(request, obj)


@admin.register(SkillTest)
class TestAdmin(admin.ModelAdmin):
    filter_horizontal = ('blocks',)
    inlines = (BlockInline,)
    change_form_template = "admin_test/change_form.html"
    readonly_fields = ('count_of_quest', 'questions')

    def _response_post_save(self, request, obj):
        if "_delegation" in request.POST:
            test_delegation = SkillTestDelegation(
                test=obj
            )
            test_delegation.save()
            return redirect(reverse("admin:skilltests_skilltestdelegation_change",
                                    args=(test_delegation.pk,)))
        return super(TestAdmin, self)._response_post_save(request, obj)
