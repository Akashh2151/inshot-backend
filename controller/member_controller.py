from flask import Blueprint, jsonify, request
from model.postCreation_model import Post

from model.signInsignup_model import User
member=Blueprint('member',__name__)


@member.route('/v1/category', methods=['GET'])
def get_posts_by_user_categories():
    try:
        user_id = request.headers.get('userId')

        if not user_id:
            response = {'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}
            return jsonify(response), 200

        user = User.objects(id=user_id).first()
        if not user:
            response = {'body': {}, 'message': 'The user ID entered does not correspond to an active user', 'status': 'error', 'statusCode': 404}
            return jsonify(response), 200

        # Assuming user has a field named categories which contains a list of categories
       # user_categories = user.categories

        # Query posts by categories that the user is interested in
        posts = Post.objects.filter(creator=user)

        # Serialize posts data
        posts_data = [{
            # 'title': post.title,
            # 'summary': post.summary,
            # 'post': post.post,
            'category': post.category,
            # 'subcategory': post.subcategory,
            # 'creator': post.creator.name  # Assuming creator has a username field
        } for post in posts]

        response = {'body': posts_data, 'message': f'All categories retrieved successfully', 'status': 'success', 'statusCode': 200}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500
    


@member.route('/v1/subcategory', methods=['GET'])
def get_posts_by_subcategory():
    try:
        category = request.args.get('category') 
        
        # Query posts by subcategory
        posts = Post.objects.filter(category=category)
        
        # Serialize posts data
        posts_data = []
        for post in posts:
            post_dict = {
                'subcategory': post.subcategory,
            }
            posts_data.append(post_dict)

        response = {'body': posts_data, 'message': f'Posts found for subcategory: {category}', 'status': 'success', 'statusCode': 200}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500