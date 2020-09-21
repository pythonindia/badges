from flask import flash, redirect, render_template, request, session, url_for

from badges import app
from badges.forms import BadgeForm, VerifyEmailForm, VerifyRegistrationForm
from badges.models import Attendee


@app.route("/", methods=["GET", "POST"])
def index():
    form = VerifyEmailForm()
    if form.validate_on_submit():
        attendee = Attendee.find_by_email(email=form.email.data)

        if not attendee:
            return redirect(url_for("buy_tickets"))

        return redirect(url_for("verify_registration"))

    return render_template("index.html", form=form)


@app.route("/buy-tickets")
def buy_tickets():
    # TODO: This can possibly be merged with index
    # Just a boilerplate for now
    return render_template("buy-tickets.html")


@app.route("/verify-registration", methods=["GET", "POST"])
def verify_registration():
    form = VerifyRegistrationForm()
    if form.validate_on_submit():
        booking_id = form.booking_id.data
        token = form.token.data

        if not Attendee.verify(booking_id=booking_id, token=token):
            flash("Invalid booking id or token")
            return render_template("verify-registration.html", form=form)

        attendee = Attendee.find_by_booking_id(booking_id=booking_id)
        session["uuid"] = attendee.uuid

        return redirect(url_for("view_badge", id=attendee.id))

    return render_template("verify-registration.html", form=form)


@app.route("/logout")
def logout():
    session.pop("uuid", None)
    flash("You are logged out")
    return redirect(url_for("verify_registration"))


@app.route("/<id>")
def view_badge(id: str):
    attendee = Attendee.find_by_id(id=id)
    if not attendee:
        flash("Attendee is not registered")
        return redirect("404.html", error=error)

    return render_template("badge.html", attendee=attendee)


@app.route("/<id>/edit", methods=["GET", "POST"])
def edit_badge(id: str):
    attendee = Attendee.find_by_id(id=id)
    if not attendee:
        flash("Attendee is not registered")
        return redirect("404.html", error=error)

    if "uuid" not in session:
        flash("Please verify your registration first")
        return redirect(url_for("verify_registration"))

    if session["uuid"] != attendee.uuid:
        flash("You are not auuthorized to edit this page")
        return redirect(url_for("view_badge", id=attendee.uuid))

    form = BadgeForm(
        fullname=attendee.fullname,
        avatar_url=attendee.avatar_url,
        username=attendee.username,
        twitter_id=attendee.twitter_id,
        about=attendee.about,
    )

    if form.validate_on_submit():
        a = Attendee.find_by_id(form.username.data)
        if a and a.uuid != attendee.uuid:
            form.username.errors.append(
                "This username already exists. Please choose another one."
            )

        attendee.fullname = form.fullname.data
        attendee.avatar_url = form.avatar_url.data
        attendee.username = form.username.data
        attendee.twitter_id = form.twitter_id.data
        attendee.about = form.about.data

        attendee.update()

        flash("Badge information updated")
        return redirect(url_for("view_badge", id=attendee.id))

    return render_template("edit-badge.html", form=form)


@app.route("/<id>/download")
def download_badge(id: str):
    # ---
    # This is unimplemented now. It redirects back to the badge page.
    # Possible ideas:
    # Take the format of download from query parameters and generate the file
    # Allow the attendees to download only their own badge
    # ---
    return redirect(url_for("view_badge", id=id))
