# API framework serialization performance

> This is a fork of https://github.com/oscarychen/building-efficient-api which adds additional Django API frameworks for comparison.

## Introduction

This project is to compare the performance of serialization between different API frameworks. 

### Frameworks

- [Django](https://www.djangoproject.com)
- [Django REST Framework (DRF)](https://www.django-rest-framework.org)
- [Django Ninja](https://django-ninja.dev)
- [Django Shinobi](https://pmdevita.github.io/django-shinobi/)
- [Django Rapid](https://github.com/FarhanAliRaza/django-rapid)
- [Django Bolt](https://github.com/FarhanAliRaza/django-bolt)
- [Djrest2](https://gitlab.levitnet.be/levit/djrest)
- [FastAPI](https://fastapi.tiangolo.com/) (not included in benchmarks by default)

## Methodology

Each API framework is in its own Docker container, along with a shared PostgreSQL database which is used to store the sample data.

A Locust API load testing tool is also included to run the tests. To ensure similar resource is available to each docker container during the tests, each Locust test is run sequentially, so when one framework is handling a request, the others are idle.

## Quick Start

1. Install [`just`](https://just.systems/man/en/packages.html)
2. `just up`: builds and starts all Docker containers
3. `just populate`: populates the database with sample data
4. `just test`: validates all APIs are returning the same data
5. `just benchmark`: basic benchmarks
6. Go to http://localhost:8089 to use `locust` for load testing

### Validation

```bash
just test
```

### Benchmarks

```bash
just benchmark
```
