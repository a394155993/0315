from django.contrib import admin
from ecshopapp import models
from django.contrib.auth.admin import UserAdmin



@admin.register(models.User_Member)  
class MyUserAdmin(UserAdmin):
    list_display = (
        'id',
        'user_name',
        'user_email',
        'user_nickname',
        'user_point',
        'is_superuser')
    list_filter = ['user_name']
    fieldsets = (
        (None, {'fields': ('user_email', 'password')}),
        ('Personal info', {'fields': ('user_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_email', 'user_name', 'password1', 'password2')}
         ),
    )
    search_fields = ('user_email',)
    ordering = ('id',)
    filter_horizontal = ()
    exclude = ['password']
    list_editable = ['user_point']


@admin.register(models.Goods)  
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'status', 'add_datetime']
    ordering = ['-add_datetime']


@admin.register(models.UserAddresses)
class UserAddressesAdmin(admin.ModelAdmin):
    list_display = ['user','receiver','is_default']