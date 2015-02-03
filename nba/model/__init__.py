from sqlalchemy.orm import sessionmaker


def create_engine(location):
    pass


def create_session(engine=None):
    if engine is None:
        engine = create_engine()
    return sessionmaker(bind=engine)
