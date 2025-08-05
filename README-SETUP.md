# 🚀 Setup Guide for Personal Kanban Life Planner

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+
- Docker & Docker Compose
- MySQL 8.0+ (for production)

## 🔧 Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd Kanban
```

### 2. Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings
# For development, you can use default values
```

### 3. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 4. Frontend Setup
```bash
cd frontend

# Copy environment template
cp env.example .env

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

## 🐳 Docker Development

### 1. Setup Environment
```bash
cp env.example .env
# Edit .env with your settings
```

### 2. Run with Docker Compose
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Access Application
- Application: http://localhost
- Backend API: http://localhost/api/
- Django Admin: http://localhost/admin/

## 🚀 Production Deployment

### 1. Environment Configuration
```bash
# Copy production template
cp env.production.example .env

# Edit .env with your production settings:
# - Change SECRET_KEY to a strong random key
# - Set DEBUG=False
# - Configure ALLOWED_HOSTS with your domain
# - Set up database credentials
# - Configure email settings
# - Set up Google OAuth credentials
# - Configure SSL settings
```

### 2. SSL Certificate Setup
```bash
# Create SSL directory
mkdir ssl

# Add your SSL certificates:
# ssl/cert.pem
# ssl/privkey.pem
```

### 3. Deploy with Production Docker Compose
```bash
# Build and deploy
docker-compose -f docker-production.yml up --build -d

# View logs
docker-compose -f docker-production.yml logs -f

# Stop services
docker-compose -f docker-production.yml down
```

## 🔐 Security Checklist

### Before Production:
- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Use strong database passwords
- [ ] Set up proper email configuration
- [ ] Configure Google OAuth with production credentials
- [ ] Set up SSL certificates
- [ ] Enable security headers
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Regular security updates

## 📊 Monitoring

### Health Checks
```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql
docker-compose logs redis
```

### Database Backup
```bash
# Backup database
docker exec kanban_mysql_prod mysqldump -u kanban_user -p kanban_db > backup.sql

# Restore database
docker exec -i kanban_mysql_prod mysql -u kanban_user -p kanban_db < backup.sql
```

## 🔧 Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Check MySQL service is running
   - Verify database credentials in .env
   - Ensure database exists

2. **Frontend Can't Connect to Backend**
   - Check VITE_API_URL in frontend .env
   - Verify CORS settings in backend
   - Check if backend is running

3. **Permission Denied on Static Files**
   - Check file permissions: `chmod -R 755 staticfiles/`
   - Verify volume mounts in docker-compose

4. **SSL Certificate Issues**
   - Verify certificate files exist in ssl/ directory
   - Check certificate validity
   - Ensure nginx configuration is correct

### Logs Location:
- Application logs: `kanban.log`
- Docker logs: `docker-compose logs [service-name]`
- Nginx logs: Inside nginx container

## 📞 Support

For issues and support:
1. Check this guide first
2. Review application logs
3. Check Docker service status
4. Open an issue in the repository

---

**Happy coding! 🎉**