from sqlalchemy.orm import Session
from sqlalchemy import func, and_, select, case, or_
from app.crud.base import CRUDBase
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate, PersonCheck

class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    def get_persons_with_highest_probability(self, person: PersonCheck, db: Session):
        print(person)

        try:
            match_probability_subquery = (
                db.query(
                    Person.id,
                    Person.identification,
                    Person.firstname,
                    Person.lastname,
                    Person.birthday,
                    func.sum(
                        case((
                            and_(
                                person.identification is not None,
                                person.identification != "unknown",
                                func.regexp_replace(Person.identification, '[^a-zA-Z0-9]', '', 'g') == func.regexp_replace(person.identification, '[^a-zA-Z0-9]', '', 'g')
                            ), 200
                        ), else_=0) +
                        case((Person.lastname.ilike(f"%{person.lastname}%"), 40), else_=0) +
                        case((Person.firstname.ilike(f"%{person.firstname}%"), 20), else_=0) +
                        case((
                            and_(
                                Person.firstname.ilike(f"%{person.firstname}%") == False,
                                or_(
                                    func.levenshtein(func.lower(Person.firstname), func.lower(person.firstname)) <= 1, # Check typo
                                    func.substr(Person.firstname, 1, 1) == func.substr(person.firstname, 1, 1), # Check initials
                                    func.similarity(func.lower(Person.firstname), func.lower(person.firstname)) > 0.5 # Check diminutive
                                )
                            ), 15
                        ), else_=0) +
                        case((and_(
                            person.birthday is not None,
                            Person.birthday.isnot(None),
                            Person.birthday != person.birthday), -100
                        ), else_=0) +
                        case((and_(
                            person.birthday is not None,
                            Person.birthday.isnot(None),
                            Person.birthday == person.birthday), 40
                        ), else_=0)
                    ).label("match_probability")
                )
                .group_by(
                    Person.id,
                    Person.identification,
                    Person.firstname,
                    Person.lastname,
                    Person.birthday
                )
                .subquery()
            )

            max_match_probability_query = select(func.max(match_probability_subquery.c.match_probability))
            max_match_probability = db.execute(max_match_probability_query).scalar()

            if max_match_probability <= 0:
                raise Exception("Match probability is zero, no valid data found.")

            if max_match_probability > 100:
                query = (
                    db.query(match_probability_subquery)
                    .filter(match_probability_subquery.c.match_probability > 100)
                    .order_by(match_probability_subquery.c.firstname)
                )
            else:
                query = (
                    db.query(match_probability_subquery)
                        .filter(match_probability_subquery.c.match_probability > 0)
                        .filter(match_probability_subquery.c.match_probability == max_match_probability)
                    .order_by(match_probability_subquery.c.firstname)
                )

            persons = query.all()

            res = []
            for p in persons:
                res.append({
                    "identification": p[1],
                    "firstname": p[2],
                    "lastname": p[3],
                    "birthday": p[4],
                    "probability": min(max(p[5], 0), 100) / 100
                })
            

            return ({ "matches": res }, None)
        
        except Exception as e:
            db.rollback()
            return ({ "matches": [] }, e)
        
    
    def create(self, db: Session, person: PersonCreate):
        try:
            db_person = Person(
                firstname=person.firstname,
                lastname=person.lastname,
                birthday=person.birthday,
                identification=person.identification,
            )
            db.add(db_person)
            db.commit()
            db.refresh(db_person)
            return (db_person, None)

        except Exception as e:
            db.rollback()
            return (None, e)

person = CRUDPerson(Person)