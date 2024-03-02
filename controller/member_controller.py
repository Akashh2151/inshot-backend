from flask import Blueprint, jsonify, request
from model.postCreation_model import Post

from model.signInsignup_model import User
member=Blueprint('member',__name__)



@app.route('/v1/category', methods=['GET'])
def get_posts_by_user_categories():
    try:
        # Assuming you don't need user authentication for this endpoint
        
        # Query all posts regardless of user
        posts = Post.objects.all()

        # Serialize posts data
        posts_data = [{
            'category': post.category,
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