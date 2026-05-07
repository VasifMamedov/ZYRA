from flask import render_template, redirect, url_for, Blueprint, request, flash, abort
from uuid import uuid4
from os import path
from functools import wraps
from flask_login import login_required, current_user
from src.views.product.forms import ProductForm
from src.config import Config
from src.models import Product, Favorite, Review, Category, Image
from src.ext import db

product_blueprint = Blueprint("products", __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@product_blueprint.route('/view_product/<int:product_id>', methods=['GET'])
@login_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)

    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = Favorite.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first() is not None

    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()

    user_reviewed = False
    if current_user.is_authenticated:
        user_reviewed = Review.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first() is not None

    avg_rating = 0
    if reviews:
        avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)

    return render_template(
        "product/view_product.html",
        product=product,
        is_favorited=is_favorited,
        reviews=reviews,
        user_reviewed=user_reviewed,
        avg_rating=avg_rating
    )


@product_blueprint.route('/add_favorite/<int:product_id>')
@login_required
def add_favorite(product_id):
    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if not existing:
        favorite = Favorite(user_id=current_user.id, product_id=product_id)
        db.session.add(favorite)
        db.session.commit()
        flash('Product added to favorites!', 'success')
    else:
        flash('Product is already in your favorites.', 'warning')

    return redirect(url_for('products.view_product', product_id=product_id))


@product_blueprint.route('/remove_favorite/<int:product_id>')
@login_required
def remove_favorite(product_id):
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('Product removed from favorites.', 'info')

    next_page = request.args.get('next', url_for('products.view_product', product_id=product_id))
    return redirect(next_page)


@product_blueprint.route('/add_review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    existing = Review.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if existing:
        flash('You have already reviewed this product.', 'warning')
        return redirect(url_for('products.view_product', product_id=product_id))

    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()

    if not rating or not (1 <= rating <= 5):
        flash('Please select a rating between 1 and 5.', 'danger')
        return redirect(url_for('products.view_product', product_id=product_id))

    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    review.create()
    flash('Your review has been submitted!', 'success')
    return redirect(url_for('products.view_product', product_id=product_id))


@product_blueprint.route('/delete_review/<int:review_id>')
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id == current_user.id or current_user.role == 'admin':
        product_id = review.product_id
        review.delete()
        flash('Review deleted.', 'info')
        return redirect(url_for('products.view_product', product_id=product_id))

    flash('You are not authorized to delete this review.', 'danger')
    return redirect(url_for('main.index'))


@product_blueprint.route('/create_product', methods=["GET", "POST"])
@login_required
@admin_required
def create_product():
    form = ProductForm()
    form.category_id.choices = [(0, '-- No Category --')] + [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]
    if form.validate_on_submit():
        filename = None
        if form.img.data and form.img.data.filename:
            file = form.img.data
            _, extension = path.splitext(file.filename)
            filename = f"{uuid4()}{extension}"
            file.save(path.join(Config.UPLOAD_PATH, filename))

        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            img=filename,
            description=form.description.data,
            stock=form.stock.data
        )
        new_product.create()


        if form.category_id.data and form.category_id.data != 0:
            selected = Category.query.get(form.category_id.data)
            if selected:
                new_product.category.append(selected)
                new_product.save()


        for file in request.files.getlist('extra_images'):
            if file and file.filename:
                _, extension = path.splitext(file.filename)
                extra_filename = f"{uuid4()}{extension}"
                file.save(path.join(Config.UPLOAD_PATH, extra_filename))
                img = Image(product_id=new_product.id, img=extra_filename)
                img.save()

        flash('Product created successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('product/create_product.html', form=form)


@product_blueprint.route('/edit_product/<int:product_id>', methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(
        name=product.name,
        price=product.price,
        description=product.description,
        stock=product.stock,
    )
    form.category_id.choices = [(0, '-- No Category --')] + [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]
    if form.validate_on_submit():
        if form.img.data and form.img.data.filename:
            file = form.img.data
            _, extension = path.splitext(file.filename)
            filename = f"{uuid4()}{extension}"
            file.save(path.join(Config.UPLOAD_PATH, filename))
            product.img = filename

        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.stock = form.stock.data

        # Many-to-many
        if form.category_id.data and form.category_id.data != 0:
            selected = Category.query.get(form.category_id.data)
            if selected and selected not in product.category:
                product.category.append(selected)


        for file in request.files.getlist('extra_images'):
            if file and file.filename:
                _, extension = path.splitext(file.filename)
                extra_filename = f"{uuid4()}{extension}"
                file.save(path.join(Config.UPLOAD_PATH, extra_filename))
                img = Image(product_id=product.id, img=extra_filename)
                img.save()

        product.save()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('product/create_product.html', form=form)


@product_blueprint.route("/delete_product/<int:product_id>")
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    Review.query.filter_by(product_id=product_id).delete()
    Favorite.query.filter_by(product_id=product_id).delete()

    Image.query.filter_by(product_id=product_id).delete()

    db.session.delete(product)
    db.session.commit()

    flash('Product deleted.', 'info')
    return redirect(url_for('main.index'))
