from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from Forms import CreateUserForm, UpdateUserForm, LogInForm, ResetRequestForm, ResetPasswordForm, CreateRewardForm, CreateRentalForm, CreateProductForm, SortProductForm, CreateBikes, CreateFeedback
import shelve, User, Reward, Product, Rental, bikes, feedback
from flask_cors import CORS
from chat import get_response
from flask_mail import Mail, Message
import random


app = Flask(__name__)
CORS(app)

app.secret_key = 'hello'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "chloefaith2612@gmail.com"
app.config['MAIL_PASSWORD'] = "sypkxffsxyvwnhys"
mail = Mail(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home_admin')
def home_admin():
    return render_template('home_admin.html')

@app.post('/predict')
def predict():
    text = request.get_json().get('message')
    response = get_response(text)
    message = {'answer': response}
    return jsonify(message)


@app.route('/profile')
def profile():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()


    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    db = shelve.open("user.db", "w")
    users_dict = db["Users"]

    total_points = 0

    for key in users_dict:
        user = users_dict.get(key)
        stored_email = user.get_email()
        if "email" in session:
            email = session["email"]
            if stored_email == email:
                points = user.get_points()
                print("this is the user's points:", points)
                total_points += points
            else:
                points = 0
                total_points += points
        else:
            return render_template('profile.html')

    print(total_points)
    db["Users"] = users_dict
    db.close()

    reward_db = shelve.open('reward.db', 'r')
    rewards_dict = reward_db['Rewards']
    reward_db.close()

    rewards_list = []
    for key in rewards_dict:
        reward = rewards_dict.get(key)
        rewards_list.append(reward)

    redemptions_dict = {}
    redemption_db = shelve.open('redeem.db', 'c')

    try:
        redemptions_dict = redemption_db["Redemptions"]
        redemption_db.close()

        redemptions_list = []
        for key in redemptions_dict:
            past_rewards = redemptions_dict.get(key)
            redemptions_list.append(past_rewards)
    except KeyError:
        redemptions_list = []

    print("this is the redemptions", redemptions_dict)
    print("this is the rewards", rewards_dict)


    return render_template('profile.html', count=len(users_list), users_list=users_list, reward_count=len(rewards_list), rewards_list=rewards_list,
                           total_points=total_points, redemptions_list=redemptions_list)

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
            object_count = len(users_dict)
            object_id = object_count + 1

        except:
            print("Error in retrieving Users from user.db.")
            object_count = 0
            object_id = 1

        user = User.User(object_id, create_user_form.firstname.data, create_user_form.lastname.data, create_user_form.username.data, create_user_form.email.data, create_user_form.phone.data, create_user_form.password.data, create_user_form.password_confirm.data)
        users_dict[user.get_email()] = user
        db['Users'] = users_dict

        db.close()

        session['user_created'] =  user.get_firstname() + ' ' + user.get_lastname() + ' ' + '@'+ user.get_username()

        return redirect(url_for('logout'))
    return render_template('createUser.html', form=create_user_form)

@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/updateUser/<email>/', methods=['GET', 'POST'])
def update_user(email):
    update_user_form = UpdateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(email)
        user.set_firstname(update_user_form.firstname.data)
        user.set_lastname(update_user_form.lastname.data)
        user.set_username(update_user_form.username.data)
        user.set_phone(update_user_form.phone.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(email)
        update_user_form.firstname.data = user.get_firstname()
        update_user_form.lastname.data = user.get_lastname()
        update_user_form.username.data = user.get_username()
        update_user_form.phone.data = user.get_phone()

        session['user_updated'] =  user.get_firstname() + ' ' + user.get_lastname() + ' ' + '@'+ user.get_username()

        return render_template('updateUser.html', form=update_user_form)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    session['login'] = False

    login_form = LogInForm(request.form)
    if request.method == 'POST':
        if request.form['email'] == 'admin@rentcycle.com' and request.form['password'] == 'adminofrentcycle':
            session['login'] = True
            return redirect(url_for('home_admin'))
        else:
            #customer
            email = login_form.email.data
            password = login_form.password.data

            print("--call--",email, "password",password)
            error_num = checkUser(email, password)
            print('Return message number', error_num)

            if error_num == '1':
                error = 'Registered'
                session['login'] = True
                session['error'] = error
                session['email'] = email

                return redirect(url_for('logout', error=error))

            elif error_num == '2':
                error = 'Not Registered'
                session['login'] = False
                session['error'] = error
                flash('Email not registered.')

                return redirect(url_for('login', error=error))

            elif error_num == '3':
                error = 'Wrong Password'
                session['login'] = False
                session['error'] = error
                flash('Wrong password.')

                return redirect(url_for('login', error=error))

    return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
    session.pop('User', None)
    return render_template('logout.html')

@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    email = None
    form = ResetRequestForm(request.form)
    if request.method == 'POST' and form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()
        list = []
        for key in users_dict:
            user = users_dict.get(key)
            list.append(user)
        for a in list:
            if a.get_email() == form.email.data:
                email = a.get_email()


        msg = Message()
        msg.subject = "RentCycle Password Reset"
        msg.recipients = [form.email.data]
        msg.body = 'Your password reset link is http://127.0.0.1:5000/reset_password/{email}'.format(email=email)
        msg.sender = "chloefaith2612@gmail.com"
        mail.send(msg)
        message = "Email sent successfully"

        session['email_sent'] =  'Reset request was sent to your email. Please kindly check.'

    return render_template('reset_request.html', form=form)

@app.route("/reset_password/<string:email>/", methods=['GET', 'POST'])
def reset_password(email):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']
        list = []
        user = users_dict.get(email)
        list.append(user)
        user.set_password(form.password.data)
        user.set_password_confirm(form.password_confirm.data)
        db['Users'] = users_dict
        db.close()
        return redirect(url_for('home_reset'))

    return render_template('reset_password.html', form=form)

@app.route('/home_reset')
def home_reset():
    session['password_reset'] =  'Your password is changed. Please login again.'
    return render_template('home.html')

def checkUser(email, password):
    print("*** check user**", email,password)
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    list = []
    for key in users_dict:
        user = users_dict.get(key)
        print("data from shelve , user data", user.get_email(), user.get_password())
        list.append(user)

    for a in list:
        print("---list ---", a.get_email(), a.get_password())
        if a.get_email() == email:
            if a.get_password() == password:
                print('Registered')
                message = '1'
                break
            else:
                print('Wrong Password.')
                message = '3'
                break
        else:
            print("not registered",a.get_password(), password)
            print("not registered",a.get_email(), email)

            print('You are not registered.')
            message = '2'


    return message

@app.route('/deleteUser/<email>', methods=['POST'])
def delete_user(email):
    users_dict = {}

    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    user = users_dict.pop(email)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))

