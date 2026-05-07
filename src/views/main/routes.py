from flask import render_template, Blueprint, request, redirect, url_for, session
from flask_login import current_user, login_required
from src.models.product import Product
from src.models.category import Category
from src.models.review import Review
from src.models.favorite import Favorite
from src.models.user import User
from src.views.product.routes import admin_required
from src.config import Config

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'tr', 'ka']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_blueprint.route('/')
def index():
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    sort = request.args.get('sort', 'newest')

    products = Product.query
    if query:
        products = products.filter(Product.name.ilike(f'%{query}%'))
    if category_id:
        products = products.filter(Product.category.any(id=category_id))

    if sort == 'price_asc':
        products = products.order_by(Product.price.asc())
    elif sort == 'price_desc':
        products = products.order_by(Product.price.desc())
    elif sort == 'name_asc':
        products = products.order_by(Product.name.asc())
    else:
        products = products.order_by(Product.id.desc())

    categories = Category.query.order_by(Category.name).all()

    return render_template('main/index.html',
        product_list=products.all(),
        categories=categories,
        query=query,
        active_category=category_id,
        sort=sort
    )

@main_blueprint.route('/about')
def about():
    return render_template("main/about.html")

@main_blueprint.route('/favorites')
def favorites():
    favorite_products = current_user.products
    return render_template("product/favorites.html", favorite_products=favorite_products)


@main_blueprint.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html',
        product_count=Product.query.count(),
        user_count=User.query.count(),
        review_count=Review.query.count(),
        favorite_count=Favorite.query.count(),
        recent_reviews=Review.query.order_by(Review.created_at.desc()).limit(10).all()
    )