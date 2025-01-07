import unittest
from app.main import app
from app.models import User, MeetingRoom, Booking
from app.utils.database import Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.utils.hashing import Hasher
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.environ.get("DATABASE_URL")


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URL
        app.config['TESTING'] = True

        self.engine = create_engine(TEST_DATABASE_URL)
        self.TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        Base.metadata.create_all(bind=self.engine)

        self.app = app
        self.client = self.app.test_client()
        self.db: Session = self.TestingSessionLocal()

    def tearDown(self):
        self.db.rollback()

        self.db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        self.db.execute(text("TRUNCATE TABLE bookings"))
        self.db.execute(text("TRUNCATE TABLE users"))
        self.db.execute(text("TRUNCATE TABLE meeting_rooms"))

        self.db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        self.db.commit()
        self.db.close()

    def test_database_connection(self):
        try:
            connection = self.engine.connect()
            connection.close()
            self.assertTrue(True)  # Connection successful
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_create_user(self):
        existing_user = self.db.query(User).filter_by(
            username="testuser").first()
        if existing_user is None:
            test_user = User(
                username="testuser",
                password=Hasher.get_password_hash("password"),
                is_admin=False,
            )
            self.db.add(test_user)
            self.db.commit()

        retrieved_user = self.db.query(User).filter_by(
            username="testuser").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")

    def test_create_room(self):
        existing_room = self.db.query(
            MeetingRoom).filter_by(name="Test Room").first()
        if existing_room is None:
            test_room = MeetingRoom(
                name="Test Room",
                capacity=10,
                description="Test Room Description"
            )
            self.db.add(test_room)
            self.db.commit()

        retrieved_room = self.db.query(
            MeetingRoom).filter_by(name="Test Room").first()
        self.assertIsNotNone(retrieved_room)
        self.assertEqual(retrieved_room.name, "Test Room")

    def test_create_booking(self):
        test_user = self.db.query(User).filter_by(username="testuser").first()
        if test_user is None:
            test_user = User(username="testuser",
                             password=Hasher.get_password_hash("password"))
            self.db.add(test_user)

        test_room = self.db.query(MeetingRoom).filter_by(
            name="Test Room").first()
        if test_room is None:
            test_room = MeetingRoom(name="Test Room", capacity=10)
            self.db.add(test_room)

        self.db.commit()

        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        test_booking = Booking(
            user_id=test_user.id,
            room_id=test_room.id,
            start_time=start_time,
            end_time=end_time,
        )
        self.db.add(test_booking)
        self.db.commit()

        retrieved_booking = self.db.query(Booking).filter_by(
            user_id=test_user.id, room_id=test_room.id
        ).first()
        self.assertIsNotNone(retrieved_booking)
        self.assertEqual(retrieved_booking.user_id, test_user.id)
        self.assertEqual(retrieved_booking.room_id, test_room.id)


if __name__ == "__main__":
    unittest.main()
