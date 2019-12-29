from zimmerman.main import db

from ..like_service import check_like
from ..user.utils import filter_author

# Import Schemas
from zimmerman.main.model.schemas import CommentSchema, UserSchema

# Define deserializers
comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()
user_schema = UserSchema()


def update_comment(comment, content):
    comment.content = content
    comment.edited = True

    db.session.commit()


def delete_comment(comment):
    db.session.delete(comment)
    db.session.commit()


def add_comment_and_flush(data, user_id):
    db.session.add(data)
    db.session.flush()

    latest_comment = load_comment(data, user_id)

    db.session.commit()

    return latest_comment


def load_comment(comment, user_id):
    info = comment_schema.dump(comment)

    # Set the author
    author = user_schema.dump(comment.author)
    info["author"] = filter_author(author)

    # Return boolean
    info["liked"] = check_like(comment.likes, user_id)

    # Get the frst 2 replies if there are any.
    info["initial_replies"] = (
        # TODO
    )

    # Filter comment

    return info