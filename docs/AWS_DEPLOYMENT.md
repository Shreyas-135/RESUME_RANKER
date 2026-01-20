# AWS Deployment Guide

## Prerequisites
- AWS Account with appropriate permissions
- Docker and Docker Compose installed locally
- OpenAI API key
- Basic knowledge of AWS services (EC2, VPC, Security Groups, ALB)

## Deployment Methods

### Method 1: Manual EC2 Deployment (Recommended for Learning)

#### Step 1: Launch EC2 Instance
```bash
# Use Ubuntu 22.04 LTS
# Instance type: t3.medium or larger (minimum 4GB RAM)
# Storage: 30GB EBS volume
```

#### Step 2: Configure Security Groups
```
Inbound Rules:
- SSH (22) from your IP
- HTTP (80) from anywhere
- HTTPS (443) from anywhere (if using SSL)
```

#### Step 3: Connect and Install Dependencies
```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo apt install docker-compose -y

# Logout and login again for docker group to take effect
exit
```

#### Step 4: Clone and Configure
```bash
# Clone repository
git clone https://github.com/Shreyas-135/RESUME_RANKER
cd RESUME_RANKER

# Copy environment files
cp analysis_service/.env.example analysis_service/.env
cp backend/.env.example backend/.env.local
cp frontend/.env.example frontend/.env.production

# Edit environment files with your values
nano analysis_service/.env  # Add OPENAI_API_KEY
nano backend/.env.local      # Configure settings
nano frontend/.env.production # Set NEXT_PUBLIC_API_URL=http://YOUR_EC2_IP/backend
```

#### Step 5: Deploy Application
```bash
# Build and start services
docker-compose build
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f
```

#### Step 6: Access Application
```
Frontend: http://YOUR_EC2_IP
Backend API: http://YOUR_EC2_IP/backend
```

### Method 2: Automated Deployment with GitHub Actions

The repository already includes CI/CD pipelines for automated deployment.

**Required GitHub Secrets:**
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
SSH_PRIVATE_KEY
DOCKERHUB_USERNAME
DOCKERHUB_PASSWORD
OPENAI_API_KEY
```

**Deployment Branches:**
- `develop` → Development environment (CI only)
- `staging` → Staging environment (Full deployment)
- `master` → Production environment (Full deployment)

**To deploy:**
1. Configure GitHub secrets in repository settings
2. Push code to the appropriate branch
3. GitHub Actions will automatically deploy

### Method 3: AWS ECS with Fargate (Production Ready)

#### Step 1: Create ECR Repositories
```bash
aws ecr create-repository --repository-name resume-ranker/frontend
aws ecr create-repository --repository-name resume-ranker/backend
aws ecr create-repository --repository-name resume-ranker/analysis-service
```

#### Step 2: Push Docker Images
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push images
docker-compose build
docker tag vectornguyen76/resume_ranking_frontend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/resume-ranker/frontend:latest
docker tag vectornguyen76/resume_ranking_backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/resume-ranker/backend:latest
docker tag vectornguyen76/analysis_service:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/resume-ranker/analysis-service:latest

docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/resume-ranker/frontend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/resume-ranker/backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/resume-ranker/analysis-service:latest
```

#### Step 3: Create ECS Cluster and Task Definitions
- Use AWS Console or Infrastructure as Code (Terraform/CloudFormation)
- Configure task definitions with appropriate CPU/Memory
- Set environment variables for each service

#### Step 4: Create Application Load Balancer
- Configure target groups for frontend and backend
- Set up path-based routing (/backend/* → backend service)

#### Step 5: Create ECS Services
- Deploy services with desired task count
- Configure auto-scaling policies

## Environment-Specific Configuration

**Development:**
```bash
# Use local MongoDB
MONGO_URL=mongodb://mongo_db:27017/resume_ranking
NEXT_PUBLIC_API_URL=http://localhost/backend
```

**Staging/Production:**
```bash
# Use MongoDB Atlas or AWS DocumentDB
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/resume_ranking
NEXT_PUBLIC_API_URL=https://your-domain.com/backend
```

## Cost Optimization Tips

1. **Use AWS Free Tier:** t2.micro for testing
2. **Use Spot Instances:** For non-production workloads
3. **Set up Auto-Scaling:** Scale down during off-hours
4. **Use MongoDB Atlas Free Tier:** Instead of self-hosted MongoDB
5. **Enable CloudWatch Alarms:** Monitor costs

## Security Best Practices

1. **Never commit `.env` files** with real credentials
2. **Use AWS Secrets Manager** for sensitive data in production
3. **Enable HTTPS** with AWS Certificate Manager
4. **Restrict Security Groups** to minimum required access
5. **Regular security updates** for dependencies
6. **Enable CloudTrail** for audit logging

## Monitoring and Logging

```bash
# View application logs
docker-compose logs -f [service_name]

# AWS CloudWatch for production
# Configure CloudWatch Logs agent on EC2
# Or use ECS built-in CloudWatch integration
```

## Troubleshooting

**Common Issues:**

1. **Services not starting:**
```bash
docker-compose logs [service_name]
docker-compose restart [service_name]
```

2. **MongoDB connection errors:**
```bash
# Check if MongoDB is running
docker-compose ps
# Verify MONGO_URL in environment files
```

3. **Frontend can't connect to backend:**
```bash
# Ensure NEXT_PUBLIC_API_URL is correct
# Check nginx configuration
# Verify backend service is running
```

4. **OpenAI API errors:**
```bash
# Verify OPENAI_API_KEY is set correctly
# Check OpenAI API quota/billing
```

## Scaling Considerations

**Horizontal Scaling:**
- Use AWS ECS or EKS for container orchestration
- Deploy multiple backend/analysis service instances
- Use Redis for session management

**Database Scaling:**
- Use MongoDB Atlas with auto-scaling
- Or AWS DocumentDB with read replicas

**Caching:**
- Add Redis for caching OpenAI responses
- Implement CDN for static frontend assets
