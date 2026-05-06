from src.admin_views.base import SecureModelView
from markupsafe import Markup
from flask_admin.form import ImageUploadField
from uuid import uuid4
from os import path

from src.config import Config

from src.admin_views.utils import generate_filename


class ProductView(SecureModelView):
    create_modal = True
    edit_modal = True
    details_modal = True
    can_view_details = True
    can_export = True
    column_editable_list = ["price", "name", "category"]
    column_labels = {
        "name": "სახელი",
        "price": "ფასი",
        "img": "სურათი"
                     }
    column_searchable_list = ["img", "price", "name"]
    column_filters = ["price"]
    column_formatters = {
        "img": lambda v, c, m, n: Markup(f"<img src = '/static/upload/{m.img}' width=128>")
    }
    column_list = ["img", "price", "name","category"]
    form_overrides = {"img": ImageUploadField}
    form_args = {"img": {
        "base_path": Config.UPLOAD_PATH,
        "namegen": generate_filename
    }}