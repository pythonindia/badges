from urllib.parse import urlencode

from flask import flash, redirect, render_template, request, session

from badges import app
from badges.forms import BadgeForm, VerifyEmailForm, VerifyRegistrationByOrderForm
from badges.models import Attendee
from badges.utils import get_prefixer


url_for = get_prefixer(app.config["URL_PREFIX"])

app.jinja_env.globals.update(url_for=url_for)


@app.route("/", methods=["GET", "POST"])
def verify_registration():
    form = VerifyRegistrationByOrderForm()
    if form.validate_on_submit():
        booking_id = form.booking_id.data
        order_id = form.order_id.data

        if not Attendee.find_by_booking_id(booking_id=booking_id):
            flash(
                "We don't seem to have your registration data yet or please check the booking ID you have entered. We reconcile the data every night."
            )
            return render_template("verify-registration.html", form=form)

        if not Attendee.verify(booking_id=booking_id, order_id=order_id):
            flash("Invalid booking id or order id")
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
        return render_template("404.html", message="Attendee is not registered.")

    tweet_link = "https://twitter.com/intent/tweet?" + urlencode(
        {
            "text": f"I am attending PyCon India 2020 on Oct 2-5.\n\nSee my badge here: {request.scheme}://{request.host}{url_for('view_badge', id=id)}.\n\nYou can get yours too at https://in.pycon.org/badges",
            "hashtags": "PyConIndia2020,python",
        }
    )

    return render_template("badge.html", attendee=attendee, tweet_link=tweet_link)


@app.route("/<id>/edit", methods=["GET", "POST"])
def edit_badge(id: str):
    attendee = Attendee.find_by_id(id=id)
    if not attendee:
        return render_template("404.html", message="Attendee is not registered.")

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
        else:
            attendee.fullname = form.fullname.data
            attendee.avatar_url = form.avatar_url.data
            attendee.username = form.username.data
            attendee.twitter_id = form.twitter_id.data
            attendee.about = form.about.data

            attendee.update()

            flash("Badge information updated")
            return redirect(url_for("view_badge", id=id))

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