# ADMIN SIDE
@app.route('/createReward', methods=['GET', 'POST'])
def create_reward():
    create_reward_form = CreateRewardForm(request.form)
    if request.method == 'POST' and create_reward_form.validate():
        rewards_dict = {}
        db = shelve.open('reward.db', 'c')

        try:
            rewards_dict = db['Rewards']
            rewards_count = len(rewards_dict)
            rand1 = random.randint(1, 999999)
            rand2 = random.randint(1, 999999)
            id = rand1 + rand2
            reward_id = rewards_count + id
        except:
            print("Error in retrieving Rewards from reward.db.")
            rewards_count = 0
            reward_id = random.randint(1, 999999)

        reward = Reward.Reward(reward_id, create_reward_form.reward_name.data, create_reward_form.discount.data, create_reward_form.points_required.data,
                               create_reward_form.reward_expiry.data, create_reward_form.remarks.data)
        rewards_dict[reward.get_reward_id()] = reward
        db['Rewards'] = rewards_dict

        db.close()

        session['reward_created'] = reward.get_name()

        return redirect(url_for('retrieve_rewards'))
    return render_template('createReward.html', form=create_reward_form)

@app.route('/retrieveRewards')
def retrieve_rewards():
    rewards_dict = {}
    db = shelve.open('reward.db', 'r')
    rewards_dict = db['Rewards']
    db.close()

    rewards_list = []
    for key in rewards_dict:
        reward = rewards_dict.get(key)
        rewards_list.append(reward)

    return render_template('retrieveRewards.html', count=len(rewards_list), rewards_list=rewards_list)

