from flask import Flask, render_template, jsonify, request, Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args
from urllib import parse
import contentful
from forms import SearchBar
from math import ceil
from products import Products
from decouple import config





get_products = Products()

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
# mod = Blueprint('product_page', __name__)
# app.register_blueprint(mod)


@app.template_filter('get_image')
def get_image(input):
    try:
        return input.image[0]['secure_url']
    except AttributeError:
        pass

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop', methods=['GET','POST'])
@app.route('/shop/<query>', methods=['GET','POST'])
def store(**kwargs):

    search_form = SearchBar() # Searchbar HTML form


    if request.method =='POST':
        if search_form.validate_on_submit():
            search_query = search_form.query.data
            if request.args.get('page') == None:
                skip_num = 0
            else:
                skip_num = int(request.args.get('page'))*36
            return get_products.search_product(search_query, search_form, skip_num)


    # try:
    #     current_page = int(request.args['page_num'])
    #     skip_num = (current_page-1)*PRODUCT_LIMIT
    #
    # except:
    #     skip_num = 0 # products to skip

    elif kwargs.get('query') != None:
        if request.args.get('page') == None:
            skip_num = 0
        else:
            skip_num = int(request.args.get('page'))*36
        products = get_products.get_by_category(query=kwargs.get('query'), skip_num=skip_num)

    else:
        print('hi')
        if request.args.get('page') == None:
            skip_num = 0
        else:
            skip_num = int(request.args.get('page'))*36

        products = get_products.all_products(skip_num=skip_num)


    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(show_single_page= True,page=page, per_page=37, total=int(products.total), search=False, record_name='products')
    # pages = ceil(products.total/PRODUCT_LIMIT) # Total Number of pages

    return render_template('store.html', products=products, search_form=search_form, pagination=pagination)

# def search_results(search_query, search_form, skip_num):
#     products = get_products.search_product(search_query=search_query,skip_num=0)
#
#     page = request.args.get(get_page_parameter(), type=int, default=1)
#     pagination = Pagination(page=page, per_page=36, total=products.total, search=False, record_name='products')
#
#     return render_template('store.html', products=products, search_form=search_form, pagination=pagination)

@app.route('/detail/<product_id>')
def get_product_detail(product_id):
    product = get_products.get_product_detail(product_id)

    return render_template('detail.html', product=product)





if __name__ =='__main__':
    app.run()
