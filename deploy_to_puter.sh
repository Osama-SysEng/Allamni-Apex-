#!/bin/bash

# Allamni v4.0 - Puter.com Deployment Script
# This script automates the deployment process to Puter.com

set -e

echo "🚀 Starting Allamni v4.0 deployment to Puter.com..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="allamni-v4"
PUTER_USERNAME="your_puter_username"
DOMAIN="allamni.puter.com"

# Step 1: Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Step 2: Prepare environment
echo -e "${YELLOW}🔧 Preparing environment...${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please update .env with your actual values${NC}"
fi

# Step 3: Build Docker images
echo -e "${YELLOW}🐳 Building Docker images...${NC}"

docker-compose build

echo -e "${GREEN}✅ Docker images built successfully${NC}"

# Step 4: Test locally
echo -e "${YELLOW}🧪 Testing locally before deployment...${NC}"

docker-compose up -d

echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 30

# Test health endpoints
echo -e "${YELLOW}Testing health endpoints...${NC}"

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API Gateway is healthy${NC}"
else
    echo -e "${RED}❌ API Gateway health check failed${NC}"
    docker-compose down
    exit 1
fi

if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Auth Service is healthy${NC}"
else
    echo -e "${RED}❌ Auth Service health check failed${NC}"
    docker-compose down
    exit 1
fi

if curl -f http://localhost:8003/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ AI Service is healthy${NC}"
else
    echo -e "${RED}❌ AI Service health check failed${NC}"
    docker-compose down
    exit 1
fi

echo -e "${GREEN}✅ All services are healthy${NC}"

# Step 5: Stop local containers
echo -e "${YELLOW}🛑 Stopping local containers...${NC}"
docker-compose down

# Step 6: Deploy to Puter.com
echo -e "${YELLOW}🌐 Deploying to Puter.com...${NC}"

# This would typically use the Puter CLI or API
# For now, this is a placeholder for the actual deployment command
echo -e "${YELLOW}Please use the Puter.com dashboard to deploy:${NC}"
echo -e "${YELLOW}1. Login to https://puter.com${NC}"
echo -e "${YELLOW}2. Create a new project: $PROJECT_NAME${NC}"
echo -e "${YELLOW}3. Select Python 3.11 runtime${NC}"
echo -e "${YELLOW}4. Upload the project files${NC}"
echo -e "${YELLOW}5. Configure environment variables from .env${NC}"
echo -e "${YELLOW}6. Add PostgreSQL database${NC}"
echo -e "${YELLOW}7. Add Redis cache${NC}"
echo -e "${YELLOW}8. Deploy services${NC}"
echo -e "${YELLOW}9. Configure domain: $DOMAIN${NC}"

# Step 7: Run database migrations
echo -e "${YELLOW}🗄️  Running database migrations...${NC}"
echo -e "${YELLOW}This should be done after deployment via Puter's terminal${NC}"
echo -e "${YELLOW}Command: psql $DATABASE_URL -f infrastructure/scripts/migrations/001_add_institutions_and_codes.sql${NC}"

# Step 8: Verify deployment
echo -e "${YELLOW}🔍 Deployment verification...${NC}"
echo -e "${YELLOW}After deployment, verify:${NC}"
echo -e "${YELLOW}1. API Gateway: https://$DOMAIN/health${NC}"
echo -e "${YELLOW}2. Auth Service: https://$DOMAIN/api/auth/health${NC}"
echo -e "${YELLOW}3. AI Service: https://$DOMAIN/api/ai/health${NC}"
echo -e "${YELLOW}4. Institution Service: https://$DOMAIN/api/institution/health${NC}"

echo -e "${GREEN}🎉 Deployment preparation complete!${NC}"
echo -e "${GREEN}📝 Next steps:${NC}"
echo -e "${GREEN}1. Update .env with actual values${NC}"
echo -e "${GREEN}2. Deploy to Puter.com using the dashboard${NC}"
echo -e "${GREEN}3. Run database migrations${NC}"
echo -e "${GREEN}4. Test the deployed application${NC}"
echo -e "${GREEN}5. Configure custom domain (optional)${NC}"