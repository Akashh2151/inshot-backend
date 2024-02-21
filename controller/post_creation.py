from flask import Blueprint, jsonify,request
from model.signInsignup_model import User
from model.postCreation_model import   Comment, Post 

postcreation=Blueprint('postcreation',__name__)


@postcreation.route('/v1/createpost', methods=['POST'])
def create_post():
    try:
        data = request.json
        user_id = request.headers.get('userId')     

        if not user_id:
            response = {'body': {},'message': 'UserID header is missing','status': 'error','statuscode': 400}
            return jsonify(response), 200   
        
        user = User.objects(id=user_id).first()     

        if not user:
            response = {'body': {},'message': 'The user ID entered does not correspond to an active user','status': 'error','statuscode': 404}
            return jsonify(response), 200                      
      
        post = Post(
            title=data.get('title'),
            summary=data.get('summary'),
            post=data.get('post'),
            category=data.get('category'),
            subcategory=data.get('subcategory'),
            creator=user,
        )
        post.save()
        return jsonify({'body': data,'message': 'Post created successfully','postid': str(post.id),'status':'success',
                'statuscode': 200}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@postcreation.route('/v1/posts/<post_id>', methods=['GET'])
def view_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        post_data = {
            'title': post.title,
            'summary': post.summary,
            'post': post.post,
            'category': post.category,
            'subcategory': post.subcategory,
            'likes': post.likes,  
            'dislikes': post.dislikes,
            'shares': post.shares,
 
        }
        
        response = {'body': post_data,'message': 'Post retrieved successfully','status': 'success','statuscode': 200}
        return jsonify(response), 200
    
    except Post.DoesNotExist:
        response = {'body': {},'message': 'Post not found','status': 'error','statuscode': 404}
        return jsonify(response), 404



@postcreation.route('/v1/posts', methods=['GET'])
def get_user_posts():
    user_id = request.headers.get('userId')
    
    if not user_id:
        return jsonify({'body': {},'message': 'UserID header is missing', 'status': 'error', 'statuscode': 400}), 200
    
    try:
        # Ensure the user exists
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {},'message': 'User not found','status': 'error', 'statuscode': 500}), 404
    
    try:
        # Fetch posts created by the specified user
        user_posts = Post.objects(creator=user)
        posts_data = []
        
        for post in user_posts:
            post_data = {
                'id': str(post.id),
                'title': post.title,
                'summary': post.summary,
                'post': post.post,
                'category': post.category,
                'subcategory': post.subcategory,
                'likes': post.likes,
                'dislikes': post.dislikes,
                'shares': post.shares,
                # 'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Uncomment if created_at is included
            }
            posts_data.append(post_data)
        
        return jsonify({'body': posts_data, 'message': 'User posts fetched successfully', 'status': 'success', 'statuscode': 200}), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statuscode': 500}), 500




@postcreation.route('/v1/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.update(inc__likes=1)
        post.reload()
        return jsonify({'body': {'likes': post.likes}, 'message': 'Like added successfully', 'status': 'success', 'statuscode': 200}), 200
    except Post.DoesNotExist:
        return jsonify({'body': {}, 'message': 'Post not found', 'status': 'error', 'statuscode': 404}), 404

    

@postcreation.route('/v1/posts/<post_id>/dislike', methods=['POST'])
def dislike_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.update(inc__dislikes=1)
        post.reload()
        return jsonify({'body': {'dislikes': post.dislikes}, 'message': 'Dislike added successfully', 'status': 'success', 'statuscode': 200}), 200
    except Post.DoesNotExist:
        return jsonify({'body': {}, 'message': 'Post not found', 'status': 'error', 'statuscode': 404}), 404


@postcreation.route('/v1/posts/<post_id>/share', methods=['POST'])
def share_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.update(inc__shares=1)
        post.reload()
        return jsonify({'body': {'shares': post.shares}, 'message': 'Post shared successfully', 'status': 'success', 'statuscode': 200}), 200
    except Post.DoesNotExist:
        return jsonify({'body': {}, 'message': 'Post not found', 'status': 'error', 'statuscode': 404}), 404


@postcreation.route('/v1/posts/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    try:
        user_id = request.headers.get('userId')
        if not user_id:
            return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statuscode': 400}), 400
        user = User.objects.get(id=user_id)
        data = request.json
        comment_content = data.get('comment')
        if not comment_content:
            return jsonify({'body': {}, 'message': 'Comment content is missing', 'status': 'error', 'statuscode': 400}), 400

        post = Post.objects.get(id=post_id)
        comment = Comment(post=post, author=user, content=comment_content)
        comment.save()
        return jsonify({'body': {}, 'message': 'Comment added successfully', 'status': 'success', 'statuscode': 201}), 201
    except (Post.DoesNotExist, User.DoesNotExist):
        return jsonify({'body': {}, 'message': 'Post or User not found', 'status': 'error', 'statuscode': 404}), 404
    except Exception as e:
        return jsonify({'body': {}, 'message': str(e), 'status': 'error', 'statuscode': 500}), 500
 