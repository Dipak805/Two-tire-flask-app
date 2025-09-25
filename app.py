from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import NotFound
from models import db, Product
from forms import ProductForm
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CSRFProtect(app)

    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
            print('Database initialized.')

    @app.route('/')
    def index():
        return redirect(url_for('list_products'))

    @app.route('/products')
    def list_products():
        query = Product.query

        search_term = request.args.get('q', '', type=str).strip()
        if search_term:
            like = f"%{search_term}%"
            query = query.filter(
                (Product.name.ilike(like)) | (Product.description.ilike(like))
            )

        sort = request.args.get('sort', 'created_at')
        order = request.args.get('order', 'desc')
        sort_attr = getattr(Product, sort, Product.created_at)
        if order == 'desc':
            sort_attr = sort_attr.desc()
        else:
            sort_attr = sort_attr.asc()
        products = query.order_by(sort_attr).all()

        return render_template('products/list.html', products=products, search_term=search_term, sort=sort, order=order)

    @app.route('/products/new', methods=['GET', 'POST'])
    def create_product():
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(
                name=form.name.data,
                price=form.price.data,
                description=form.description.data,
                image_url=form.image_url.data or None,
                stock=form.stock.data,
            )
            db.session.add(product)
            db.session.commit()
            flash('Product created successfully.', 'success')
            return redirect(url_for('list_products'))
        return render_template('products/form.html', form=form, mode='create')

    @app.route('/products/<int:product_id>')
    def view_product(product_id: int):
        product = Product.query.get(product_id)
        if not product:
            raise NotFound()
        return render_template('products/view.html', product=product)

    @app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
    def edit_product(product_id: int):
        product = Product.query.get(product_id)
        if not product:
            raise NotFound()
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            form.populate_obj(product)
            db.session.commit()
            flash('Product updated successfully.', 'success')
            return redirect(url_for('list_products'))
        return render_template('products/form.html', form=form, mode='edit', product=product)

    @app.route('/products/<int:product_id>/delete', methods=['POST'])
    def delete_product(product_id: int):
        product = Product.query.get(product_id)
        if not product:
            raise NotFound()
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted.', 'info')
        return redirect(url_for('list_products'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