@app.route('/updateReward/<int:id>/', methods=['GET', 'POST'])
def update_reward(id):
    update_reward_form = CreateRewardForm(request.form)
    if request.method == 'POST' and update_reward_form.validate():
        rewards_dict = {}
        db = shelve.open('reward.db', 'w')
        rewards_dict = db['Rewards']

        reward = rewards_dict.get(id)
        reward.set_name(update_reward_form.reward_name.data)
        reward.set_discount(update_reward_form.discount.data)
        reward.set_points_required(update_reward_form.points_required.data)
        reward.set_reward_expiry(update_reward_form.reward_expiry.data)
        reward.set_remarks(update_reward_form.remarks.data)

        db['Rewards'] = rewards_dict
        db.close()

        session['reward_updated'] = reward.get_name()

        return redirect(url_for('retrieve_rewards'))
    else:
        rewards_dict = {}
        db = shelve.open('reward.db', 'r')
        rewards_dict = db['Rewards']
        db.close()

        reward = rewards_dict.get(id)
        update_reward_form.reward_name.data = reward.get_name()
        update_reward_form.discount.data = reward.get_discount()
        update_reward_form.points_required.data = reward.get_points_required()
        update_reward_form.reward_expiry.data = reward.get_reward_expiry()
        update_reward_form.remarks.data = reward.get_remarks()

        session['reward_updated'] = reward.get_name()

        return render_template('updateReward.html', form=update_reward_form)


@app.route('/deleteReward/<int:id>', methods=['POST'])
def delete_reward(id):
    rewards_dict = {}

    db = shelve.open('reward.db', 'w')
    rewards_dict = db['Rewards']

    reward = rewards_dict.pop(id)

    db['Rewards'] = rewards_dict
    db.close()

    session['reward_deleted'] = reward.get_name()

    return redirect(url_for('retrieve_rewards'))


#CUSTOMER SIDE
@app.route('/customer_home')
def customer_home():
    return render_template('homeCustomer.html')

@app.route('/redeemRewards/', methods=['GET', 'POST'])
def redeem_rewards():
    print("opening success test")
    users_dict = {}
    db = shelve.open("user.db", "w")
    users_dict = db["Users"]

    total_points = 0

    for key in users_dict:
        user = users_dict.get(key)
        stored_email = user.get_email()
        if "email" in session:
            email = session["email"]
            if stored_email == email:
                points = user.get_points()
                print("this is the user's points:", points)
                total_points += points
            else:
                points = 0
                total_points += points
        else:
            return render_template('redeemRewards.html')

    print(total_points)
    db["Users"] = users_dict
    db.close()

    reward_db = shelve.open('reward.db', 'r')
    rewards_dict = reward_db['Rewards']
    reward_db.close()

    rewards_list = []
    for key in rewards_dict:
        reward = rewards_dict.get(key)
        rewards_list.append(reward)

    redemptions_dict = {}
    redemption_db = shelve.open('redeem.db', 'c')

    try:
        redemptions_dict = redemption_db["Redemptions"]
        redemption_db.close()

        redemptions_list = []
        for key in redemptions_dict:
            past_rewards = redemptions_dict.get(key)
            redemptions_list.append(past_rewards)
    except KeyError:
        redemptions_list = []

    print("this is the redemptions", redemptions_dict)
    print("this is the rewards", rewards_dict)


    return render_template('redeemRewards.html', reward_count=len(rewards_list), rewards_list=rewards_list,
                           total_points=total_points, redemptions_list=redemptions_list)

