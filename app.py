
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

users = {
    'gwapo@bisu.edu.ph' : ['admin','admin'],
    'pangit@bisu.edu.ph' : ['user','user']
}

@app.route('/')
def home():
    return '<meta charset="UTF-8"><h1>KINSA KA OOOIIIEEEEE ABOT MAN KA DIREEEEE &#128544;</h1>'

@app.route('/admindashboard')
def admindashboard():
    return render_template('admindashboard.html', username='Admin')

@app.route('/admindashboard/product-management')
def adminproductmanagement():
    return render_template('adminproductmanagement.html', username='Admin')

@app.route('/admindashboard/discount-management')
def admindiscountmanagement():
    return render_template('admindiscountmanagement.html', username='Admin')

@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html', username='User', role='user')

@app.route('/userdashboard/<section>')
def userdashboard_section(section):
    if section == 'pricing':
        return render_template(
            'pricingdashboard.html',
            username='User',
            role='user'
        )
    elif section == 'discount':
        return render_template(
            'discountdashboard.html',
            username='User',
            role='user'
        )
    elif section == 'settings':
        return render_template(
            'settingsdashboard.html',
            username='User',
            role='user'
        )
    return render_template('userdashboard.html', username='User', role='user')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
               
        if username in users:           
            if users[username][0] == password:
                role = users[username][1]
                if role == 'admin':
                    return render_template(
                        'admindashboard.html',
                        message=username,
                        username=username
                    )
                else:
                    return render_template(
                        'userdashboard.html',
                        message=username,
                        username=username,
                        role=role
                    )
            else:              
                return render_template('login.html', message='Invalid username or password')
        
    return render_template('login.html', message='')


application = app


if __name__ == '__main__':
    app.run(debug=True)
