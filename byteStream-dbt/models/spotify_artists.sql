with raw_artists as (
    select
        artist_id,
        artist_name,
        followers,
        genres,
        images,
        popularity
    from {{ source('spotify_data', 'spotify_artists_data') }}
)

select
    artist_id,
    artist_name,
    followers,
    genres,
    images,
    popularity
from raw_artists
