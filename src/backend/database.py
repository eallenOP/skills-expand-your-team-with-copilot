"""
MongoDB database configuration and setup for Mergington High School API
"""

from pymongo import MongoClient
from argon2 import PasswordHasher
import os

# Connect to MongoDB or use in-memory storage for development
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Test connection
    db = client['mergington_high']
    activities_collection = db['activities']
    teachers_collection = db['teachers']
    print("Connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using in-memory storage for development")
    
    # Simple in-memory storage
    class InMemoryCollection:
        def __init__(self):
            self.data = {}
        
        def count_documents(self, query=None):
            return len(self.data)
        
        def find_one(self, query):
            if isinstance(query, dict) and "_id" in query:
                return self.data.get(query["_id"])
            return None
        
        def insert_one(self, document):
            doc_id = document.get("_id")
            if doc_id:
                self.data[doc_id] = document
        
        def find(self, query=None):
            if query is None:
                return [{"_id": doc_id, **doc} for doc_id, doc in self.data.items()]
            
            result = []
            for doc_id, doc in self.data.items():
                if self._match_query({"_id": doc_id, **doc}, query):
                    result.append({"_id": doc_id, **doc})
            return result
        
        def update_one(self, query, update):
            class UpdateResult:
                def __init__(self, modified_count):
                    self.modified_count = modified_count
            
            if isinstance(query, dict) and "_id" in query:
                doc_id = query["_id"]
                if doc_id in self.data:
                    doc = self.data[doc_id]
                    if "$push" in update:
                        for key, value in update["$push"].items():
                            if key in doc:
                                doc[key].append(value)
                            else:
                                doc[key] = [value]
                    if "$pull" in update:
                        for key, value in update["$pull"].items():
                            if key in doc and isinstance(doc[key], list):
                                doc[key] = [x for x in doc[key] if x != value]
                    return UpdateResult(1)
            return UpdateResult(0)
        
        def aggregate(self, pipeline):
            # Simple aggregation for getting unique days
            if len(pipeline) >= 2 and "$unwind" in pipeline[0] and "$group" in pipeline[1]:
                days = set()
                for doc_id, doc in self.data.items():
                    if "schedule_details" in doc and "days" in doc["schedule_details"]:
                        for day in doc["schedule_details"]["days"]:
                            days.add(day)
                return [{"_id": day} for day in sorted(days)]
            return []
        
        def _match_query(self, doc, query):
            for key, value in query.items():
                if "." in key:
                    # Handle nested keys like "schedule_details.days"
                    parts = key.split(".")
                    current = doc
                    for part in parts:
                        if isinstance(current, dict) and part in current:
                            current = current[part]
                        else:
                            return False
                    
                    if isinstance(value, dict) and "$in" in value:
                        if not isinstance(current, list):
                            return False
                        if not any(item in current for item in value["$in"]):
                            return False
                    elif isinstance(value, dict) and "$gte" in value:
                        if current < value["$gte"]:
                            return False
                    elif isinstance(value, dict) and "$lte" in value:
                        if current > value["$lte"]:
                            return False
                    elif current != value:
                        return False
                else:
                    if key not in doc or doc[key] != value:
                        return False
            return True
    
    activities_collection = InMemoryCollection()
    teachers_collection = InMemoryCollection()

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    },
    "Manga Maniacs": {
        "description": "Dive into epic adventures and discover incredible worlds! Join fellow otaku as we explore legendary manga series, discuss your favorite heroes and villains, and uncover hidden gems in Japanese storytelling.",
        "schedule": "Tuesdays, 7:00 PM - 8:00 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:00"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]

