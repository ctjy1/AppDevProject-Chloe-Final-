from wtforms import Form, StringField, validators, ValidationError
from wtforms.fields import EmailField, PasswordField, TelField, IntegerField, DateField, TextAreaField, FileField, SelectField, TimeField, SubmitField
from wtforms.validators import NumberRange, DataRequired, Regexp, Email, InputRequired
import datetime, shelve

class CreateUserForm(Form):
    firstname = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastname = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone = TelField('Mobile Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.Length(min=6, message='Too short'), validators.EqualTo('password_confirm', message='Passwords must match'), validators.DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[validators.Length(min=6, message='Too short'), validators.DataRequired()])

    def validate_phone(form, field):
        if field.data.isdigit() and field.data.startswith('8') or field.data.isdigit() and field.data.startswith('9'):
            pass
        else:
            raise ValidationError("Please enter a valid phone number")

class UpdateUserForm(Form):
    firstname = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastname = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', render_kw={'readonly': True})
    phone = TelField('Mobile Number', [validators.Length(min=8, max=8), validators.DataRequired()])

    def validate_phone(form, field):
        if field.data.isdigit() and field.data.startswith('8') or field.data.isdigit() and field.data.startswith('9'):
            pass
        else:
            raise ValidationError("Please enter a valid phone number")

class LogInForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.Length(min=6, message='Too short'), validators.DataRequired()])

class ResetRequestForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])

