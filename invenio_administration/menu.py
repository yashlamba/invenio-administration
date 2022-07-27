from flask import request


class AdminMenu:
    def __init__(self):
        self._menu_items = []
        self._menu_key = "admin_navigation"

    @property
    def items(self):
        return self._menu_items

    def register_menu_entries(self, flask_menu_instance):
        main_menu = flask_menu_instance.submenu(self._menu_key)

        for menu_entry in self._menu_items:
            category = menu_entry.category
            name = menu_entry.name
            endpoint = menu_entry.endpoint
            order = menu_entry.order
            active_when = menu_entry.active_when

            if category:
                category_menu = main_menu.submenu(category)
                category_menu.register(text=category)
                category_menu.submenu(name).register(
                    endpoint=endpoint,
                    text=name,
                    order=order,
                    active_when=active_when or self.default_active_when
                )
            else:
                main_menu.submenu(name).register(
                    endpoint=endpoint,
                    text=name,
                    order=order,
                    active_when=active_when or self.default_active_when
                )

    def add_menu_item(self, item, index=None):
        is_menu_item = isinstance(item, MenuItem)

        if not is_menu_item:
            return

        if index:
            self._menu_items[index] = item
            return

        self._menu_items.append(item)

    def add_view_to_menu(self, view, index=None):
        menu_item = MenuItem(endpoint=view.endpoint_location_name, name=view.name, category=view.category)
        self.add_menu_item(menu_item, index)

    @staticmethod
    def default_active_when(self):
        return request.endpoint == self._endpoint


class MenuItem:
    def __init__(self, name="", endpoint="", category="", order=None, active_when=None):
        self.name = name
        self.endpoint = endpoint
        self.category = category
        self.order = order
        self.active_when = active_when