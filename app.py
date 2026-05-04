from flask import Flask, render_template, redirect, url_for, request, jsonify
from abc import ABC, abstractmethod
from datetime import datetime

_discount_transaction_history = []


def load_discount_history():
    global _discount_transaction_history
    return _discount_transaction_history

def save_discount_transaction(transaction_data):
    global _discount_transaction_history
    
    transaction_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_data['date'] = datetime.now().strftime('%Y-%m-%d')
    transaction_data['time'] = datetime.now().strftime('%H:%M:%S')
    
    _discount_transaction_history.append(transaction_data)
    
    return True

def get_discount_history():
    return load_discount_history()

def get_discount_summary():
    global _discount_transaction_history
    
    if not _discount_transaction_history:
        return {
            'total_transactions': 0,
            'total_saved': 0,
            'avg_discount': 0
        }
    
    total_saved = sum(t.get('saved_amount', 0) for t in _discount_transaction_history)
    total_discount_percent = sum(t.get('discount_percentage', 0) for t in _discount_transaction_history)
    
    return {
        'total_transactions': len(_discount_transaction_history),
        'total_saved': total_saved,
        'avg_discount': total_discount_percent / len(_discount_transaction_history) if _discount_transaction_history else 0
    }

class DiscountCreationHistoryManager:  
    def __init__(self):
        self._history = []
    
    def log_discount_action(self, action, product_id, discount_percent, start_date, end_date, admin_email):
        entry = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'action': action,
            'product_id': product_id,
            'discount_percent': discount_percent,
            'start_date': start_date,
            'end_date': end_date,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'admin': admin_email
        }
        
        self._history.append(entry)
        return True
    
    def get_all_history(self):
        return list(reversed(self._history))
    
    def get_history_by_product(self, product_id):
        return [h for h in self._history if h['product_id'] == product_id]
    
    def get_history_by_action(self, action):
        return [h for h in self._history if h['action'] == action]
    
    def get_summary(self):
        if not self._history:
            return {
                'total_actions': 0,
                'total_created': 0,
                'total_updated': 0,
                'total_removed': 0,
                'unique_products': 0
            }
        
        total_created = len([h for h in self._history if h['action'] == 'created'])
        total_updated = len([h for h in self._history if h['action'] == 'updated'])
        total_removed = len([h for h in self._history if h['action'] == 'removed'])
        unique_products = len(set(h['product_id'] for h in self._history))
        
        return {
            'total_actions': len(self._history),
            'total_created': total_created,
            'total_updated': total_updated,
            'total_removed': total_removed,
            'unique_products': unique_products
        }
    
    def clear_history(self):
        self._history = []
        return True
    
class User(ABC):
    def __init__(self, email, password, role):
        self._email = email
        self._password = password
        self._role = role
        self._is_authenticated = False
    
    def get_email(self):
        return self._email
    
    def get_role(self):
        return self._role
    
    def is_authenticated(self):
        return self._is_authenticated
    
    def set_email(self, email):
        if '@' in email and '.' in email:
            self._email = email
            return True
        return False
    
    def set_password(self, password):
        if len(password) >= 3:
            self._password = password
            return True
        return False
    
    def authenticate(self, password):
        if self._password == password:
            self._is_authenticated = True
            return True
        return False
    
    def logout(self):
        self._is_authenticated = False
    
    @abstractmethod
    def get_dashboard_template(self):
        pass
    
    @abstractmethod
    def get_allowed_sections(self):
        pass

class AdminUser(User):
    def __init__(self, email, password, role="admin"):
        super().__init__(email, password, role)
        self._admin_permissions = ['product_management', 'discount_management', 'user_management']
    
    def get_admin_permissions(self):
        return self._admin_permissions

    def set_admin_permissions(self, permissions):
        if isinstance(permissions, list):
            self._admin_permissions = permissions
            return True
        return False
    
    # ============= IMPLEMENTING ABSTRACT METHODS =============
    def get_dashboard_template(self):
        return 'admindashboard.html'
    
    def get_allowed_sections(self):
        return ['product-management', 'discount-management', 'settings', 'discount-history']
    
    def can_manage_products(self):
        return 'product_management' in self._admin_permissions
    
    def can_manage_discounts(self):
        return 'discount_management' in self._admin_permissions


class RegularUser(User):
    
    def __init__(self, email, password, role="user"):
        super().__init__(email, password, role)
        self._user_preferences = {
            'theme': 'light',
            'notifications': True
        }
    
    def get_user_preferences(self):
        return self._user_preferences
    
    def get_preference(self, key):
        return self._user_preferences.get(key, None)
    
    # ============= SETTERS =============
    def set_user_preferences(self, preferences):
        if isinstance(preferences, dict):
            self._user_preferences.update(preferences)
            return True
        return False
    
    def set_preference(self, key, value):
        self._user_preferences[key] = value
        return True
    
    # ============= IMPLEMENTING ABSTRACT METHODS =============
    def get_dashboard_template(self):
        return 'userdashboard.html'
    
    def get_allowed_sections(self):
        return ['pricing', 'discount', 'settings']

