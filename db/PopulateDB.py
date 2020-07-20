from database import session, engine
from models import *
from datetime import datetime

feedback = Feedback(
    date = datetime.strptime('2020-07-20', '%Y-%m-%d'),
    full_name = 'Ido Nov',
    content = 'test feedback, The you can see feedbacks! thats great'
)

# models.Base.metadata.create_all(bind=engine)
session.add(feedback)
session.commit()