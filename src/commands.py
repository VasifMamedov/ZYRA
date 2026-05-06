from flask.cli import with_appcontext
from datetime import datetime
import click


from src.models import Product, IDCard, Person, University, Student, Actor, Movie, ActorMovie, User
from src.ext import db


products = [
    {"id":0, "name":"s25", "price":100, "img":"s25.jpg" },
    {"id":1, "name":"iphone17", "price":200, "img":"iphone17.jpg" },
]



def init_db():

    click.echo("initializing dataBase")

    db.drop_all()
    db.create_all()

    click.echo("DataBase Created")





def populate_db():
    click.echo("Populating Database")

    admin = User(username = "admin", password = "123123123", role = "admin")
    admin.create()

    user = User(username = "user", password = "123123123", role = "user")
    user.create()

    for product in products:
        new_product = Product(name=product["name"], price=product["price"], img=product["img"])
        new_product.create(commit = False)

    db.session.commit()


    ### ONE TO ONE ###
    id_card = IDCard(personal_number="0102030405", serial_number="pjazdi23", expiration_date= datetime.now())
    id_card.create()

    person = Person(name="Nodo", surname= "Dora", birth_date = datetime.now() ,idcard_id=id_card.id)
    person.create()

    ### ONE TO MANY ###
    university = University(name = "Ilias State University", address = "Vake")
    university.create()

    university2 = University(name = "Javaxishvili State University", address = "Vake")
    db.session.add(university2)
    db.session.commit()

    student1 = Student(name = "Doto", university_id = university.id)
    student2 = Student(name = "Moto", university_id = university2.id)
    student3 = Student(name = "Toto", university_id = university2.id)
    db.session.add_all([student1, student2, student3])
    db.session.commit()

    ### MANY TO MANY ###
    actor = Actor(name= "Robert Downey JR")
    actor2 = Actor(name = "Chris Evans")

    movie1 = Movie(name= "Iron Man")
    movie2 = Movie(name = "Avengers")
    movie3 = Movie(name = "Captain Trashica")
    db.session.add_all([movie1, movie2, movie3])
    db.session.add_all([actor, actor2])
    db.session.commit()

    actormovie = ActorMovie(actor_id=actor.id, movie_id=movie1.id)
    actormovie2 = ActorMovie(actor_id=actor.id, movie_id=movie2.id)
    actormovie3 = ActorMovie(actor_id=actor2.id, movie_id=movie2.id)
    actormovie4 = ActorMovie(actor_id=actor2.id, movie_id=movie3.id)
    db.session.add_all([actormovie, actormovie2, actormovie3, actormovie4])
    db.session.commit()

    click.echo("DB Populated")



@click.command("init_db")
@with_appcontext
def init_db_command():
    init_db()


@click.command("populate_db")
@with_appcontext
def populate_db_command():
    populate_db()


