from django.db.models.signals import post_migrate
from django.dispatch import receiver
from elasticsearchs.models import Actor, Director, Genre, Award, MediaContent


@receiver(post_migrate)
def populate_data(sender, **kwargs):
    if sender.name == 'elasticsearchs':  # Replace 'yourapp' with your actual app name
        # Actors
        actors = [
            "Robert Downey Jr.", "Chris Evans", "Scarlett Johansson", "Mark Ruffalo", "Chris Hemsworth",
            "Tom Holland", "Leonardo DiCaprio", "Brad Pitt", "Margot Robbie", "Christian Bale",
            "Tom Hanks", "Matt Damon", "Joaquin Phoenix", "Gal Gadot", "Henry Cavill",
            "Amy Adams", "Dwayne Johnson", "Vin Diesel", "Paul Walker", "Natalie Portman",
            "Ryan Reynolds", "Hugh Jackman", "Jennifer Lawrence", "Anne Hathaway", "Emma Stone",
            "Ryan Gosling", "Keanu Reeves", "Sandra Bullock", "Will Smith", "Charlize Theron"
        ]

        for actor_name in actors:
            Actor.objects.get_or_create(name=actor_name)

        # Directors
        directors = [
            "Christopher Nolan", "Steven Spielberg", "Quentin Tarantino", "Martin Scorsese", "James Cameron",
            "Joss Whedon", "Taika Waititi", "David Fincher", "Ridley Scott", "Denis Villeneuve",
            "Tim Burton", "Patty Jenkins", "Zack Snyder", "James Wan", "Peter Jackson"
        ]

        for director_name in directors:
            Director.objects.get_or_create(name=director_name)

        # Genres
        genres = [
            "Action", "Adventure", "Comedy", "Drama", "Thriller", "Sci-Fi",
            "Fantasy", "Mystery", "Horror", "Romance"
        ]

        for genre_name in genres:
            Genre.objects.get_or_create(name=genre_name)

        # Awards
        awards = [
            "Oscar", "Golden Globe", "BAFTA", "Cannes Palm d'Or", "Emmy",
            "Screen Actors Guild", "Critics' Choice", "People’s Choice", "MTV Movie Award", "Independent Spirit Award"
        ]

        for award_name in awards:
            Award.objects.get_or_create(name=award_name)

        # Movies (Example data, add more movies similarly)
        movies = [
            {
                "title": "Avengers: Endgame",
                "description": "The Avengers take a final stand against Thanos in Marvel Studios' conclusion to twenty-two films.",
                "video_url": "https://www.youtube.com/watch?v=TcMBFSGVi1c",
                "image_url": "https://example.com/endgame.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2019,
                "actors": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson", "Mark Ruffalo", "Chris Hemsworth"],
                "director": "Anthony Russo, Joe Russo",
                "genre": "Action, Sci-Fi",
                "awards": ["Oscar", "People’s Choice"]
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
                "video_url": "https://www.youtube.com/watch?v=YoHD9XEInc0",
                "image_url": "https://example.com/inception.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2010,
                "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
                "director": "Christopher Nolan",
                "genre": "Action, Sci-Fi",
                "awards": ["Oscar", "BAFTA"]
            },
            {
                "title": "Interstellar",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "video_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E",
                "image_url": "https://example.com/interstellar.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2014,
                "actors": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
                "director": "Christopher Nolan",
                "genre": "Sci-Fi",
                "awards": ["Oscar", "BAFTA"]
            },
            {
                "title": "The Godfather",
                "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "video_url": "https://www.youtube.com/watch?v=sY1S34973zA",
                "image_url": "https://example.com/godfather.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1972,
                "actors": ["Marlon Brando", "Al Pacino", "James Caan"],
                "director": "Francis Ford Coppola",
                "genre": "Crime",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "Pulp Fiction",
                "description": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                "video_url": "https://www.youtube.com/watch?v=s7EdQ4FqbhY",
                "image_url": "https://example.com/pulpfiction.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1994,
                "actors": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
                "director": "Quentin Tarantino",
                "genre": "Crime",
                "awards": ["Cannes Palm d'Or", "Oscar"]
            },
            {
                "title": "The Matrix",
                "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
                "video_url": "https://www.youtube.com/watch?v=vKQi3bBA1y8",
                "image_url": "https://example.com/matrix.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1999,
                "actors": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
                "director": "Lana Wachowski, Lilly Wachowski",
                "genre": "Sci-Fi",
                "awards": ["Oscar", "BAFTA"]
            },
            {
                "title": "Gladiator",
                "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
                "video_url": "https://www.youtube.com/watch?v=owK1qxDselE",
                "image_url": "https://example.com/gladiator.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2000,
                "actors": ["Russell Crowe", "Joaquin Phoenix", "Connie Nielsen"],
                "director": "Ridley Scott",
                "genre": "Action",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "Wonder Woman",
                "description": "When an Amazon princess comes to the world of Man in the grips of the First World War, she discovers her full powers and true destiny.",
                "video_url": "https://www.youtube.com/watch?v=VSB4wGIdDwo",
                "image_url": "https://example.com/wonderwoman.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2017,
                "actors": ["Gal Gadot", "Chris Pine", "Robin Wright"],
                "director": "Patty Jenkins",
                "genre": "Action",
                "awards": ["Critics' Choice"]
            },
            {
                "title": "Mad Max: Fury Road",
                "description": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search of her homeland with the aid of a group of female prisoners, a psychotic worshipper, and a drifter named Max.",
                "video_url": "https://www.youtube.com/watch?v=hEJnMQG9ev8",
                "image_url": "https://example.com/madmax.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2015,
                "actors": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"],
                "director": "George Miller",
                "genre": "Action",
                "awards": ["Oscar", "BAFTA"]
            },
            {
                "title": "La La Land",
                "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
                "video_url": "https://www.youtube.com/watch?v=0pdqf4P9MB8",
                "image_url": "https://example.com/lalaland.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2016,
                "actors": ["Ryan Gosling", "Emma Stone", "Rosemarie DeWitt"],
                "director": "Damien Chazelle",
                "genre": "Comedy",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "The Shawshank Redemption",
                "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "video_url": "https://www.youtube.com/watch?v=6hB3S9bIaco",
                "image_url": "https://example.com/shawshank.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1994,
                "actors": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
                "director": "Frank Darabont",
                "genre": "Drama",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "Black Panther",
                "description": "T'Challa, the King of Wakanda, rises to the throne in the isolated, technologically advanced African nation, but his claim is challenged by a vengeful outsider.",
                "video_url": "https://www.youtube.com/watch?v=xjDjIWPwcPU",
                "image_url": "https://example.com/blackpanther.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2018,
                "actors": ["Chadwick Boseman", "Michael B. Jordan", "Lupita Nyong'o"],
                "director": "Ryan Coogler",
                "genre": "Action",
                "awards": ["Oscar", "Screen Actors Guild"]
            },
            {
                "title": "Guardians of the Galaxy",
                "description": "A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.",
                "video_url": "https://www.youtube.com/watch?v=d96cjJhvlMA",
                "image_url": "https://example.com/guardians.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2014,
                "actors": ["Chris Pratt", "Vin Diesel", "Bradley Cooper"],
                "director": "James Gunn",
                "genre": "Action",
                "awards": ["Critics' Choice"]
            },
            {
                "title": "Deadpool",
                "description": "A wisecracking mercenary gets experimented on and becomes immortal but ugly, and sets out to track down the man who ruined his looks.",
                "video_url": "https://www.youtube.com/watch?v=ONHBaC-pfsk",
                "image_url": "https://example.com/deadpool.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2016,
                "actors": ["Ryan Reynolds", "Morena Baccarin", "T.J. Miller"],
                "director": "Tim Miller",
                "genre": "Action",
                "awards": ["Golden Globe", "Critics' Choice"]
            },
            {
                "title": "The Social Network",
                "description": "The story of the founders of the social-networking website, Facebook.",
                "video_url": "https://www.youtube.com/watch?v=lB95KLmpLR4",
                "image_url": "https://example.com/socialnetwork.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2010,
                "actors": ["Jesse Eisenberg", "Andrew Garfield", "Justin Timberlake"],
                "director": "David Fincher",
                "genre": "Drama",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "Fight Club",
                "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
                "video_url": "https://www.youtube.com/watch?v=SUXWAEX2jlg",
                "image_url": "https://example.com/fightclub.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1999,
                "actors": ["Brad Pitt", "Edward Norton", "Meat Loaf"],
                "director": "David Fincher",
                "genre": "Drama",
                "awards": ["MTV Movie Award"]
            },
            {
                "title": "Titanic",
                "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
                "video_url": "https://www.youtube.com/watch?v=2e-eXJ6HgkQ",
                "image_url": "https://example.com/titanic.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1997,
                "actors": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane"],
                "director": "James Cameron",
                "genre": "Romance",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
                "video_url": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
                "image_url": "https://example.com/darkknight.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2008,
                "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
                "director": "Christopher Nolan",
                "genre": "Action",
                "awards": ["Oscar", "BAFTA"]
            },
            {
                "title": "Forrest Gump",
                "description": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
                "video_url": "https://www.youtube.com/watch?v=bLvqoHBptjg",
                "image_url": "https://example.com/forrestgump.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1994,
                "actors": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
                "director": "Robert Zemeckis",
                "genre": "Drama",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "Star Wars: Episode IV - A New Hope",
                "description": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee, and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader.",
                "video_url": "https://www.youtube.com/watch?v=vZ734NWnAHA",
                "image_url": "https://example.com/starwars.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1977,
                "actors": ["Mark Hamill", "Harrison Ford", "Carrie Fisher"],
                "director": "George Lucas",
                "genre": "Action",
                "awards": ["Oscar"]
            },
            {
                "title": "The Lion King",
                "description": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
                "video_url": "https://www.youtube.com/watch?v=4sj1MT05lAA",
                "image_url": "https://example.com/lionking.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1994,
                "actors": ["Matthew Broderick", "Jeremy Irons", "James Earl Jones"],
                "director": "Roger Allers, Rob Minkoff",
                "genre": "Animation",
                "awards": ["Oscar", "Golden Globe"]
            },
            {
                "title": "The Terminator",
                "description": "A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine, sent from the same year, which has been programmed to execute a young woman whose unborn son is the key to humanity's future salvation.",
                "video_url": "https://www.youtube.com/watch?v=k64P4l2Wmeg",
                "image_url": "https://example.com/terminator.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 1984,
                "actors": ["Arnold Schwarzenegger", "Linda Hamilton", "Michael Biehn"],
                "director": "James Cameron",
                "genre": "Sci-Fi",
                "awards": ["Saturn Award"]
            },
            {
                "title": "The Wolf of Wall Street",
                "description": "Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption, and the federal government.",
                "video_url": "https://www.youtube.com/watch?v=iszwuX1AK6A",
                "image_url": "https://example.com/wolfofwallstreet.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.MOVIE,
                "release_year": 2013,
                "actors": ["Leonardo DiCaprio", "Jonah Hill", "Margot Robbie"],
                "director": "Martin Scorsese",
                "genre": "Biography",
                "awards": ["Golden Globe"],
            },
            {
                "title": "Breaking Bad",
                "description": "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family's future.",
                "video_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
                "image_url": "https://example.com/breakingbad.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.TV_SHOW,
                "release_year": 2008,
                "actors": ["Bryan Cranston", "Aaron Paul", "Anna Gunn"],
                "director": "Vince Gilligan",
                "genre": "Crime, Drama",
                "awards": ["Golden Globe"]
            },
            {
                "title": "Stranger Things",
                "description": "When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.",
                "video_url": "https://www.youtube.com/watch?v=XWxyRG_tckY",
                "image_url": "https://example.com/strangerthings.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.TV_SHOW,
                "release_year": 2016,
                "actors": ["Millie Bobby Brown", "Finn Wolfhard", "Winona Ryder"],
                "director": "The Duffer Brothers",
                "genre": "Drama, Fantasy",
                "awards": ["Screen Actors Guild"]
            },
            {
                "title": "Planet Earth",
                "description": "David Attenborough narrates a documentary series on the natural history of the planet.",
                "video_url": "https://www.youtube.com/watch?v=KbyNSbCCgws",
                "image_url": "https://example.com/planetearth.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.DOCUMENTARY,
                "release_year": 2006,
                "actors": ["David Attenborough"],
                "director": "Alastair Fothergill",
                "genre": "Nature, Documentary",
                "awards": ["Emmy", "BAFTA"]
            },
            {
                "title": "Cosmos: A Spacetime Odyssey",
                "description": "An exploration of our discovery of the laws of nature and coordinates in space and time.",
                "video_url": "https://www.youtube.com/watch?v=XKx4Ck0IY3c",
                "image_url": "https://example.com/cosmos.jpg",
                "subtitle": "English",
                "content_type": MediaContent.ContentType.DOCUMENTARY,
                "release_year": 2014,
                "actors": ["Neil deGrasse Tyson"],
                "director": "Ann Druyan, Brannon Braga",
                "genre": "Science, Documentary",
                "awards": ["Emmy"]
            },
        ]

        for movie in movies:
            director, _ = Director.objects.get_or_create(name=movie["director"])
            genre, _ = Genre.objects.get_or_create(name=movie["genre"].split(", ")[0])
            award = None
            if movie["awards"]:
                award, _ = Award.objects.get_or_create(name=movie["awards"][0])

            media_content, created = MediaContent.objects.get_or_create(
                title=movie["title"],
                description=movie["description"],
                video_url=movie["video_url"],
                image_url=movie["image_url"],
                subtitle=movie["subtitle"],
                content_type=movie["content_type"],
                release_year=movie["release_year"],
                director=director,
                genre=genre,
                awards=award
            )
            if created:
                for actor_name in movie["actors"]:
                    actor, _ = Actor.objects.get_or_create(name=actor_name)
                    media_content.actors.add(actor)
                media_content.save()

#
# ### `apps.py`
# Connect
# the
# signal in the
# `apps.py`
# file:
#
# ```python
# from django.apps import AppConfig
#
#
# class YourAppConfig(AppConfig):
#     name = 'yourapp'
#
#     def ready(self):
#         import yourapp.signals  # Import the signals module