@app.route("/updateCustomerReward/<int:id>/", methods=["GET", "POST"])
def update_customer_reward(id):
    print("update customer reward")
    users_dict = {}
    db = shelve.open("user.db", "w")
    users_dict = db["Users"]

    rewards_dict = {}
    reward_db = shelve.open("reward.db", "w")
    rewards_dict = reward_db["Rewards"]
    reward_db.close()

    redemptions_dict = {}
    redemption_db = shelve.open('redeem.db', 'c')

    print("-- reward is --", id)
    reward = rewards_dict.get(id)
    require_points = reward.get_points_required()
    print("*** required points ***", require_points)

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
        print("this is the user's points:", user.get_points())

    total_points = 0
    for user in users_list:
        stored_email = user.get_email()
        if "email" in session:
            email = session["email"]
            if stored_email == email:
                print("---customer points---", user.get_points())
                if user.get_points() < require_points:
                    print("Error! Not enough points?")
                    flash("Error! Not enough points.", "warning")
                    total_points = user.get_points()
                else:
                    print("---customer points---", user.get_points())
                    user.update_points(require_points)
                    print("---new customer points---", user.get_points())
                    total_points = user.get_points()
                    user.set_points(total_points)

                    try:
                        redemptions_dict = redemption_db["Redemptions"]

                        redeem_count = random.randint(1, 999999)
                        print("previous redemptions dict", redemptions_dict)

                        reward.set_reward_id(redeem_count)

                        redemptions_dict[reward.get_reward_id()] = reward
                        redemption_db["Redemptions"] = redemptions_dict
                        print("current redemptions dict", redemptions_dict)

                        redemption_db.close()

                    except KeyError:
                        redeem_count = random.randint(1, 999999)
                        print("previous redemptions dict", redemptions_dict)

                        reward.set_reward_id(redeem_count)

                        redemptions_dict[reward.get_reward_id()] = reward
                        redemption_db["Redemptions"] = redemptions_dict
                        print("current redemptions dict", redemptions_dict)

                        redemption_db.close()

        else:
            return redirect(url_for('page_not_found'))

    db["Users"] = users_dict
    db.close()

    rewards_dict = {}
    reward_db = shelve.open('reward.db', 'r')
    rewards_dict = reward_db['Rewards']
    reward_db.close()

    rewards_list = []
    for key in rewards_dict:
        reward = rewards_dict.get(key)
        rewards_list.append(reward)

    redemptions_dict = {}
    redemption_db = shelve.open('redeem.db', 'r')
    redemptions_dict = redemption_db["Redemptions"]
    redemption_db.close()
    print(redemptions_dict)

    redemptions_list = []
    for key in redemptions_dict:
        past_rewards = redemptions_dict.get(key)
        redemptions_list.append(past_rewards)

    return render_template('redeemRewards.html', count=len(rewards_list), rewards_list=rewards_list, total_points=total_points, redemptions_list=redemptions_list)


# RENTAL INFORMATION
@app.route('/createRental/', methods=['GET', 'POST'])
def create_rental():
    create_rental_form = CreateRentalForm(request.form)
    if request.method == 'POST' and create_rental_form.validate():

        # For the confirmation email
        msg = Message('Hi there!', sender='RentCycle_admin@gmail.com', recipients=[create_rental_form.email.data])
        msg.body = 'Thank you for visiting RentCycle. This is an email to confirm that your rental was successful.'
        mail.send(msg)

        rental_dict = {}
        rental_db = shelve.open('rental.db', 'c')

        users_dict = {}
        db = shelve.open("user.db", "w")
        users_dict = db["Users"]

        try:
            rental_dict = rental_db['Rental']
        except:
            print("Error in retrieving Rental from rental.db.")

        rental_list = []
        for key in rental_dict:
            rental = rental_dict.get(key)
            rental_list.append(rental)

        rental = None
        if len(rental_dict) == 0:
            rental = Rental.Rental(create_rental_form.full_name.data, create_rental_form.phone_no.data,
                                   create_rental_form.email.data, create_rental_form.date.data,
                                   create_rental_form.time_in.data, create_rental_form.time_out.data,
                                   create_rental_form.bicycle.data, create_rental_form.duration.data,
                                   len(rental_dict))
        elif len(rental_dict) > 0:
            last_object = rental_list[-1]
            rental = Rental.Rental(create_rental_form.full_name.data, create_rental_form.phone_no.data,
                                   create_rental_form.email.data, create_rental_form.date.data,
                                   create_rental_form.time_in.data, create_rental_form.time_out.data,
                                   create_rental_form.bicycle.data, create_rental_form.duration.data,
                                   last_object.get_customer_id())

        rental_dict[rental.get_customer_id()] = rental
        rental_db['Rental'] = rental_dict

        price = None
        if create_rental_form.bicycle.data == 'RB':
            price = create_rental_form.duration.data * 9
        elif create_rental_form.bicycle.data == 'MB':
            price = create_rental_form.duration.data * 10
        elif create_rental_form.bicycle.data == 'FB':
            price = create_rental_form.duration.data * 10
        elif create_rental_form.bicycle.data == 'HB':
            price = create_rental_form.duration.data * 11

        session['calculation'] = price
        session['bicycle'] = create_rental_form.bicycle.data
        session['date'] = create_rental_form.date.data

        rental_db.close()

        return redirect(url_for('redeem_rewards'))
    return render_template('createRental.html', form=create_rental_form)