class UserManager:
    def __init__(self):
        self._users = {}
        self._current_user = None
        self._initialize_default_users()
    
    def _initialize_default_users(self):
        admin = AdminUser('gwapo@bisu.edu.ph', 'admin', 'admin')
        self._users[admin.get_email()] = admin
        
        user = RegularUser('pangit@bisu.edu.ph', 'user', 'user')
        self._users[user.get_email()] = user

    def get_user(self, email):
        return self._users.get(email, None)
    
    def get_current_user(self):
        return self._current_user
    
    def get_all_users(self):
        return self._users.copy()
    
    def is_user_exists(self, email):
        return email in self._users

    def add_user(self, user):
        if isinstance(user, User) and user.get_email() not in self._users:
            self._users[user.get_email()] = user
            return True
        return False
    
    def remove_user(self, email):
        if email in self._users:
            del self._users[email]
            return True
        return False

    def authenticate_user(self, email, password):
        user = self.get_user(email)
        if user and user.authenticate(password):
            self._current_user = user
            return True
        return False
    
    def logout_current_user(self):
        if self._current_user:
            self._current_user.logout()
            self._current_user = None
    
    def is_user_authenticated(self):
        return self._current_user is not None

class FlaskAppWrapper:
    def __init__(self, name):
        self._app = Flask(name)
        self._user_manager = UserManager()
        self._discount_creation_history = DiscountCreationHistoryManager()
        self._setup_routes()

    def get_flask_app(self):
        return self._app
    
    def get_user_manager(self):
        return self._user_manager
    
    def get_discount_creation_history(self):
        return self._discount_creation_history

    def _setup_routes(self):
        @self._app.route('/')
        def home():
            return '<meta charset="UTF-8"><h1>KINSA KA OOOIIIEEEEE ABOT MAN KA DIREEEEE &#128544;</h1>'
        
        @self._app.route('/admindashboard')
        def admindashboard():
            if self._user_manager.get_current_user():
                current_user = self._user_manager.get_current_user()
                if current_user.get_role() == 'admin':
                    return render_template(
                        current_user.get_dashboard_template(),
                        username='Admin',
                        permissions=current_user.get_admin_permissions()
                    )
            return redirect(url_for('login'))
        
        @self._app.route('/admindashboard/product-management')
        def adminproductmanagement():
            if self._user_manager.get_current_user():
                current_user = self._user_manager.get_current_user()
                if current_user.get_role() == 'admin' and current_user.can_manage_products():
                    return render_template(
                        'adminproductmanagement.html',
                        username='Admin'
                    )
            return redirect(url_for('login'))
        
        @self._app.route('/admindashboard/discount-management')
        def admindiscountmanagement():
            if self._user_manager.get_current_user():
                current_user = self._user_manager.get_current_user()
                if current_user.get_role() == 'admin' and current_user.can_manage_discounts():
                    return render_template(
                        'admindiscountmanagement.html',
                        username='Admin'
                    )
            return redirect(url_for('login'))
        
        @self._app.route('/admindashboard/settings')
        def adminsettings():
            if self._user_manager.get_current_user():
                current_user = self._user_manager.get_current_user()
                if current_user.get_role() == 'admin':
                    return render_template(
                        'adminsettings.html',
                        username='Admin',
                        role=current_user.get_role()
                    )
            return redirect(url_for('login'))
        
        @self._app.route('/admindashboard/discount-history')
        def discount_history():
            if self._user_manager.get_current_user():
                current_user = self._user_manager.get_current_user()
                if current_user.get_role() == 'admin':
                    history = get_discount_history()
                    summary = get_discount_summary()
                    history.reverse()
                    
                    creation_history = self._discount_creation_history.get_all_history()
                    creation_summary = self._discount_creation_history.get_summary()
                    
                    return render_template(
                        'discount_history.html',
                        username='Admin',
                        history=history,
                        total_saved=summary['total_saved'],
                        total_transactions=summary['total_transactions'],
                        avg_discount=summary['avg_discount'],
                        creation_history=creation_history,
                        summary=creation_summary
                    )
            return redirect(url_for('login'))
        
        # ============= API ROUTE PARA MAG-SAVE OG DISCOUNT CREATION =============
        @self._app.route('/api/save_discount_creation', methods=['POST'])
        def api_save_discount_creation():
            if not self._user_manager.get_current_user():
                return jsonify({'success': False, 'message': 'Not authenticated'}), 401
            
            data = request.get_json()
            
            required_fields = ['action', 'product_id', 'discount_percent', 'start_date', 'end_date']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400
            
            success = self._discount_creation_history.log_discount_action(
                action=data['action'],
                product_id=data['product_id'],
                discount_percent=data['discount_percent'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                admin_email=self._user_manager.get_current_user().get_email()
            )
            
            if success:
                return jsonify({'success': True, 'message': 'Discount creation logged successfully!'})
            else:
                return jsonify({'success': False, 'message': 'Failed to log discount creation'}), 500

        @self._app.route('/api/get_discount_creation_history', methods=['GET'])
        def api_get_discount_creation_history():
            if not self._user_manager.get_current_user():
                return jsonify({'success': False, 'message': 'Not authenticated'}), 401
            
            history = self._discount_creation_history.get_all_history()
            return jsonify({'success': True, 'history': history})

        @self._app.route('/api/get_discount_creation_summary', methods=['GET'])
        def api_get_discount_creation_summary():
            if not self._user_manager.get_current_user():
                return jsonify({'success': False, 'message': 'Not authenticated'}), 401
            
            summary = self._discount_creation_history.get_summary()
            return jsonify({'success': True, 'summary': summary})

        @self._app.route('/api/save_discount_transaction', methods=['POST'])
        def api_save_discount_transaction():
            if not self._user_manager.get_current_user():
                return jsonify({'success': False, 'message': 'Not authenticated'}), 401
            
            data = request.get_json()
            
            required_fields = ['transaction_id', 'original_amount', 'discounted_amount', 'saved_amount']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400
            
            transaction = {
                'transaction_id': data['transaction_id'],
                'customer_name': data.get('customer_name', 'Guest'),
                'discount_code': data.get('discount_code', 'N/A'),
                'discount_percentage': data.get('discount_percentage', 0),
                'original_amount': float(data['original_amount']),
                'discounted_amount': float(data['discounted_amount']),
                'saved_amount': float(data['saved_amount']),
                'user': self._user_manager.get_current_user().get_email()
            }
            
            if save_discount_transaction(transaction):
                return jsonify({'success': True, 'message': 'Transaction saved successfully!'})
            else:
                return jsonify({'success': False, 'message': 'Failed to save transaction'}), 500

        @self._app.route('/api/clear_discount_history', methods=['POST'])
        def api_clear_discount_history():
            if not self._user_manager.get_current_user():
                return jsonify({'success': False, 'message': 'Not authenticated'}), 401
            
            current_user = self._user_manager.get_current_user()
            if current_user.get_role() != 'admin':
                return jsonify({'success': False, 'message': 'Admin only'}), 403
            
            global _discount_transaction_history
            _discount_transaction_history = []
            self._discount_creation_history.clear_history()
            
            return jsonify({'success': True, 'message': 'All history cleared!'})
        
        @self._app.route('/userdashboard')
        def userdashboard():
            if self._user_manager.get_current_user():
                current_user = self._user_manager.get_current_user()
                if current_user.get_role() == 'user':
                    return render_template(
                        current_user.get_dashboard_template(),
                        username='User',
                        role=current_user.get_role(),
                        preferences=current_user.get_user_preferences()
                    )
            return redirect(url_for('login'))
        
        @self._app.route('/userdashboard/<section>')
        def userdashboard_section(section):
            if self._user_manager.get_current_user():
                current_user = self._user_manager.get_current_user()
                if current_user.get_role() == 'user':
                    allowed_sections = current_user.get_allowed_sections()
                    if section in allowed_sections:
                        template_map = {
                            'pricing': 'pricingdashboard.html',
                            'discount': 'discountdashboard.html',
                            'settings': 'settingsdashboard.html'
                        }
                        return render_template(
                            template_map.get(section, 'userdashboard.html'),
                            username='User',
                            role='user'
                        )
            return redirect(url_for('login'))
        
        @self._app.route('/logout')
        def logout():
            self._user_manager.logout_current_user()
            return redirect(url_for('login'))
        
        @self._app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username', '')
                password = request.form.get('password', '')
                
                if self._user_manager.authenticate_user(username, password):
                    current_user = self._user_manager.get_current_user()
                    if current_user.get_role() == 'admin':
                        return render_template(
                            current_user.get_dashboard_template(),
                            message=username,
                            username=username
                        )
                    else:
                        return render_template(
                            current_user.get_dashboard_template(),
                            message=username,
                            username=username,
                            role=current_user.get_role()
                        )
                else:
                    return render_template('login.html', message='Invalid username or password')
            
            return render_template('login.html', message='')

    def run(self, debug=True):
        """Run the Flask application"""
        self._app.run(debug=debug)

    def get_wsgi_app(self):
        """Return WSGI application for Vercel deployment"""
        return self._app
    
flask_app_wrapper = FlaskAppWrapper(__name__)

application = flask_app_wrapper.get_wsgi_app()
app = application

if __name__ == '__main__':
    flask_app_wrapper.run(debug=True)