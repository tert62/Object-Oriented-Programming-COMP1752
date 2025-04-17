import pytest
from library_item import LibraryItem, LibraryItemAlbum

@pytest.fixture
def sample_item():
    return LibraryItem(1, "Sample Track", "Sample Artist", 3)

@pytest.fixture
def sample_album_item():
    return LibraryItemAlbum(
        2, "Album Track", "Album Artist", 4, 
        album="Sample Album", release_year=2020, 
        genre="Rock", track_number=1
    )

def test_create_library_item(sample_item):
    assert sample_item.track_id == 1
    assert sample_item.name == "Sample Track"
    assert sample_item.artist == "Sample Artist"
    assert sample_item.rating == 3
    assert sample_item.play_count == 0
    assert sample_item.image_path == ""

def test_create_library_item_album(sample_album_item):
    assert sample_album_item.track_id == 2
    assert sample_album_item.name == "Album Track"
    assert sample_album_item.artist == "Album Artist"
    assert sample_album_item.rating == 4
    assert sample_album_item.play_count == 0
    assert sample_album_item.album == "Sample Album"
    assert sample_album_item.release_year == 2020
    assert sample_album_item.genre == "Rock"
    assert sample_album_item.track_number == 1

def test_get_details(sample_item, sample_album_item):
    assert sample_item.get_details() == "1: Sample Track - Sample Artist (Rating: 3) [Played: 0 times]"
    assert sample_album_item.get_details() == (
        "2: Album Track - Album Artist (Album: Sample Album, Track 1) "
        "(Rating: 4) [Played: 0 times]"
    )

def test_get_album_info(sample_album_item):
    assert sample_album_item.get_album_info() == (
        "Album: Sample Album, Released: 2020, Genre: Rock"
    )

def test_set_rating_valid(sample_item):
    sample_item.set_rating(5)
    assert sample_item.rating == 5

def test_set_rating_invalid_string(sample_item):
    with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
        sample_item.set_rating("four")

def test_set_rating_out_of_range(sample_item):
    with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
        sample_item.set_rating(6)

def test_set_rating_negative(sample_item):
    with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
        sample_item.set_rating(-1)

def test_increment_play_count(sample_item):
    assert sample_item.play_count == 0
    sample_item.increment_play_count()
    assert sample_item.play_count == 1
    sample_item.increment_play_count()
    assert sample_item.play_count == 2

def test_image_path(sample_item):
    sample_item.image_path = "path/to/image.jpg"
    assert sample_item.image_path == "path/to/image.jpg"


    