@app.route('/payment/<int:id>/')
def payment(id):

    redemptions_dict = {}
    redemption_db = shelve.open('redeem.db', 'c')
    # to remove redeemed reward later

    if id == 1:
        discount = None
        session['discount'] = discount
        count = 0
    else:
        redemptions_dict = redemption_db["Redemptions"]
        redeemed_reward = redemptions_dict.get(id)

        discount_value = redeemed_reward.get_discount()
        discount = discount_value / 100

        session['discount'] = discount
        session['redeem_id'] = id

        count = 1

# the session no need care yet
    price = session.get('calculation')
    discount = session.get('discount')
    bicycle = session.get('bicycle')
    date = session.get('date')


    return render_template('payment.html', price=price, count=count, discount=discount, bicycle=bicycle, date=date)

@app.route('/rentalConfirm')
def rental_confirm():
    users_dict = {}
    db = shelve.open("user.db", "w")
    users_dict = db["Users"]

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    # after payment is successful, user gets point
    total_points = 0
    for user in users_list:
        stored_email = user.get_email()
        if "email" in session:
            email = session["email"]
            if stored_email == email:
                for key in users_dict:
                    user = users_dict.get(key)
                    if user.get_email() == session["email"]:
                        total_points = user.get_points() + 100
                        print(total_points)
                        user.set_points(total_points)
                    else:
                        user.set_points(0)

    db["Users"] = users_dict
    db.close()

    # to remove redeemed reward
    redemptions_dict = {}
    redemption_db = shelve.open('redeem.db', 'w')
    try:
        redemptions_dict = redemption_db['Redemptions']

        redeem_id = session.get('redeem_id')
        redeemed_reward = redemptions_dict.get(redeem_id)

        redemptions_dict.pop(redeem_id)

        redemption_db['Redemptions'] = redemptions_dict
        redemption_db.close()
    except:
        redemption_db['Redemptions'] = redemptions_dict
        redemption_db.close()

    return render_template('rentalConfirm.html')

@app.route('/retrieveRental')
def retrieve_rental():
    rental_dict = {}
    rental_db = shelve.open('rental.db', 'r')
    rental_dict = rental_db['Rental']
    rental_db.close()

    rental_list = []
    for key in rental_dict:
        rental = rental_dict.get(key)
        rental_list.append(rental)

    return render_template('retrieveRental.html', count=len(rental_list), rental_list=rental_list)

