# Allamni v4.0 - Puter.com Deployment Configuration

## Overview
This document provides comprehensive deployment configuration for Allamni v4.0 on Puter.com, including environment setup, secrets management, and service configuration.

## Prerequisites
- Puter.com account
- Domain name (optional)
- PostgreSQL database (Puter provides managed instances)
- Redis instance (Puter provides managed instances)
- External AI provider credentials (Gemini API key)
- Odoo integration credentials (if applicable)

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