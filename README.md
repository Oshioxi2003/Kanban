Dưới đây là mẫu `README.md` dành cho dự án ứng dụng web **Personal Kanban Life Planner** – trình bày rõ ràng, chuyên nghiệp, phù hợp với GitHub hoặc portfolio cá nhân:

---

```markdown
# 🗓️ Personal Kanban Life Planner

A modern, intuitive web application that helps users organize tasks, goals, and personal routines using a drag-and-drop **Kanban board** combined with **calendar scheduling**.

> 🎯 Designed for students, creators, professionals, and anyone who needs a flexible system to manage life and work visually.

---

## 🚀 Features

- **User Authentication**: Login and user management
- **Board Management**: Create, edit, and delete Kanban boards
- **List Management**: Add, reorder, and manage lists within boards
- **Card Management**: Create, edit, move, and delete cards
- **Drag & Drop**: Intuitive drag-and-drop functionality for cards and lists
- **Priority System**: Set card priorities (Low, Medium, High, Urgent)
- **Due Dates**: Add due dates to cards with overdue indicators
- **Comments**: Add comments to cards for collaboration
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Technology Stack

### Backend
- **Django 4.2.7**: Python web framework
- **Django REST Framework**: API development
- **PyMySQL**: MySQL database adapter
- **Django CORS Headers**: Cross-origin resource sharing
- **WhiteNoise**: Static file serving
- **Gunicorn**: WSGI HTTP server

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vue Router**: Client-side routing
- **Pinia**: State management
- **Vite**: Build tool and development server
- **TailwindCSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **Headless UI**: Unstyled, accessible UI components

### Database
- **MySQL 8.0**: Relational database
- **SQLite**: Development database (fallback)

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and static file serving

## 📦 Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- MySQL 8.0+ (for production)
- Docker & Docker Compose (for containerized deployment)

### Development Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd Kanban
```

#### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables (optional)
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

#### 4. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

### Production Deployment with Docker

#### 1. Environment Configuration
Create a `.env` file with production settings:
```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=mysql://kanban_user:kanban_password@mysql:3306/kanban_db
ALLOWED_HOSTS=yourdomain.com,localhost
```

#### 2. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 3. Access the Application
- **Application**: http://localhost (Nginx proxy)
- **Backend API**: http://localhost/api/
- **Django Admin**: http://localhost/admin/

## 🗄️ Database Schema

### Models
- **Board**: Kanban boards with title, description, and owner
- **List**: Columns within boards with position ordering
- **Card**: Tasks/items within lists with priority, due dates, and assignments
- **Comment**: Comments on cards for collaboration

### Key Features
- User-based board ownership
- Position-based ordering for lists and cards
- Priority system (Low, Medium, High, Urgent)
- Due date tracking with overdue detection
- Comment system for collaboration

## 🔌 API Endpoints

### Boards
- `GET /api/boards/` - List all boards
- `POST /api/boards/` - Create new board
- `GET /api/boards/{id}/` - Get board details
- `PATCH /api/boards/{id}/` - Update board
- `DELETE /api/boards/{id}/` - Delete board
- `POST /api/boards/{id}/duplicate/` - Duplicate board

### Lists
- `GET /api/lists/` - List all lists
- `POST /api/lists/` - Create new list
- `GET /api/lists/{id}/` - Get list details
- `PATCH /api/lists/{id}/` - Update list
- `DELETE /api/lists/{id}/` - Delete list
- `POST /api/lists/{id}/reorder/` - Reorder list position

### Cards
- `GET /api/cards/` - List all cards
- `POST /api/cards/` - Create new card
- `GET /api/cards/{id}/` - Get card details
- `PATCH /api/cards/{id}/` - Update card
- `DELETE /api/cards/{id}/` - Delete card
- `POST /api/cards/{id}/move/` - Move card between lists

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create new comment
- `PATCH /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

## 🎨 Frontend Structure

```
frontend/
├── src/
│   ├── components/          # Vue components
│   │   ├── KanbanBoard.vue
│   │   ├── KanbanList.vue
│   │   ├── KanbanCard.vue
│   │   └── ...
│   ├── views/              # Page components
│   │   ├── BoardList.vue
│   │   └── BoardDetail.vue
│   ├── stores/             # Pinia stores
│   │   └── kanban.js
│   ├── services/           # API services
│   │   └── api.js
│   └── router/             # Vue Router config
│       └── index.js
├── package.json
└── vite.config.js
```

## 🔧 Configuration

### Django Settings
Key settings in `kanban_project/settings.py`:
- Database configuration with MySQL/SQLite fallback
- CORS settings for frontend integration
- REST Framework configuration
- Static file handling with WhiteNoise

### Frontend Configuration
Key files:
- `vite.config.js`: Build tool configuration
- `tailwind.config.js`: TailwindCSS customization
- `src/services/api.js`: API client configuration

## 🧪 Testing

### Backend Testing
```bash
# Run Django tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Testing
```bash
# Run frontend tests (if configured)
cd frontend
npm run test
```

## 🚀 Deployment Options

### 1. Docker Compose (Recommended)
Complete containerized deployment with MySQL, Nginx, and auto-scaling.

### 2. Manual Deployment
- Deploy Django backend to platforms like Heroku, DigitalOcean, or AWS
- Deploy Vue.js frontend to Netlify, Vercel, or CDN
- Use managed MySQL service

### 3. Kubernetes
For large-scale deployments, convert Docker Compose to Kubernetes manifests.

## 🛠️ Development

### Code Structure
- **Backend**: Django REST API with ViewSets and Serializers
- **Frontend**: Vue 3 Composition API with Pinia for state management
- **Database**: Normalized schema with proper relationships
- **Styling**: TailwindCSS utility classes with custom components

### Key Features Implementation
- **Drag & Drop**: Vue.Draggable with API synchronization
- **Real-time Updates**: Optimistic UI updates with API validation
- **Responsive Design**: Mobile-first TailwindCSS approach
- **Error Handling**: Comprehensive error handling and user feedback

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Known Issues

- MySQL installation on Windows requires additional setup
- WebSocket real-time updates not yet implemented
- Mobile drag-and-drop may need optimization

## 🚧 Roadmap

- [ ] WebSocket integration for real-time collaboration
- [ ] File attachments for cards
- [ ] Advanced filtering and search
- [ ] Team management and permissions
- [ ] Mobile app development
- [ ] Integration with external services (GitHub, Slack, etc.)

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Happy coding! 🎉**