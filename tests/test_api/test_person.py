from app.crud.person import CRUDPerson
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonCheck
from datetime import datetime

def test_init_db_success(test_db):
    mock_people = [
        Person(
            identification="12345",
            firstname="John",
            lastname="Doe",
            birthday="1990-01-01"
        ),
        Person(
            identification="67890",
            firstname="Harry",
            lastname="Doe",
            birthday="1990-01-01"
        ),
        Person(
            identification="54321",
            firstname="Jenny",
            lastname="Doe",
            birthday="1985-03-03"
        ),
        Person(
            identification="096382",
            firstname="Harry",
            lastname="Potter",
            birthday=None
        )
    ]

    test_db.add_all(mock_people)
    test_db.commit()

    db_people = test_db.query(Person).all()
    assert len(db_people) == 4

    assert db_people[0].identification == "12345"
    assert db_people[0].firstname == "John"
    assert db_people[1].identification == "67890"
    assert db_people[1].firstname == "Harry"
    assert db_people[2].identification == "54321"
    assert db_people[2].firstname == "Jenny"
    assert db_people[3].identification == "096382"
    assert db_people[3].firstname == "Harry"

def test_store_person_success(test_db):
    crud_person = CRUDPerson(Person)

    person_data = PersonCreate(
        identification="9318762",
        firstname="Andrew",
        lastname="Craw",
        birthday="1985-02-20"
    )

    person, error = crud_person.create(test_db, person_data)

    assert error is None
    assert person.identification == "9318762"
    assert person.firstname == "Andrew"
    assert person.lastname == "Craw"
    assert person.birthday == datetime(1985, 2, 20)

def test_check_person_initials_match_return_1_person_055(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="A.",
        lastname="Craw"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Andrew"
    assert persons[0]['lastname'] == "Craw"
    assert persons[0]['probability'] == 0.55

def test_check_person_typo_match_return_1_person_055(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="Andew",
        lastname="Craw"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Andrew"
    assert persons[0]['lastname'] == "Craw"
    assert persons[0]['probability'] == 0.55

def test_check_person_birthday_match_return_1_person_04(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="Petty",
        lastname="Smith",
        birthday="1985-02-20"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Andrew"
    assert persons[0]['lastname'] == "Craw"
    assert persons[0]['probability'] == 0.4

def test_check_person_initials_match_birthday_match_return_1_person_095(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="A.",
        lastname="Craw",
        birthday="1985-02-20"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Andrew"
    assert persons[0]['lastname'] == "Craw"
    assert persons[0]['probability'] == 0.95

def test_check_person_identification_match_return_1_person_1(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="Petty",
        lastname="Smith",
        birthday="1985-02-20",
        identification="93-18-762"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Andrew"
    assert persons[0]['lastname'] == "Craw"
    assert persons[0]['probability'] == 1

def test_check_person_name_match_birthday_match_return_1_person_1(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="andrew",
        lastname="craw",
        birthday="1985-02-20"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Andrew"
    assert persons[0]['lastname'] == "Craw"
    assert persons[0]['probability'] == 1

def test_check_person_diminutive_match_return_1_person_055(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="Andy",
        lastname="Craw"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Andrew"
    assert persons[0]['lastname'] == "Craw"
    assert persons[0]['probability'] == 0.55

def test_check_person_multiple_matches_return_2_persons_055(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="J.",
        lastname="Doe"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 2

    assert persons[0]['firstname'] == "Jenny"
    assert persons[0]['lastname'] == "Doe"
    assert persons[0]['probability'] == 0.55

    assert persons[1]['firstname'] == "John"
    assert persons[1]['lastname'] == "Doe"
    assert persons[1]['probability'] == 0.55

def test_check_person_initials_match_birthday_not_match_return_0_person(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="J.",
        lastname="Doe",
        birthday="1985-03-08"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is not None

    persons = result['matches']

    assert len(persons) == 0

def test_check_person_identification_match_birthday_not_match_return_1_person_1(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="J.",
        lastname="Doe",
        birthday="1985-03-08",
        identification="12345"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "John"
    assert persons[0]['lastname'] == "Doe"
    assert persons[0]['probability'] == 1

def test_check_person_non_birthday_return_1_person_06(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="Harry",
        lastname="Potter"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 1

    assert persons[0]['firstname'] == "Harry"
    assert persons[0]['lastname'] == "Potter"
    assert persons[0]['probability'] == 0.6

def test_check_person_birthday_or_lastname_match_return_1_person_06(test_db):
    crud_person = CRUDPerson(Person)

    person_check = PersonCheck(
        firstname="Harry",
        lastname="Potter",
        birthday="1990-01-01"
    )

    result, error = crud_person.get_persons_with_highest_probability(person_check, test_db)

    assert error is None

    persons = result['matches']

    assert len(persons) == 2

    assert persons[0]['firstname'] == "Harry"
    assert persons[0]['lastname'] == "Potter"
    assert persons[0]['probability'] == 0.6

    assert persons[1]['firstname'] == "Harry"
    assert persons[1]['lastname'] == "Doe"
    assert persons[1]['probability'] == 0.6