class ResetPasswordForm(Form):
    password = PasswordField('Password', validators=[validators.Length(min=6, message='Too short'), validators.EqualTo('password_confirm', message='Passwords must match'), validators.DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[validators.Length(min=6, message='Too short'), validators.DataRequired()])

class CreateRewardForm(Form):
    reward_name = StringField('Reward Name', [validators.InputRequired("Please enter the reward name.")])
    discount = IntegerField('Discount Value', [validators.InputRequired("Please enter the reward discount.")])
    points_required = IntegerField('Points Required', [validators.InputRequired("Please enter required number of points.")])
    reward_expiry = DateField('Reward Expiry', [validators.InputRequired("Please enter a valid date of expiry.")], format="%Y-%m-%d")
    remarks = TextAreaField('Remarks', [validators.Optional()])

    def validate_reward_name(form, field):
        if len(field.data) > 50:
            raise ValidationError('Name must be less than 50 characters.')

    def validate_reward_expiry(form, field):
        print("***", field.data, type(field.data))
        input_data = str(field.data)
        print("Current Date", datetime.datetime.now())
        print("Current YMD:", datetime.date.today().strftime("%Y-%m-%d"))
        if input_data < datetime.date.today().strftime("%Y-%m-%d"):
            raise ValidationError("Date of Expiry cannot be earlier than current date.")

class CreateProductForm(Form):
    file = FileField('Product Image', [validators.Length(min=1, max = 150), validators.DataRequired()])
    product_name = StringField('Product Name', [validators.Length(min=1, max = 150), validators.DataRequired()])
    product_price = StringField('Product Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_status = SelectField('Product Status', [validators.DataRequired()], choices=[('', 'Select'), ('INS', 'In Stock'), ('OOS', 'Out of Stock')], default='')
    product_amount = StringField('Product Amount', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_description = TextAreaField('Product Description', [validators.Optional()])

    def validate_product_price(form, field):
        if not field.data.isdigit():
            raise ValidationError("Price must be in numbers")
    def validate_product_amount(form, field):
        if not field.data.isdigit():
            raise ValidationError("Amount must be in numbers")
    def validate_product_description(form, field):
        if field.data.isdigit():
            raise ValidationError("Description must be a string")

class CreateRentalForm(Form):
    full_name = StringField("Renter's Full Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_no = StringField('Phone Number', validators=[Regexp(regex="^(\\+\\d{2}( )?)?\\d{4}[- .]?\\d{4}$", message="Valid phone number format is +xx xxxx-xxxx / xxxx-xxxx"), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(message="Valid email format is email@address.com"), validators.DataRequired()])
    date = DateField('Rental Date', format='%Y-%m-%d', validators=[DataRequired()])
    time_in = TimeField('Estimated Time-In', format='%H:%M', validators=[DataRequired()])
    time_out = TimeField('Estimated Time-Out', format='%H:%M', validators=[DataRequired()])
    bicycle = SelectField('Bicycle', [validators.DataRequired()], choices=[('', 'Select'), ('RB', 'RoadBike ($9/hr)'), ('MB', 'MountainBike ($10/hr)'), ('FB', 'FoldableBike ($10/hr)'), ('HB', 'HybridBike ($11/hr)')], default='')
    duration = IntegerField('Total Duration (Hrs)', validators=[DataRequired(message="Rental Duration must not exceed 24 hours"), NumberRange(min=1, max=24)])

    def validate_date(form, field):
        input_date = str(field.data)
        today_date = datetime.date.today().strftime('%Y-%m-%d')
        if input_date < today_date:
            raise ValidationError("Rental date cannot be before today's date")

    def validate_time_out(form, field):
        if field.data < form.time_in.data:
            raise ValidationError("Time out must not be earlier than time in")

class CreateBikes(Form):
    Bike_ID = StringField('Bicycle ID', [validators.Length(min=1, max=5), validators.DataRequired()])
    date = DateField('Date Rented', format='%Y-%m-%d')
    damage = TextAreaField('Damage description', [validators.DataRequired()])
    payment = StringField('Penalty Amount', [validators.Length(min=1, max=4), validators.DataRequired()])

    def validate_Bike_ID(form, field): # Check for duplicates
            bikes_dict = {}
            db = shelve.open("bikes.db","r")
            bikes_dict = db['Bicycle Entries']
            db.close()

            if field.data in bikes_dict:
                message = field.data + "Bike ID already exists in system"
                raise ValidationError("Bike ID already exists in system")

    def validate_payment(form, field): # Ensure only numbers are allowed
            try:
                num = int(field.data)
            except ValueError:
                raise ValidationError("Only numbers are allowed.")

    def validate_date(form, field): # Checks if date selected is not in the future or before 1 Jan 2023
            print(field.data, type(field.data))
            s_date = str(field.data)
            check_date = "2023-01-01"
            today_date = datetime.date.today().strftime("%Y-%m-%d")
            if s_date > today_date:
                raise ValidationError("Date selected cannot be in the future")

            elif s_date < check_date:
                print("---s date is", s_date, "check_date", check_date)
                raise ValidationError("Date selected cannot be before website's creation")
            else:
                print("success")

class CreateProductForm(Form):
    file = FileField('Product Image', [validators.Length(min=1, max = 150), validators.DataRequired()])
    product_name = StringField('Product Name', [validators.Length(min=1, max = 150), validators.DataRequired()])
    product_price = StringField('Product Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_status = SelectField('Product Status', [validators.DataRequired()], choices=[('', 'Select'), ('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')], default='')
    product_amount = StringField('Product Amount', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_description = TextAreaField('Product Description', [validators.Optional()])

    def validate_product_price(form, field):
        if not field.data.isdigit():
            raise ValidationError("Price must be in numbers")
    def validate_product_amount(form, field):
        if not field.data.isdigit():
            raise ValidationError("Amount must be in numbers")
    def validate_product_description(form, field):
        if field.data.isdigit():
            raise ValidationError("Description must be a string")

class SortProductForm(Form):
    sort = SelectField('Filter By', validators=[DataRequired()],
                       choices=[('', 'Select'), ('product_price', 'Price'), ('product_amount', 'Quantity')])
    direction = SelectField('Sort By', validators=[DataRequired()],
                            choices=[('', 'Select'), ('Ascending', 'Ascending'), ('Descending', 'Descending')],
                            default='')
    submit = SubmitField('Update')

class CreateBikes(Form):
    Bike_ID = StringField('Bicycle ID', [validators.Length(min=1, max=5), validators.DataRequired()])
    date = DateField('Date Rented', format='%Y-%m-%d')
    damage = TextAreaField('Damage description', [validators.DataRequired()])
    payment = StringField('Penalty Amount', [validators.Length(min=1, max=4), validators.DataRequired()])

    def validate_Bike_ID(form, field): # Check for duplicates
            bikes_dict = {}
            db = shelve.open("bikes.db","r")
            bikes_dict = db['Bicycle Entries']
            db.close()

            if len(field.data) < 5:
                message = field.data + "Bike ID must have 5 digits"
                raise ValidationError("Bike ID must have 5 digits")

            if field.data in bikes_dict:
                message = field.data + "Bike ID already exists in system"
                raise ValidationError("Bike ID already exists in system")

            try:
                num = int(field.data)
            except ValueError:
                raise ValidationError("Only numbers are allowed.")

    def validate_payment(form, field): # Ensure only numbers are allowed
            try:
                num = int(field.data)
            except ValueError:
                raise ValidationError("Only numbers are allowed.")

    def validate_date(form, field): # Checks if date selected is not in the future or before 1 Jan 2023
            print(field.data, type(field.data))
            s_date = str(field.data)
            check_date = "2023-01-01"
            today_date = datetime.date.today().strftime("%Y-%m-%d")
            if s_date > today_date:
                raise ValidationError("Date selected cannot be in the future")

            elif s_date < check_date:
                print("---s date is", s_date, "check_date", check_date)
                raise ValidationError("Date selected cannot be before website's creation")
            else:
                print("success")


class CreateFeedback(Form):
    First_Name = StringField('First Name', [validators.DataRequired()])
    Last_Name = StringField('Last Name', [validators.DataRequired()])
    Email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    Phone_Number = StringField('Phone Number', [validators.Length(max=8), validators.DataRequired()])
    Feedback = TextAreaField('Feedback', [validators.DataRequired()])

    def validate_First_Name(form, field):
        excluded_chars = " *?!'^+%&/()=}][{$#_-<>"
        for char in field.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    def validate_Last_Name(form, field):
        excluded_chars = " *?!'^+%&/()=}][{$#_-<>"
        for char in field.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    def validate_Phone_Number(form, field):
        excluded_chars = " *?!'^%&/()=}][{$#_-<>"
        for char in field.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in contact number.")
