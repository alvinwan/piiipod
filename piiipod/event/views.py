from flask import Blueprint, render_template, request, redirect, url_for, g
from piiipod.views import current_user, login_required
from .forms import EventForm, EventSignupForm, EventCheckinForm, \
    EventGenerateCodeForm
from piiipod.models import Group, Event, User, UserSetting, Membership, Signup,\
    GroupRole, EventRole, Base
from sqlalchemy.orm.exc import NoResultFound


event = Blueprint('event', __name__,
    url_prefix='/<string:group_url>/e/<int:event_id>/<string:event_url>')


@event.url_defaults
def add_ids(endpoint, values):
    values.setdefault('group_url', getattr(g, 'group_url', None))
    values.setdefault('event_id', getattr(g, 'event_id', None))
    values.setdefault('event_url', getattr(g, 'event_url', None))


@event.url_value_preprocessor
def pull_ids(endpoint, values):
    try:
        g.group_url = values.pop('group_url')
        g.group = Group.query.filter_by(url=g.group_url).one()
        g.event_id = values.pop('event_id')
        g.event_url = values.pop('event_url')
        g.event = Event.query.get(g.event_id)
        g.user = current_user()
        if g.user.is_authenticated:
            g.membership = Membership.query.filter_by(
                group_id=g.group.id,
                user_id=g.user.id,
                is_active=True).one_or_none()
            if g.membership:
                g.group_role = GroupRole.query.get(g.membership.role_id)
            else:
                g.group_role = None
            g.signup = Signup.query.filter_by(
                event_id=g.event.id,
                user_id=g.user.id,
                is_active=True).one_or_none()
            if g.signup:
                g.event_role = EventRole.query.get(g.signup.role_id)
            else:
                g.event_role = None
        else:
            g.membership = g.signup = g.group_role = g.event_role = None
    except NoResultFound:
        return 'No such event.'


def render_event(f, *args, **kwargs):
    """custom render for events"""
    from piiipod.views import render
    data = vars(g)
    data.update(kwargs)
    return render(f, *args, **data)


#########
# EVENT #
#########


@event.route('/')
@login_required
def home():
    """event homepage"""
    return render_event('event/index.html')


@event.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """event edit"""
    form = EventForm(request.form, obj=g.event)
    if request.method == 'POST' and form.validate():
        g.event.update(**request.form).save()
        return redirect(url_for('event.home'))
    return render_event('form.html',
        title='Edit Event',
        submit='save',
        form=form)


@event.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    """event signup"""
    form = EventSignupForm(request.form)
    choose_role = g.event.setting('choose_role').is_active
    if choose_role:
        form.role_id.choices = [(r.id, r.name) for r in EventRole.query.filter_by(
            event_id=g.event.id,
            is_active=True).all()]
    else:
        del form.role_id
    if g.user in g.event:
        return redirect(url_for('event.home', notif=7))
    if request.method == 'POST' and form.validate():
        if choose_role:
            role = {'role_id': request.form['role_id']}
        else:
            role = {'role': g.event.setting('role').value }
        signup = g.user.signup(g.event, **role)
        return redirect(url_for('event.home'))
    form.event_id.default = g.event.id
    form.user_id.default = g.user.id
    form.process()
    return render_event('form.html',
        title='Signup for %s' % event.name,
        submit='Confirm',
        form=form,
        back=url_for('event.home'))


@event.route('/leave')
@login_required
def leave():
    """leave event"""
    g.user.leave(g.event)
    return redirect(url_for('event.home'))


@event.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    """event checkin"""
    message = ''
    form = EventCheckinForm(request.form)
    if request.method == 'POST' and form.validate():
        setting = UserSetting.query.filter_by(
            name='authorize_code',
            value=request.form['code'].strip(),
            is_active=True).one_or_none()
        if setting:
            checkin = g.user.checkin(g.event, setting.user)
            return redirect(url_for('event.home', notif=8))
        message = 'Authorization failed.'
    form.event_id.default = g.event.id
    form.user_id.default = g.user.id
    form.process()
    return render_event('form.html',
        title='Checkin for %s' % event.name,
        message=message,
        submit='Checkin',
        form=form)


@event.route('/authorize', methods=['GET', 'POST'])
@login_required
def authorize():
    """event authorization (for checkin)"""
    form = EventGenerateCodeForm(request.form)
    setting = g.user.setting('authorize_code')
    if request.method == 'POST' and form.validate():
        n = 25
        setting.value = Base.hash(request.form['value']
            )[n:n+int(request.form['length'])]
        setting.save()
    message = 'Current code: %s' % setting.value
    return render_event('form.html',
        title='Authorization Code for %s' % event.name,
        message=message,
        submit='Regenerate',
        form=form,
        back=url_for('event.home'))