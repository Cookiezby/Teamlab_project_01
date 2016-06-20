from app import models,db


class PostService(object):
    @staticmethod
    def get_user_followed_post(user_id,page,per_page):
        follows = models.Follow.query.filter_by(follow_id=user_id).all()
        posts = models.Post.query.order_by(models.Post.id.desc()).all()
        follow_posts = []
        for post in posts:
            if post.user_id == user_id:
                follow_posts.append(post)
            for follow in follows:
                if follow.followed_id == post.user_id:
                    follow_posts.append(post)
                else:
                    pass

        start = (page-1)*per_page;
        return follow_posts[start:start+per_page]

    @staticmethod
    def get_all_posts():
        posts = models.Post.query.order_by(models.Post.id.desc()).all()
        return posts

    @staticmethod
    def add_post(user_id, body, date):
        print user_id
        print body
        print date
        post = models.Post(user_id=user_id, body=body, timestamp=date)
        db.session.add(post)
        db.session.commit()
        return post





