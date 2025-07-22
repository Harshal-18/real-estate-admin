# Real Estate Admin Panel

A comprehensive admin panel for managing real estate properties, developers, users, and more.

## Features

### 🏠 **Projects Management**
- Create, edit, and delete real estate projects
- Upload project images and documents
- Manage project details, pricing, and specifications
- Track project status and timeline

### 👥 **Developers Management**
- Manage developer profiles and information
- Upload developer logos
- Track developer statistics and ratings
- Link developers to projects

### 🏙️ **Cities & Locations**
- Manage cities and localities
- Organize projects by location
- Geographic data management

### 🏊 **Amenities Management**
- Create and manage property amenities
- Categorize amenities (lifestyle, sports, security, etc.)
- Icon support for visual representation

### 👤 **Users Management**
- User registration and profile management
- Role-based access control
- User verification system

### 📊 **Dashboard**
- Real-time statistics and analytics
- Recent activities feed
- Quick action buttons
- Visual charts and graphs

### 🔍 **Advanced Features**
- Search and filter functionality
- Bulk operations (delete, export)
- Pagination for large datasets
- File upload and management
- Responsive design for mobile devices

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL Database
- Flask framework

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd real-estate-admin
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Create a MySQL database
   - Update database configuration in `app/config.py`
   - Set up environment variables in `.env` file

5. **Run database migrations**
   ```bash
   flask db upgrade
   ```

6. **Start the application**
   ```bash
   python run.py
   ```

7. **Access the admin panel**
   - Open your browser and go to `http://localhost:5000/admin`
   - Use the default admin credentials (configured in config.py)

## Admin Panel Structure

### 📁 **File Organization**
```
app/
├── templates/
│   └── admin/
│       ├── base.html              # Base template with sidebar
│       ├── dashboard.html         # Main dashboard
│       ├── projects/              # Project management templates
│       ├── developers/            # Developer management templates
│       ├── cities/                # City management templates
│       ├── amenities/             # Amenity management templates
│       └── users/                 # User management templates
├── static/
│   ├── css/
│   │   └── admin.css             # Admin panel styles
│   └── js/
│       └── admin.js              # Admin panel JavaScript
└── routers/
    └── admin.py                  # Admin routes and logic
```

### 🎨 **Design Features**
- **Modern UI**: Clean, professional design with Bootstrap 5
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Interactive**: Real-time search, filters, and AJAX operations
- **Accessible**: Proper ARIA labels and keyboard navigation
- **Customizable**: Easy to modify colors, fonts, and layout

### 🔧 **Technical Features**
- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **File Upload**: Image and document upload with preview
- **Data Validation**: Client-side and server-side validation
- **Error Handling**: Comprehensive error messages and logging
- **Security**: CSRF protection, input sanitization, and access control

## Usage Guide

### 🏠 **Managing Projects**

1. **View Projects**
   - Navigate to "Projects" in the sidebar
   - Use search and filters to find specific projects
   - Click on project name to view details

2. **Create New Project**
   - Click "Add New Project" button
   - Fill in project details (name, developer, location, etc.)
   - Upload project images and documents
   - Set pricing and specifications
   - Save the project

3. **Edit Project**
   - Click the edit icon next to any project
   - Modify project information
   - Update images and documents
   - Save changes

4. **Delete Project**
   - Click the delete icon next to any project
   - Confirm deletion in the popup dialog

### 👥 **Managing Developers**

1. **View Developers**
   - Navigate to "Developers" in the sidebar
   - Browse through the list of developers
   - Use search to find specific developers

2. **Add New Developer**
   - Click "Add New Developer" button
   - Enter developer information (name, contact details, etc.)
   - Upload developer logo
   - Set verification status
   - Save the developer

3. **Edit Developer**
   - Click the edit icon next to any developer
   - Update developer information
   - Modify logo and settings
   - Save changes

### 🏙️ **Managing Cities**

1. **View Cities**
   - Navigate to "Cities" in the sidebar
   - Browse through the list of cities

2. **Add New City**
   - Click "Add New City" button
   - Enter city name, state, and country
   - Set active status
   - Save the city

### 🏊 **Managing Amenities**

1. **View Amenities**
   - Navigate to "Amenities" in the sidebar
   - Browse through different amenity categories

2. **Add New Amenity**
   - Click "Add New Amenity" button
   - Enter amenity name and description
   - Select category and icon
   - Set active status
   - Save the amenity

### 👤 **Managing Users**

1. **View Users**
   - Navigate to "Users" in the sidebar
   - Browse through registered users

2. **Add New User**
   - Click "Add New User" button
   - Enter user details (name, email, phone)
   - Set password and role
   - Upload profile picture
   - Set verification and active status
   - Save the user

## Customization

### 🎨 **Styling**
- Modify `app/static/css/admin.css` to change colors, fonts, and layout
- Update CSS variables in the `:root` selector for quick theme changes
- Add custom CSS classes for specific components

### 🔧 **Functionality**
- Extend admin routes in `app/routers/admin.py`
- Add new models and database tables
- Create additional templates for new features
- Modify JavaScript functions in `app/static/js/admin.js`

### 📊 **Dashboard**
- Add new statistics cards in `app/templates/admin/dashboard.html`
- Create custom charts and graphs
- Add new activity types to the recent activities feed

## Security Considerations

### 🔒 **Access Control**
- Implement proper authentication and authorization
- Use role-based access control for different admin functions
- Secure file uploads with proper validation
- Implement CSRF protection for all forms

### 🛡️ **Data Protection**
- Validate and sanitize all user inputs
- Use prepared statements for database queries
- Implement proper error handling without exposing sensitive information
- Regular security audits and updates

## Troubleshooting

### 🔧 **Common Issues**

1. **Database Connection Error**
   - Check database configuration in `config.py`
   - Ensure MySQL server is running
   - Verify database credentials

2. **File Upload Issues**
   - Check upload folder permissions
   - Verify file size limits in configuration
   - Ensure proper file type validation

3. **Template Errors**
   - Check template syntax and variable names
   - Verify template inheritance structure
   - Ensure all required variables are passed to templates

4. **JavaScript Errors**
   - Check browser console for JavaScript errors
   - Verify jQuery and Bootstrap are loaded
   - Test AJAX functionality

### 📞 **Support**
- Check the application logs for detailed error messages
- Review the Flask debug output for development issues
- Ensure all dependencies are properly installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Administering! 🎉** 