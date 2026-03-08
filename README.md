# docker-service-collection

**Cyber's Docker Service Collection** – A curated, production-ready set of Docker Compose and Dockerfile configurations tailored for modern AI development, DevOps workflows, and personal infrastructure.

This repository serves as a practical toolkit for developers, AI engineers, and sysadmins who want to quickly deploy, manage, and scale services using Docker. Each service is carefully selected and configured based on real-world usage in AI applications, data pipelines, and secure infrastructure setups.

Whether you're building a **LangChain-powered agent**, setting up a **RAG pipeline**, automating web intelligence with **AI-driven crawling**, or self-hosting private tools — this collection provides modular, well-documented, and easily customizable Docker services that integrate seamlessly.

Focus Areas:
- **AI & LLM Infrastructure**: Vector databases, web scraping for RAG, checkpointer backends.
- **Privacy-First Tools**: Self-hosted search, network proxies, and monitoring.
- **Developer Productivity**: Pre-configured services with best practices (networking, volumes, restart policies).
- **Modular Design**: All services can be mixed and matched via Docker Compose.

Tip: Combine services like PostgreSQL (for memory), Weaviate (for vector storage), and Crawl4ai (for data ingestion) into a single AI stack using custom networks and shared volumes.

Just clone, tweak the environment variables, and `docker compose up` — your dev stack is ready in seconds.

## Services

- Database
    - Relationship Database
       - [PostgreSQL](./PostgreSQL/docker-compose.yml): Best Open Source RDBMS for LangChain Checkpointer
    - Vector Database
       - [Weaviate](./Weaviate/docker-compose.yml): Open Source Vector Database, Good for LLM RAG
- Web Search and Web Crawl
    - [Crawl4ai](./Crawl4AI/docker-compose.yml): AI-Powered Web Scraping and Crawling
    - [SearXNG](./SearXNG/docker-compose.yml): Online Search, Self-hosted Search Engine. Good competitor to Travily AI, SerpAPI, etc.
- Network
    - [V2RayA](./V2RayA/docker-compose.yml): Network Proxy in Docker
- Docker Monitor
    - [Portainer](./Portainer/docker-compose.yml): A dashboard for Docker Management, if in a Linux Server.

## Example docker-compose.yml syntax with combination of services

```yaml
# name is the docker compose version name
name: ai-docker-stack

# define the services
services:
  postgres:
    image: postgres:18.2
    container_name: postgres
    restart: always
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql
    networks:
      - ai-docker-stack-network
      
  crawl4ai:
    image: unclecode/crawl4ai:latest
    container_name: crawl4ai
    ports:
      - "11235:11235"
    shm_size: 1gb
    restart: unless-stopped
    networks:
      - ai-docker-stack-network

# define the volumes need persistance
volumes:
  postgres_data:

# define the network for the docker compose stack
networks:
  ai-docker-stack-network:
    driver: bridge
    name: ai-docker-stack-network
    # add subnet for custom network
    ipam:
      config:
        # different docker compose need to set different subnet to avoid conflict
        - subnet: 10.200.1.0/24
```