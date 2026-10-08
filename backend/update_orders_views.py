import os
import re

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Update CancelOrderView
old_cancel = """class CancelOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        from apps.orders.models import Order
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            if order.status in [Order.Status.PENDING, Order.Status.PAID]:
                order.status = Order.Status.CANCELLED
                order.save()
                return Response({"detail": "Order cancelled successfully."})
            return Response({"detail": "Cannot cancel this order."}, status=400)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)"""

new_cancel = """class CancelOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request, pk):
        from apps.orders.models import Order
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            if order.status in [Order.Status.PENDING, Order.Status.PAID]:
                order.status = Order.Status.CANCELLED
                order.save(update_fields=['status'])
                # Restore stock
                for item in order.items.all():
                    if item.product:
                        item.product.stock += item.quantity
                        item.product.save(update_fields=['stock'])
                return Response({"detail": "Order cancelled successfully."})
            return Response({"detail": "Cannot cancel this order."}, status=400)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)"""

content = content.replace(old_cancel, new_cancel)

# Update AdminOrderViewSet
old_admin_update = """    def perform_update(self, serializer):
        status_val = self.request.data.get('status')
        instance = serializer.instance
        from django.utils import timezone
        
        kwargs = {}
        if status_val:
            if status_val == 'delivered':
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
            elif status_val == 'paid':
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
                    
        serializer.save(**kwargs)"""

new_admin_update = """    def perform_update(self, serializer):
        status_val = self.request.data.get('status')
        instance = serializer.instance
        old_status = instance.status
        from django.utils import timezone
        from django.db import transaction
        
        kwargs = {}
        if status_val:
            if status_val == 'delivered':
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
            elif status_val == 'paid':
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
                    
        with transaction.atomic():
            serializer.save(**kwargs)
            # If status changed to cancelled from a non-cancelled state, restore stock
            if status_val == 'cancelled' and old_status != 'cancelled':
                for item in instance.items.all():
                    if item.product:
                        item.product.stock += item.quantity
                        item.product.save(update_fields=['stock'])
            # If status changed from cancelled to another state, deduce stock
            elif old_status == 'cancelled' and status_val and status_val != 'cancelled':
                for item in instance.items.all():
                    if item.product:
                        item.product.stock -= item.quantity
                        if item.product.stock < 0:
                            item.product.stock = 0
                        item.product.save(update_fields=['stock'])"""

content = content.replace(old_admin_update, new_admin_update)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated views.py with stock restoration logic.")
