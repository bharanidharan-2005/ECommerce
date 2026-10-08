from django.contrib import admin

from .models import Order, OrderItem, PromoCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number", "user", "status", "payment_method",
        "total_price", "is_paid", "created_at",
    )
    list_filter = ("status", "is_paid", "payment_method")
    search_fields = ("order_number", "user__email", "email")
    list_editable = ("status",)
    inlines = (OrderItemInline,)
    date_hierarchy = "created_at"

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percentage", "active", "valid_from", "valid_until")
    list_filter = ("active",)
    search_fields = ("code",)
