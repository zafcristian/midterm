from flask import Flask, render_template, redirect, url_for, request
from abc import ABC, abstractmethod

# ============= BASE CLASS WITH ABSTRACTION =============
class User(ABC):
    """Base abstract class for all users - demonstrates inheritance"""
    
    def __init__(self, email, password, role):
        """Constructor - initializes user attributes"""
        self._email = email          # Encapsulated (protected)
        self._password = password    # Encapsulated
        self._role = role            # Encapsulated
        self._is_authenticated = False
    
    # ============= GETTERS (Encapsulation) =============
    def get_email(self):
        """Getter for email"""
        return self._email
    
    def get_role(self):
        """Getter for role"""
        return self._role
    
    def is_authenticated(self):
        """Getter for authentication status"""
        return self._is_authenticated
    
    # ============= SETTERS (Encapsulation) =============
    def set_email(self, email):
        """Setter for email with validation"""
        if '@' in email and '.' in email:
            self._email = email
            return True
        return False
    
    def set_password(self, password):
        """Setter for password with validation"""
        if len(password) >= 3:  # Minimum length validation
            self._password = password
            return True
        return False
    
    # ============= BUSINESS METHODS =============
    def authenticate(self, password):
        """Method to authenticate user"""
        if self._password == password:
            self._is_authenticated = True
            return True
        return False
    
    def logout(self):
        """Method to logout user"""
        self._is_authenticated = False
    
    @abstractmethod
    def get_dashboard_template(self):
        """Abstract method - forces child classes to implement"""
        pass
    
    @abstractmethod
    def get_allowed_sections(self):
        """Abstract method for role-based sections"""
        pass


# ============= INHERITANCE: CHILD CLASS 1 =============
class AdminUser(User):
    """Admin user class - inherits from User"""
    
    def __init__(self, email, password, role="admin"):
        """Constructor calls parent constructor"""
        super().__init__(email, password, role)
        self._admin_permissions = ['product_management', 'discount_management', 'user_management']
    
    # ============= GETTERS =============
    def get_admin_permissions(self):
        """Get admin-specific permissions"""
        return self._admin_permissions
    
    # ============= SETTERS =============
    def set_admin_permissions(self, permissions):
        """Set admin permissions"""
        if isinstance(permissions, list):
            self._admin_permissions = permissions
            return True
        return False
    
    # ============= IMPLEMENTING ABSTRACT METHODS =============
    def get_dashboard_template(self):
        """Returns admin dashboard template"""
        return 'admindashboard.html'
    
    def get_allowed_sections(self):
        """Returns admin sections"""
        return ['product-management', 'discount-management', 'settings']
    
    # ============= ADMIN-SPECIFIC METHODS =============
    def can_manage_products(self):
        """Check if admin can manage products"""
        return 'product_management' in self._admin_permissions
    
    def can_manage_discounts(self):
        """Check if admin can manage discounts"""
        return 'discount_management' in self._admin_permissions


# ============= INHERITANCE: CHILD CLASS 2 =============
class RegularUser(User):
    """Regular user class - inherits from User"""
    
    def __init__(self, email, password, role="user"):
        """Constructor calls parent constructor"""
        super().__init__(email, password, role)
        self._user_preferences = {
            'theme': 'light',
            'notifications': True
        }
    
    # ============= GETTERS =============
    def get_user_preferences(self):
        """Get user preferences"""
        return self._user_preferences
    
    def get_preference(self, key):
        """Get specific preference"""
        return self._user_preferences.get(key, None)
    
    # ============= SETTERS =============
    def set_user_preferences(self, preferences):
        """Set user preferences"""
        if isinstance(preferences, dict):
            self._user_preferences.update(preferences)
            return True
        return False
    
    def set_preference(self, key, value):
        """Set specific preference"""
        self._user_preferences[key] = value
        return True
    
    # ============= IMPLEMENTING ABSTRACT METHODS =============
    def get_dashboard_template(self):
        """Returns user dashboard template"""
        return 'userdashboard.html'
    
    def get_allowed_sections(self):
        """Returns user sections"""
        return ['pricing', 'discount', 'settings']


# ============= USER MANAGEMENT CLASS =============
class UserManager:
    """Manages all users - demonstrates encapsulation and collection management"""
    
    def __init__(self):
        """Constructor initializes empty user storage"""
        self._users = {}  # Encapsulated dictionary
        self._current_user = None  # Track logged-in user
        self._initialize_default_users()
    
    def _initialize_default_users(self):
        """Private method to add default users"""
        # Create admin user using AdminUser class
        admin = AdminUser('gwapo@bisu.edu.ph', 'admin', 'admin')
        self._users[admin.get_email()] = admin
        
        # Create regular user using RegularUser class
        user = RegularUser('pangit@bisu.edu.ph', 'user', 'user')
        self._users[user.get_email()] = user
    
    # ============= GETTERS =============
    def get_user(self, email):
        """Get user by email"""
        return self._users.get(email, None)
    
    def get_current_user(self):
        """Get currently logged-in user"""
        return self._current_user
    
    def get_all_users(self):
        """Get all users (returns copy for encapsulation)"""
        return self._users.copy()
    
    def is_user_exists(self, email):
        """Check if user exists"""
        return email in self._users
    
    # ============= SETTERS =============
    def add_user(self, user):
        """Add new user"""
        if isinstance(user, User) and user.get_email() not in self._users:
            self._users[user.get_email()] = user
            return True
        return False
    
    def remove_user(self, email):
        """Remove user by email"""
        if email in self._users:
            del self._users[email]
            return True
        return False
    
    # ============= AUTHENTICATION METHODS =============
    def authenticate_user(self, email, password):
        """Authenticate user and set as current user"""
        user = self.get_user(email)
        if user and user.authenticate(password):
            self._current_user = user
            return True
        return False
    
    def logout_current_user(self):
        """Logout current user"""
        if self._current_user:
            self._current_user.logout()
            self._current_user = None
    
    def is_user_authenticated(self):
        """Check if any user is logged in"""
        return self._current_user is not None


# ============= FLASK APPLICATION CLASS =============
class FlaskAppWrapper:
    """Wrapper class for Flask application - demonstrates OOP with Flask"""
    
    def __init__(self, name):
        """Constructor initializes Flask app and user manager"""
        self._app = Flask(name)  # Encapsulated Flask app
        self._user_manager = UserManager()  # Encapsulated user manager
        self._setup_routes()  # Private method to setup routes
    
    # ============= GETTERS =============
    def get_flask_app(self):
        """Get the underlying Flask app"""
        return self._app
    
    def get_user_manager(self):
        """Get the user manager instance"""
        return self._user_manager
    
    # ============= ROUTE SETUP (Private Methods) =============
    def _setup_routes(self):
        """Private method to setup all routes"""
        
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
    
    # ============= RUN METHOD =============
    def run(self, debug=True):
        """Run the Flask application"""
        self._app.run(debug=debug)
    
    # ============= EXPOSE FOR VERCEL =============
    def get_wsgi_app(self):
        """Return WSGI application for Vercel deployment"""
        return self._app


# ============= MAIN APPLICATION INSTANCE =============
# Create the Flask app wrapper instance
flask_app_wrapper = FlaskAppWrapper(__name__)

# For Vercel deployment - expose the WSGI app
application = flask_app_wrapper.get_wsgi_app()
app = application  # Also expose as 'app' for compatibility

# ============= RUN THE APPLICATION =============
if __name__ == '__main__':
    flask_app_wrapper.run(debug=True)