# Allamni v4.0 - Puter.com Deployment Guide

## 🚀 Quick Start Deployment

### Step 1: Create Puter.com Account
1. Go to https://puter.com
2. Sign up for a free account
3. Verify your email address

### Step 2: Create New Project
1. Click "Create New Project"
2. Project name: `allamni-v4`
3. Description: `Allamni v4.0 - AI-Native Education Operating System`
4. Runtime: `Python 3.11`
5. Region: Choose closest to your users

### Step 3: Upload Project Files
1. Click "Upload Files" or "Connect GitHub"
2. Upload all files from the Allamni-Apex directory
3. Alternatively, connect your GitHub repository: https://github.com/Osama-SysEng/Allamni-Apex-

### Step 4: Configure Database
1. Go to "Resources" → "Add Database"
2. Select "PostgreSQL"
3. Database name: `allamni`
4. Size: `Small` (for testing) or `Medium` (for production)
5. Note the connection details (will be used in environment variables)

### Step 5: Configure Redis
1. Go to "Resources" → "Add Cache"
2. Select "Redis"
3. Cache name: `allamni-cache`
4. Size: `Small`
5. Note the connection details

### Step 6: Configure Environment Variables
Go to "Settings" → "Environment Variables" and add:

```bash
# Database Configuration
DATABASE_URL=postgresql://your_db_user:your_db_password@your_db_host:5432/allamni
REDIS_URL=redis://your_redis_host:6379

# AI Provider Configuration
AI_PROVIDER=mock  # Change to 'gemini' when you have API key
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro

# Security Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here_change_in_production
JWT_ACCESS_MINUTES=30
JWT_REFRESH_DAYS=7

# Service URLs (Puter internal URLs)
AUTH_URL=http://auth-service:8001
LEARNING_URL=http://learning-service:8002
AI_URL=http://ai-service:8003
INTEGRATION_URL=http://integration-service:8004
INSTITUTION_URL=http://institution-service:8005

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://allamni.puter.com

# Monitoring
LOG_LEVEL=info
```

### Step 7: Configure Services
In Puter.com, create the following services:

#### API Gateway
- Name: `api-gateway`
- Build context: `backend/api_gateway`
- Port: `8000`
- Environment variables: `AUTH_URL`, `AI_URL`, `INSTITUTION_URL`, `CORS_ALLOWED_ORIGINS`

#### Auth Service
- Name: `auth-service`
- Build context: `backend/services/auth-service`
- Port: `8001`
- Environment variables: `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET_KEY`

#### AI Service
- Name: `ai-service`
- Build context: `backend/services/ai-service`
- Port: `8003`
- Environment variables: `AI_PROVIDER`, `GEMINI_API_KEY`, `DATABASE_URL`

#### Institution Service
- Name: `institution-service`
- Build context: `backend/services/institution-service`
- Port: `8005`
- Environment variables: `DATABASE_URL`, `REDIS_URL`

### Step 8: Deploy
1. Click "Deploy" for each service
2. Wait for deployment to complete
3. Check deployment logs for any errors

### Step 9: Run Database Migrations
1. Go to "Terminal" in Puter.com
2. Run the migration script:
```bash
psql $DATABASE_URL -f infrastructure/scripts/migrations/001_add_institutions_and_codes.sql
```

### Step 10: Configure Domain
1. Go to "Domains" → "Add Domain"
2. Primary domain: `allamni.puter.com` (auto-generated)
3. Custom domain: Add your own domain if desired
4. Configure DNS records if using custom domain

### Step 11: Test Deployment
Test the following endpoints:
- API Gateway: `https://allamni.puter.com/health`
- Auth Service: `https://allamni.puter.com/api/auth/health`
- AI Service: `https://allamni.puter.com/api/ai/health`

## 📱 Flutter App Deployment

### Build Flutter Web App
```bash
cd flutter_app
flutter build web --release
```

### Deploy to Puter Static Hosting
1. Go to "Static Files" in Puter.com
2. Upload the contents of `flutter_app/build/web`
3. Configure routing to serve as single-page app
4. Access at: `https://allamni.puter.com`

## 🔧 Advanced Configuration

### Auto-scaling Configuration
In Puter.com dashboard, configure auto-scaling for each service:
- API Gateway: 1-3 instances, target CPU 70%
- Auth Service: 1-2 instances, target CPU 60%
- AI Service: 1-2 instances, target CPU 80%

### Monitoring Setup
1. Enable Prometheus metrics in each service
2. Configure Grafana dashboards
3. Set up alerting for critical metrics

### Security Enhancements
1. Enable SSL/TLS (Puter provides this automatically)
2. Configure security headers
3. Set up rate limiting
4. Enable request logging

## 🎯 Production Checklist

