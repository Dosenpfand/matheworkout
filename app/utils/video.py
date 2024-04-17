from urllib.parse import parse_qs, urlparse


def video_embed_url(video_url):
    if not video_url:
        return None
    url = urlparse(video_url.strip())
    if url.hostname in ["www.youtube.com", "youtube.com", "youtu.be"]:
        queries = parse_qs(url.query)
        if url.hostname == "youtu.be":
            video_id = url.path[1:]
        else:
            if queries.get("v", False):
                video_id = queries["v"][0]
            else:
                return None
        if queries.get("t", False):
            start_at = queries["t"][0]
            if start_at.endswith("s"):
                start_at = start_at[:-1]
        else:
            start_at = 0

        video_embed_url = (
            f"https://www.youtube-nocookie.com/embed/{video_id}?start={start_at}"
        )
        return video_embed_url
    return None
