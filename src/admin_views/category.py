from src.admin_views.base import SecureModelView

class CategoryView(SecureModelView):
    create_modal = True
    edit_modal = True
    can_delete = True
    column_labels = {
        "name": "Category Name",
        "products": "Products"
    }
    column_list = ["name", "products"]
    column_searchable_list = ["name"]