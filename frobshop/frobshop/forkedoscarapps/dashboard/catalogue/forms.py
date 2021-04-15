from oscar.apps.dashboard.catalogue import forms as base_forms
from oscar.core.loading import get_model

Partner = get_model('partner', 'Partner')


class StockRecordForm(base_forms.StockRecordForm):

    class Meta(base_forms.StockRecordForm.Meta):
        # fields = ['partner', 'partner_sku', 'price_currency', 'price_excl_tax', 'price_retail', 'cost_price',
        #           'num_in_stock', 'low_stock_threshold', 'stock_nickname']
        base_forms.StockRecordForm.Meta.fields.extend(['stock_nickname'])


class ProductForm(base_forms.ProductForm):
    
    class Meta(base_forms.ProductForm.Meta):
        base_forms.ProductForm.Meta.fields.extend(['nick_name'])