@app.route('/updateRental/<int:id>/', methods=['GET', 'POST'])
def update_rental(id):
    update_rental_form = CreateRentalForm(request.form)
    if request.method == 'POST' and update_rental_form.validate():
        rental_dict = {}
        rental_db = shelve.open('rental.db', 'w')
        rental_dict = rental_db['Rental']

        rental = rental_dict.get(id)
        rental.set_full_name(update_rental_form.full_name.data)
        rental.set_phone_no(update_rental_form.phone_no.data)
        rental.set_email(update_rental_form.email.data)
        rental.set_date(update_rental_form.date.data)
        rental.set_time_in(update_rental_form.time_in.data)
        rental.set_time_out(update_rental_form.time_out.data)
        rental.set_bicycle(update_rental_form.bicycle.data)
        rental.set_duration(update_rental_form.duration.data)

        rental_db['Rental'] = rental_dict
        rental_db.close()

        session['rental_updated'] = rental.get_full_name()

        return redirect(url_for('retrieve_rental'))
    else:
        rental_dict = {}
        rental_db = shelve.open('rental.db', 'r')
        rental_dict = rental_db['Rental']
        rental_db.close()

        rental = rental_dict.get(id)
        update_rental_form.full_name.data = rental.get_full_name()
        update_rental_form.phone_no.data = rental.get_phone_no()
        update_rental_form.email.data = rental.get_email()
        update_rental_form.date.data = rental.get_date()
        update_rental_form.time_in.data = rental.get_time_in()
        update_rental_form.time_out.data = rental.get_time_out()
        update_rental_form.bicycle.data = rental.get_bicycle()
        update_rental_form.duration.data = rental.get_duration()

        return render_template('updateRental.html', form=update_rental_form)

@app.route('/deleteRental/<int:id>', methods=['POST'])
def delete_rental(id):
    rental_dict = {}
    rental_db = shelve.open('rental.db', 'w')
    rental_dict = rental_db['Rental']

    rental = rental_dict.pop(id)

    rental_db['Rental'] = rental_dict
    rental_db.close()

    session['rental_deleted'] = rental.get_full_name()

    return redirect(url_for('retrieve_rental'))


@app.route('/pieChart')
def pie_chart():
    rental_dict = {}
    rental_db = shelve.open('rental.db', 'r')
    rental_dict = rental_db['Rental']
    rental_db.close()

    rb_list = []
    mb_list = []
    fb_list = []
    hb_list = []

    for key in rental_dict:
        rental = rental_dict.get(key)
        if rental.get_bicycle() == 'RB':
            rb_list.append(rental)
        elif rental.get_bicycle() == 'MB':
            mb_list.append(rental)
        elif rental.get_bicycle() == 'FB':
            fb_list.append(rental)
        elif rental.get_bicycle() == 'HB':
            hb_list.append(rental)

    labels = ['Road Bike', 'Mountain Bike', 'Foldable Bike', 'Hybrid Bike']

    values = [len(rb_list), len(mb_list), len(fb_list), len(hb_list)]

    colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA"]

    pie_labels = labels
    pie_values = values
    return render_template('pieChart.html', title='Bicycle Type Popularity', max=100, set=zip(values, labels, colors))



@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Products from product.db.")

        product = Product.Product(create_product_form.product_name.data, create_product_form.file.data, create_product_form.product_price.data, create_product_form.product_status.data, create_product_form.product_amount.data, create_product_form.product_description.data)
        products_dict[product.get_product_id()] = product
        db['Products'] = products_dict

        db.close()

        session['product_created'] = product.get_product_name()

        return redirect(url_for('retrieve_products'))
    return render_template('createProduct.html', form=create_product_form)


@app.route('/retrieveProducts')
def retrieve_products():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('retrieveProducts.html', count=len(products_list), products_list=products_list)

#Trying to get product amount to decrease after an order

# def get_orders(product_id, product_amount):
#     with transaction.atomic():
#         products_list.filter(id=product_id).update(product_amount=F('quantity') - 1)
#         if products_list.get(id=product_id).product_amount < 0:
#             raise ValueError("Capacity exceeded: %s bikes left." % product_amount)


@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        product.set_file(update_product_form.file.data)
        product.set_product_name(update_product_form.product_name.data)
        product.set_product_price(update_product_form.product_price.data)
        product.set_product_status(update_product_form.product_status.data)
        product.set_product_amount(update_product_form.product_amount.data)
        product.set_product_description(update_product_form.product_description.data)

        db['Products'] = products_dict
        db.close()

        session['product_updated'] = product.get_product_name()

        return redirect(url_for('retrieve_products'))
    else:

        products_dict = {}
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)
        update_product_form.file.data = product.get_file
        update_product_form.product_name.data = product.get_product_name()
        update_product_form.product_price.data = product.get_product_price()
        update_product_form.product_status.data = product.get_product_status()
        update_product_form.product_amount.data = product.get_product_amount()
        update_product_form.product_description.data = product.get_product_description()

        return render_template('updateProduct.html', form=update_product_form)

