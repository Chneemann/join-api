# Join API

This is the backend for the Join Task Manager application. It provides the necessary API endpoints for managing tasks, users, and their interactions with the task management system. Built using Django REST Framework, it integrates with PostgreSQL for data storage and Redis for caching.

## Technologies Used

- Django / Django REST Framework
- PostgreSQL
- Redis
- Python

## Features

- User authentication and authorization (JWT tokens)
- Task management with full CRUD operations (Create, Read, Update, Delete)
- Task prioritization and categorization
- User management (assigning tasks to users)
- Caching using Redis for faster response times
- Optimized database queries with PostgreSQL

## Description

The Join Task Manager Backend is designed to provide a robust and efficient API for task management. Built with Django REST Framework, this backend allows seamless communication with the frontend, handling user authentication, task creation, task management, and more.

Key features include:

- User Authentication: Secure login and registration using JWT tokens.
- Task Management: Full CRUD operations for tasks, including assigning priority levels, categories, and deadlines.
- User Assignment: Tasks can be assigned to users, allowing for effective collaboration.
- Database: PostgreSQL handles all data storage, ensuring reliability and scalability.
- Caching: Redis is used to cache frequently accessed data, improving performance.
