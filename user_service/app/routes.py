from .views import RegView, LogInView, LogOutView, UpdateView, InfoView, RefreshView


def setup_routes(app):

    app.router.add_view("/registr", RegView)
    app.router.add_view("/login", LogInView)
    app.router.add_view("/logout", LogOutView)
    app.router.add_view("/update", UpdateView)
    app.router.add_view("/userinfo", InfoView)
    app.router.add_view("/refresh", RefreshView)
