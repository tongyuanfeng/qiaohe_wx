@main_blueprint.route('/login', methods=['GET', 'POST'])
@openid.loginhandler
def login():
    """View function for login.

       Flask-OpenID will be receive the Authentication-information
       from relay party.
    """

    # Create the object for LoginForm
    form = LoginForm()
    # Create the object for OpenIDForm
    openid_form = OpenIDForm()

    # Send the request for login to relay party(URL).
    if openid_form.validate_on_submit():
        return openid.trg_login(
            openid_form.openid_url.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname'])

    # Try to login the relay party failed.
    openid_errors = openid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")

    # Will be check the account whether rigjt.
    if form.validate_on_submit():

        # Using session to check the user's login status
        # Add the user's name to cookie.
        # session['username'] = form.username.data

        user = User.query.filter_by(username=form.username.data).one()

        # Using the Flask-Login to processing and check the login status for user
        # Remember the user's login status. 
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id))

        flash("You have been logged in.", category="success")
        return redirect(url_for('blog.home'))

    return render_template('login.html',
                           form=form,
                           openid_form=openid_form)




@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    """View function for logout."""

    # Remove the username from the cookie.
    # session.pop('username', None)

    # Using the Flask-Login to processing and check the logout status for user.
    logout_user()

    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())
    flash("You have been logged out.", category="success")
    return redirect(url_for('main.login'))





