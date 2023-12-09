from flask import Flask, render_template, flash, request, redirect, url_for, session 

app = Flask(__name__)

categories = ['Admin login', 'Reserve a set']
app.secret_key = 'infotec'

# admin usernames and passwords
users = {
    'admin1': {'password': '12345'},
    'admin2': {'password': '24680'},
    'admin3': {'password': '98765'},

}

# this will check to see if the passwords and usernames are valid
def admin_check(username, password):
    user = users.get(username)
    if user and user['password'] == password:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method== 'POST':
        category = request.form['category']
        if category == 'Admin login':
            return redirect(url_for('admin'))
        elif category == 'Reserve a set':
            return redirect(url_for('reservation'))
        
    return render_template('index.html', catagories=categories)

# admin endpoint
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    username = None  
    indexed_seating_chart = [['O' for _ in range(4)] for _ in range(12)] 

    if request.method == 'POST':
        username_input = request.form.get('username')
        password = request.form.get('password')

        if admin_check(username_input, password):
            flash('Login successful!', 'success')  
            username = username_input 
#get the positions from the txt file. Read them as columns 
            with open('reservations.txt', 'r') as seat:
                for line in seat: 
                    parts = line.strip().split(',')
                    if len(parts)== 4:
                        row, col= map(int, (parts[1],parts[2]))
                        indexed_seating_chart[row][col] = 'X'


        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('admin.html', username=username, indexed_seating_chart=indexed_seating_chart)

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        row = request.form['row']
        column = request.form['column']

        reservation_info = f'{first_name}, {row}, {column}, {last_name}\n'

        with open('reservations.txt', 'a') as seat:
            seat.write(reservation_info)

        flash('Reservation was made', 'success')
      #  return redirect(url_for('reservation'))

    return render_template('reservations.html')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

