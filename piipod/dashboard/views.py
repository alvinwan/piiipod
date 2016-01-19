from flask import Blueprint, request, redirect, url_for, g
from piipod.views import current_user, login_required
from piipod.group.forms import GroupForm


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.url_value_preprocessor
def load_current_user(_, __):
    g.user = current_user()


def render_dashboard(f, *args, **kwargs):
    """custom render for dashboard"""
    from piipod.views import render
    return render(f, *args, **kwargs)


#############
# DASHBOARD #
#############


@dashboard.route('/')
@login_required
def home():
    """user dashboard"""
    return render_dashboard('dashboard/index.html', groups=g.user.groups())


@dashboard.route('/g/', methods=['GET', 'POST'])
@login_required
def create_group():
    """create group form"""
    if request.form == 'POST':
        return redirect(url_for('group.home',
            group_id=Group.from_request().save().id))
    return render_dashboard('form.html',
        title='Create Group',
        submit='create',
        form=GroupForm())
