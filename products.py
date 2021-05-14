import contentful
from flask_paginate import Pagination, get_page_parameter
from flask import render_template, request

SPACE_ID = '0snbon2lhkq6'
ACCESS_TOKEN = '46di05bpPVP8VaAybkYp9TNqXeN_4frcbrFyEvZytg4'
client = contentful.Client(SPACE_ID, ACCESS_TOKEN)

PRODUCT_LIMIT = 36

class Products:

    def search_product(self, search_query, search_form, skip_num):
        products = client.entries({'limit': PRODUCT_LIMIT,
                               'content_type': 'samAndCoProducts',
                               'skip': skip_num,
                               'fields.title[match]': search_query})
        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(show_single_page= True, page=page, per_page=36, total=products.total, search=False, record_name='products')

        return render_template('store.html', products=products, search_form=search_form, pagination=pagination)


    # All Products
    def all_products(self, skip_num):
        products = client.entries({'limit': PRODUCT_LIMIT,
                                   'content_type': 'samAndCoProducts',
                                   'skip': skip_num})
        print(products)
        return products

    #Sort by Category
    def get_by_category(self, query, skip_num):
        products = client.entries({'limit': PRODUCT_LIMIT,
                                   'content_type': 'samAndCoProducts',
                                   'skip': skip_num,
                                  'fields.category[match]':query})
        return products