- [ ] All environment variables configured
- [ ] Database migrations completed
- [ ] All services deployed and healthy
- [ ] Domain configured and accessible
- [ ] SSL/TLS enabled
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Error tracking (Sentry) configured
- [ ] Rate limiting enabled
- [ ] Security audit completed

## 🚨 Troubleshooting

### Common Issues

**Service won't start:**
- Check logs in Puter.com dashboard
- Verify environment variables are correct
- Ensure database and Redis are accessible

**Database connection errors:**
- Verify DATABASE_URL is correct
- Check database is running
- Test connectivity from Puter terminal

**API errors:**
- Check service logs
- Verify service-to-service communication
- Check CORS configuration

## 📊 Monitoring

Access monitoring at:
- Puter Dashboard: Built-in metrics
- Prometheus: `https://allamni.puter.com/metrics`
- Grafana: Configure via Puter dashboard

## 🔄 Updates and Maintenance

### Update Process
1. Push changes to GitHub
2. In Puter.com, click "Redeploy"
3. Monitor deployment logs
4. Test critical functionality

### Backup Strategy
- Enable automatic daily backups in Puter.com
- Test backup restoration regularly
- Keep backup of environment variables

## 📞 Support

For Puter.com specific issues:
- Puter Documentation: https://docs.puter.com
- Puter Support: support@puter.com

For Allamni specific issues:
- GitHub Issues: https://github.com/Osama-SysEng/Allamni-Apex-/issues

## Environment Variables

### Backend Services
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@postgres-host:5432/allamni
REDIS_URL=redis://redis-host:6379

# AI Provider Configuration
AI_PROVIDER=gemini  # or mock for development
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro

# Security Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ACCESS_MINUTES=30
JWT_REFRESH_DAYS=7
ENCRYPTION_KEY=your_encryption_key_here

# Service URLs
AUTH_URL=http://auth-service:8001
LEARNING_URL=http://learning-service:8002
AI_URL=http://ai-service:8003
INTEGRATION_URL=http://integration-service:8004
INSTITUTION_URL=http://institution-service:8005

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://your-app.puter.com,https://your-custom-domain.com

# Odoo Integration (Optional)
ODOO_URL=https://your-odoo-instance.com
ODOO_API_KEY=your_odoo_api_key
ODOO_DATABASE=your_odoo_database

# Monitoring & Logging
LOG_LEVEL=info
SENTRY_DSN=your_sentry_dsn_optional
```

### Flutter App Configuration
```bash
# API Configuration
API_BASE_URL=https://your-app.puter.com
API_VERSION=/api/v1

# Service URLs
AUTH_BASE_URL=https://your-app.puter.com/api/auth
AI_BASE_URL=https://your-app.puter.com/api/ai
INSTITUTION_BASE_URL=https://your-app.puter.com/api/institution

# Feature Flags
ENABLE_VOICE_INPUT=true
ENABLE_IMAGE_ANALYSIS=true
ENABLE_OFFLINE_MODE=true
ENABLE_NOTIFICATIONS=true
ENABLE_PHASE5_CHATBOT=true
```

## Puter.com Deployment Steps

### 1. Project Setup
1. Create a new project on Puter.com
2. Select "Python FastAPI" as the runtime
3. Configure project name: `allamni-v4`
4. Set region: Choose closest to your users

### 2. Database Setup
1. Add PostgreSQL database to your project
2. Note connection details (host, port, database, user, password)
3. Run database migrations:
```bash
psql $DATABASE_URL -f infrastructure/scripts/migrations/001_add_institutions_and_codes.sql
```

### 3. Redis Setup
1. Add Redis instance to your project
2. Note connection details
3. Configure Redis for sessions and caching

### 4. Environment Configuration
1. Add all environment variables listed above
2. Use Puter's secrets manager for sensitive values
3. Never commit secrets to version control

### 5. Backend Deployment
Create `puter.yaml` configuration:

```yaml
name: allamni-v4
version: 4.0.0
runtime: python-3.11

services:
  api-gateway:
    build: ./backend/api_gateway
    port: 8000
    env:
      - AUTH_URL
      - LEARNING_URL
      - AI_URL
      - INTEGRATION_URL
      - INSTITUTION_URL
      - CORS_ALLOWED_ORIGINS

  auth-service:
    build: ./backend/services/auth-service
    port: 8001
    env:
      - DATABASE_URL
      - REDIS_URL
      - JWT_SECRET_KEY
      - JWT_ACCESS_MINUTES
      - JWT_REFRESH_DAYS

  ai-service:
    build: ./backend/services/ai-service
    port: 8003
    env:
      - AI_PROVIDER
      - GEMINI_API_KEY
      - GEMINI_MODEL
      - DATABASE_URL

  institution-service:
    build: ./backend/services/institution-service
    port: 8005
    env:
      - DATABASE_URL
      - REDIS_URL

  integration-service:
    build: ./backend/services/integration-service
    port: 8004
    env:
      - ODOO_URL
      - ODOO_API_KEY
      - ODOO_DATABASE
      - DATABASE_URL

