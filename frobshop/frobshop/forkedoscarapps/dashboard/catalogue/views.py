from oscar.apps.dashboard.catalogue import views as base_views
# from oscar.core.loading import get_class, get_model

# StockRecordFormSet = get_class('dashboard.catalogue.formsets', 'StockRecordFormSet')
# Product = get_model('catalogue', 'Product')

class ProductCreateUpdateView(base_views.ProductCreateUpdateView):
    template_name = 'dashboard/catalogue/product_update.html'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.formsets['stockrecord_formset'] = StockRecordFormSet

    # def get_queryset(self):
    #     return filter_products_by_permission(Product.objects.all(), self.request.user)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

