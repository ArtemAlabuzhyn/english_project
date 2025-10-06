import pytest

from english_course.models import Word, UserWord


@pytest.mark.django_db
def test_word_created(authorized_client):
    client, user = authorized_client

    data = {
        "word_text": "test",
        "translation": "тест"
    }

    response = client.post('/api/drf/words/', data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_words_list(authorized_client):

    client, user = authorized_client

    word1 = Word.objects.create(word="Apple")
    word2 = Word.objects.create(word="Banana")

    UserWord.objects.create(user=user, word=word1, translation="Яблоко")
    UserWord.objects.create(user=user, word=word2, translation="Банан")
    response = client.get('/api/drf/words/')
    assert response.status_code == 200

    data = response.data['results']
    assert isinstance(data, list)
    assert len(data) == 2

    returned_words = {entry['word'] for entry in data}

    assert 'Apple' in returned_words
    assert 'Banana' in returned_words

    returned_translation = {entry['translation'] for entry in data}

    assert 'Яблоко' in returned_translation
    assert 'Банан' in returned_translation

    assert data[0]['word'] == 'Banana'
    assert data[1]['word'] == 'Apple'
