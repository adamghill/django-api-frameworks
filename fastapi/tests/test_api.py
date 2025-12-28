import pytest
from car.models import Car, CarModel
from database import Base, get_db
from httpx import ASGITransport, AsyncClient
from main import app
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/test_django_api_frameworks"


@pytest.fixture(scope="function")
async def setup_test_database():
    """Create and destroy test database"""

    # Connect to postgres database to create test database
    postgres_engine = create_async_engine("postgresql+asyncpg://postgres:postgres@db:5432/postgres", echo=False)

    # Use autocommit mode for database creation/deletion
    async with postgres_engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(
            text(
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                "FROM pg_stat_activity "
                "WHERE pg_stat_activity.datname = 'test_django_api_frameworks' "
                "AND pid <> pg_backend_pid()"
            )
        )
        await conn.execute(text("DROP DATABASE IF EXISTS test_django_api_frameworks"))
        await conn.execute(text("CREATE DATABASE test_django_api_frameworks"))

    await postgres_engine.dispose()

    yield

    # Clean up: drop test database
    postgres_engine = create_async_engine("postgresql+asyncpg://postgres:postgres@db:5432/postgres", echo=False)

    async with postgres_engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(text("DROP DATABASE IF EXISTS test_django_api_frameworks"))

    await postgres_engine.dispose()


@pytest.fixture(scope="function")
async def test_engine_fixture(setup_test_database):
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    yield test_engine, TestSessionLocal

    await test_engine.dispose()


@pytest.fixture(scope="function")
async def test_db(test_engine_fixture):
    """Create a test database session"""
    test_engine, TestSessionLocal = test_engine_fixture

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(test_db: AsyncSession):
    """Create a test client with test database"""

    def override_get_db():
        return test_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def create_test_data(test_db: AsyncSession):
    """Create test data for cars"""

    async with test_db.begin():
        # Create a car model
        car_model = CarModel(name="Test Model", make="Test Make", year=2024, color="Red", price=50000.00)
        test_db.add(car_model)

        await test_db.flush()

        # Create a car
        car = Car(vin="VIN-123", model_id=car_model.id, owner="Test Owner")
        test_db.add(car)

        await test_db.commit()


@pytest.mark.asyncio
async def test_list_cars(client: AsyncClient, create_test_data):
    """Test listing cars API endpoint"""

    response = await client.get("/api/cars/")
    assert response.status_code == 200

    actual = response.json()

    results = actual["results"]
    assert len(results) == 1
    assert results[0]["vin"] == "VIN-123"
    assert results[0]["car_model_name"] == "Test Model"
    assert results[0]["owner"] == "Test Owner"
    assert results[0]["car_model_year"] == 2024
    assert results[0]["color"] == "Red"


@pytest.mark.asyncio
async def test_list_cars_empty(client: AsyncClient):
    """Test listing cars when no data exists"""

    response = await client.get("/api/cars/")
    assert response.status_code == 200

    actual = response.json()
    results = actual["results"]
    assert len(results) == 0
