import qrcode
import base64
from io import BytesIO

from django.contrib import admin
from django.db import models
from django.utils.html import mark_safe

from ckeditor.widgets import CKEditorWidget

from apps.web.models import (
    AppUser,
    Bot,
    CallbackQuery,
    Chat,
    Condition,
    Event,
    Handler,
    Message,
    Photo,
    Quest,
    Response,
    Session,
    Step,
    Update,
)

from apps.web.models.condition import QR_CODE
from apps.web.forms import ConditionForm

class SessionInline(admin.TabularInline):
    model = Session


class StepInline(admin.TabularInline):
    model = Step


class ResponseInline(admin.TabularInline):
    model = Response
    fields = ('id', 'title', 'on_true', 'as_reply', 'priority', )
    readonly_fields = ('id',)


class PhotoInline(admin.TabularInline):
    model = Photo
    readonly_fields = ('url',)
    fields = ('url', 'height', 'width', 'file_size',)

    def has_add_permission(self, request):
        return False


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    model = Photo
    list_display = ('id', 'message', 'get_file_size', 'width', 'height')

    fields = ('file_id', 'message', 'width', 'height', 'file_size', 'url')

    readonly_fields = ('url', 'file_id',)

    def get_file_size(self, obj):
        labels = [
            ('Bytes', 1), ('Kb', 1024), ('Mb', 1024**2), ('Gb', 1024**3),
        ]
        i = 0
        while obj.file_size > labels[i+1][1] and i+1 < len(labels):
            i += 1

        return f'{int(obj.file_size / labels[i][1])} {labels[i][0]}'


class HandlerInline(admin.TabularInline):
    model = Handler
    readonly_fields = ('id', )
    fields = ('id', 'ids_expression', 'title',)
    fk_name = 'step'


class ConditionInline(admin.TabularInline):
    model = Condition
    form = ConditionForm
    readonly_fields = ('id',)
    fields = ('id', 'value', 'matched_field', 'rule',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'token',)
    list_filter = ('enabled', 'owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'from_user', 'date',)
    list_filter = ('from_user', 'chat',)
    inlines = (PhotoInline, )


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_filter = ('bot',)
    list_display = ('update_id', 'message',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'username', 'type',)
    readonly_fields = ('current_keyboard',)


@admin.register(CallbackQuery)
class CallbackQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'data',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    inlines = (StepInline,)


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    form = ConditionForm
    list_display = ('rule', 'quest', 'handler', 'qr_code')
    list_filter = ('rule', )
    readonly_fields = ('created', 'modified', 'qr_code')
    fieldsets = (
        (None, {
            'fields': (
                'rule',
                'value',
                'created',
                'modified',
                'qr_code'
            ),
        }),
        ('Handler', {
            'fields': (
                'handler',
            )
        }),
    )

    def quest(self, obj):
        return obj.handler.step.quest

    def qr_code(self, obj):
        if obj.rule == QR_CODE:
            image = qrcode.make('https://telegram.me/share/url?url={}'.format(obj.value))
            buffered = BytesIO()
            image.get_image().save(buffered, format="PNG")
            return mark_safe(u'<img src="data:image/png;base64,{}" style="max-width: 200px;"/>'.format(
                base64.b64encode(buffered.getvalue()).decode()
            ))
        return None


@admin.register(Handler)
class HandlerAdmin(admin.ModelAdmin):
    inlines = (ConditionInline, ResponseInline)

    list_display = ('title', 'step',)

    list_filter = ('step', 'enabled_on', )

    fieldsets = (
        (None, {
            'fields': (
                'enabled_on',
                'title',
                'step',
                'ids_expression',
            )
        }),
        ('Actions', {
            'fields': (
                'step_on_success',
                'step_on_error',
            )
        }),
        ('Extra', {
            # 'classes': ('collapse',),
            'fields': (
                'redirects',
            )
        })
    )

    ordering = ('step',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
    list_filter = ('handler__step', 'handler')
    list_display = ('title', 'on_true', 'step_number',)
    ordering = ('handler__step', 'created',)

    def step_number(self, obj):
        return obj.handler.step.number if obj.handler else None


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('created', 'user',)
    readonly_fields = ('created', 'modified')
    fields = (
        'created',
        'modified',
        'user',
        'step',
    )


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    inlines = (HandlerInline,)
    list_display = ('title', 'number', 'is_initial', )
    list_filter = ('quest', )


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    exclude = ('groups',)
    readonly_fields = ('password', 'last_login')
    list_display = ('username', 'email', 'device_uid', 'is_staff', 'current_session')
    list_filter = (
        ('is_staff', admin.BooleanFieldListFilter),
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'current_session',
                'email',
                'device_uid',
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('password', 'user_permissions', 'last_login'),
        }),
    )
