from elasticsearch_dsl import Document, Text, Keyword, Integer, connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class VideoDocument(Document):
    title = Text()
    description = Text()
    video_url = Keyword()
    image_url = Keyword()
    subtitle = Text()
    content_type = Keyword()
    release_year = Integer()
    actors = Keyword()
    director = Keyword()
    genre = Keyword()
    awards = Keyword()

    class Index:
        name = 'videos'

    def save(self, **kwargs):
        return super().save(**kwargs)

# Initialize the index
VideoDocument.init()