@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_products'))


# FIRST TRY FOR VIEW PRODUCTS********************************************************
# @app.route('/viewProducts')
# def view():
#     return render_template('admin_viewProducts.html')

@app.route('/admin_viewProducts', methods=['GET', 'POST'])
# def products():
#     products_dict = {}
#     db = shelve.open('Products', 'c')
#     try:
#         if 'Product' in db:
#             products_dict = db['Product']
#         else:
#             db['Product'] = products_dict
#     except:
#         print("Error in retrieving Products from storage.")
#     db.close()
#
#     products_list = []
#     for key in products_dict:
#         product = products_dict.get(key)
#         products_list.append(product)
#*****************************************************************nbelow was tje one used
def adminview_products():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    form = SortProductForm(request.form)
    if request.method == "POST" and form.validate():
        if form.sort.data == "Price":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_product_price())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_product_price(), reverse=True)
        elif form.sort.data == "Quantity":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_product_amount())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_product_amount(), reverse=True)

    return render_template('admin_viewProducts.html', count=len(products_list), products_list=products_list, form=form)

@app.route('/customer_viewProducts', methods=['GET', 'POST'])
def customerview_products():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    form = SortProductForm(request.form)
    if request.method == "POST" and form.validate():
        if form.sort.data == "Price":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_product_price())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_product_price(), reverse=True)
        elif form.sort.data == "Quantity":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_product_amount())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_product_amount(), reverse=True)

    return render_template('customer_viewProducts.html', count=len(products_list), products_list=products_list, form=form)

@app.route('/login_viewProducts', methods=['GET', 'POST'])
def loginview_products():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    form = SortProductForm(request.form)
    if request.method == "POST" and form.validate():
        if form.sort.data == "Price":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_product_price())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_product_price(), reverse=True)
        elif form.sort.data == "Quantity":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_product_amount())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_product_amount(), reverse=True)

    return render_template('login_viewProducts.html', count=len(products_list), products_list=products_list, form=form)


@app.route('/createBikes', methods=['GET', 'POST'])
def create_bicycles():
    create_bike_entry = CreateBikes(request.form)
    if request.method == 'POST' and create_bike_entry.validate():
        bikes_dict = {}
        db = shelve.open('bikes.db', 'c')

        try:
            bikes_dict = db['Bicycle Entries']
            object_count = len(bikes_dict)
            object_id = object_count + 1
        except:
            object_id = 1
            print("Error in retrieving bicycle entries from bicycle.db.")

        bike = bikes.bikes(object_id, create_bike_entry.Bike_ID.data, create_bike_entry.date.data, create_bike_entry.damage.data, create_bike_entry.payment.data)
        bikes_dict[bike.get_Bike_ID()] = bike
        db['Bicycle Entries'] = bikes_dict

        bicycle_dict = db['Bicycle Entries']
        bike = bicycle_dict[bike.get_Bike_ID()]
        print(bike.get_Bike_ID(), "was stored in bikes.db successfully with Bike_ID ==", bike.get_Bike_ID())

        db.close()

        return redirect(url_for('retrieve_bikes'))
    return render_template('createBikes.html', form=create_bike_entry)


@app.route('/retrieveBikes')
def retrieve_bikes():
    bikes_dict = {}
    db = shelve.open('bikes.db', 'r')
    bikes_dict = db['Bicycle Entries']
    db.close()

    bikes_list = []
    for key in bikes_dict:
        bikes = bikes_dict.get(key)
        bikes_list.append(bikes)

    return render_template('retrieveBikes.html', count=len(bikes_list), bikes_list=bikes_list)