databases:
  - type: postgresql
    name: allamni-db
    size: small

caches:
  - type: redis
    name: allamni-cache
    size: small
```

### 6. Flutter Web Deployment
1. Build Flutter web app:
```bash
cd flutter_app
flutter build web --release
```

2. Deploy to Puter static hosting:
```bash
puter deploy --path build/web --domain allamni.puter.com
```

### 7. Domain Configuration (Optional)
1. Add custom domain in Puter dashboard
2. Configure DNS records:
   - A record: `your-domain.com` → Puter IP
   - CNAME: `www.your-domain.com` → Puter domain
3. Enable SSL/TLS certificates

## Security Configuration

### Production Security Checklist
- [ ] All secrets stored in Puter secrets manager
- [ ] HTTPS enforced for all endpoints
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation active
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Security headers configured
- [ ] Regular security scans enabled

### API Security Headers
Configure in API gateway:
```python
app.add_middleware(
    SecurityMiddleware,
    headers={
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    }
)
```

## Monitoring & Logging

### Logging Configuration
```python
import logging
from puter import logger

logger.setLevel(logging.INFO)
logger.addHandler(puter.LoggingHandler())
```

### Metrics Collection
- Enable Prometheus metrics in API gateway
- Configure Grafana dashboards
- Set up alerting for critical metrics

### Error Tracking
- Configure Sentry for error tracking
- Set up alerts for high error rates
- Monitor performance metrics

## Scaling Configuration

### Horizontal Scaling
```yaml
scaling:
  api-gateway:
    min_instances: 2
    max_instances: 10
    target_cpu: 70%
  
  auth-service:
    min_instances: 2
    max_instances: 5
    target_cpu: 60%
  
  ai-service:
    min_instances: 1
    max_instances: 8
    target_cpu: 80%
```

### Load Balancing
- Puter provides automatic load balancing
- Configure health checks for all services
- Set up circuit breakers for external dependencies

## Backup & Recovery

### Database Backups
- Enable automatic daily backups
- Configure point-in-time recovery
- Test backup restoration regularly

### Redis Backup
- Enable Redis persistence (AOF)
- Configure regular snapshots
- Test Redis recovery

## CI/CD Pipeline

### Puter CI/CD Configuration
```yaml
version: 1
pipeline:
  build:
    - pip install -r requirements.txt
    - python -m pytest tests/
    - docker build -t allamni-backend .
  
  deploy:
    - puter deploy --environment production
    - puter run migrations
    - puter restart services
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify DATABASE_URL is correct
   - Check database instance is running
   - Ensure network connectivity

2. **Redis Connection Errors**
   - Verify REDIS_URL is correct
   - Check Redis instance is running
   - Test Redis connectivity

3. **AI Provider Errors**
   - Verify GEMINI_API_KEY is valid
   - Check API rate limits
   - Test API connectivity

4. **Flutter Build Errors**
   - Ensure Flutter SDK is compatible
   - Check dependencies are resolved
   - Verify web build configuration

## Performance Optimization

### Backend Optimization
- Enable response compression
- Configure database connection pooling
- Implement request caching
- Optimize database queries

### Flutter Optimization
- Enable code splitting
- Optimize asset loading
- Implement lazy loading
- Configure service workers

## Cost Optimization

### Puter Cost Management
- Monitor resource usage
- Right-size instances based on load
- Enable auto-scaling to reduce idle costs
- Use reserved instances for predictable workloads

## Compliance & Privacy

### Data Protection
- GDPR compliance checklist
- Data encryption at rest and in transit
- User consent management
- Data retention policies

### Access Control
- Role-based access control
- Audit logging
- Regular access reviews
- Multi-factor authentication for admin access

## Maintenance

### Regular Maintenance Tasks
- Weekly: Review logs and metrics
- Monthly: Update dependencies
- Quarterly: Security audits
- Annually: Disaster recovery testing

### Update Procedures
1. Test updates in staging environment
2. Create database backups before updates
3. Deploy updates during low-traffic periods
4. Monitor system after deployment
5. Roll back if issues detected

## Support & Documentation

### Documentation Links
- Puter.com documentation: https://docs.puter.com
- FastAPI documentation: https://fastapi.tiangolo.com
- Flutter deployment: https://flutter.dev/docs/deployment/web

### Emergency Contacts
- Technical support: support@puter.com
- Security team: security@allamni.com
- On-call rotation: oncall@allamni.com

## Version History
- v4.0.0 - Initial Phase 5 deployment configuration
- v3.0.0 - Previous baseline version