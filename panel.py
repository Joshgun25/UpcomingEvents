from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for)

panel = Blueprint(name='panel', import_name=__name__,
                  template_folder='templates')


@panel.route("/panel/admin")
def admin_panel_page():
    auth = session.get('auth_type')
    if(auth != 'admin'):
        flash("Unauthorized request", 'danger')
        return redirect(url_for("home.home_page"))
    return render_template("admin_panel_page.html")


@panel.route("/panel/organizer")
def organizer_panel_page():
    auth = session.get('auth_type')
    if(auth != 'organizer'):
        flash("Unauthorized request", 'danger')
        return redirect(url_for("home.home_page"))
    return render_template("organizer_panel_page.html")