@app.route('/updateBikes/<id>/', methods=['GET', 'POST'])
def update_bike(id):
    update_bike_entry = CreateBikes(request.form)
    if request.method == 'POST':
        db = shelve.open('Bikes.db', 'w')
        bikes_dict = db['Bicycle Entries']

        bikes= bikes_dict.get(id)
        bikes.set_Bike_ID(update_bike_entry.Bike_ID.data)
        bikes.set_date(update_bike_entry.date.data)
        bikes.set_damage(update_bike_entry.damage.data)
        bikes.set_payment(update_bike_entry.payment.data)
        db['Bicycle Entries'] = bikes_dict
        db.close()
        return redirect(url_for('retrieve_bikes'))
    else:
        bikes_dict = {}
        db = shelve.open('bikes.db', 'w')
        bikes_dict = db['Bicycle Entries']
        db.close()
        bikes = bikes_dict.get(id)
        update_bike_entry.Bike_ID.data = bikes.get_Bike_ID()
        update_bike_entry.date.data = bikes.get_date()
        update_bike_entry.damage.data = bikes.get_damage()
        update_bike_entry.payment.data = bikes.get_payment()
        return render_template('updateBikes.html', form=update_bike_entry)


@app.route('/deleteBikes/<id>', methods=['POST'])
def delete_bike(id):
    bikes_dict = {}
    db = shelve.open('bikes.db', 'w')
    bikes_dict = db['Bicycle Entries']

    bikes_dict.pop(id)

    db['Bicycle Entries'] = bikes_dict
    db.close()
    return redirect(url_for('retrieve_bikes'))

@app.route('/createFeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback_entry = CreateFeedback(request.form)
    if request.method == 'POST' and create_feedback_entry.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db['Feedback Entries']
            object_count = len(feedback_dict)
            object_id = object_count + 1
        except:
            object_id = 1
            print("Error in retrieving feedback entries from feedback.db.")


        feedback_object = feedback.feedback(object_id, create_feedback_entry.First_Name.data, create_feedback_entry.Last_Name.data, create_feedback_entry.Email.data, create_feedback_entry.Phone_Number.data, create_feedback_entry.Feedback.data)
        feedback_dict[feedback_object.get_Feed()] = feedback_object
        db['Feedback Entries'] = feedback_dict

        feedback_dict = db['Feedback Entries']
        feedback_object = feedback_dict[feedback_object.get_Feed()]
        print(feedback_object.get_First_Name(), "was stored in feedback.db successfully with Name of", feedback_object.get_First_Name())

        db.close()

        return redirect(url_for('home'))
    return render_template('createFeedback.html', form=create_feedback_entry)

@app.route('/createFeedback_login', methods=['GET', 'POST'])
def create_feedback_login():
    create_feedback_entry = CreateFeedback(request.form)
    if request.method == 'POST' and create_feedback_entry.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db['Feedback Entries']
            object_count = len(feedback_dict)
            object_id = object_count + 1
        except:
            object_id = 1
            print("Error in retrieving feedback entries from feedback.db.")


        feedback_object = feedback.feedback(object_id, create_feedback_entry.First_Name.data, create_feedback_entry.Last_Name.data, create_feedback_entry.Email.data, create_feedback_entry.Phone_Number.data, create_feedback_entry.Feedback.data)
        feedback_dict[feedback_object.get_Feed()] = feedback_object
        db['Feedback Entries'] = feedback_dict

        feedback_dict = db['Feedback Entries']
        feedback_object = feedback_dict[feedback_object.get_Feed()]
        print(feedback_object.get_First_Name(), "was stored in feedback.db successfully with Name of", feedback_object.get_First_Name())

        db.close()

        return redirect(url_for('logout'))
    return render_template('createFeedback_login.html', form=create_feedback_entry)

@app.route('/retrieveFeedback')
def retrieve_feedback():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedback_dict = db['Feedback Entries']
    db.close()

    feedback_list = []
    for key in feedback_dict:
        feed = feedback_dict.get(key)
        feedback_list.append(feed)

    return render_template('retrieveFeedback.html', count=len(feedback_list), feedback_list=feedback_list)

@app.route('/deleteFeedback/<name>', methods=['POST'])
def delete_feedback(name):
    feedback_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedback_dict = db['Feedback Entries']

    feedback_dict.pop(name)

    db['Feedback Entries'] = feedback_dict
    db.close()
    return redirect(url_for('retrieve_feedback'))

@app.errorhandler(404)
def page_not_found():
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

    #debug=True so there's no need to keep restarting init, just refresh the webpage itself.




