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



# @postcreation.route('/v1/posts', methods=['GET'])
# def get_user_posts():
#     user_id = request.headers.get('userId')
    
#     if not user_id:
#         return jsonify({'body': {},'message': 'UserID header is missing', 'status': 'error', 'statuscode': 400}), 200
    
#     try:
#         # Ensure the user exists
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return jsonify({'body': {},'message': 'User not found','status': 'error', 'statuscode': 500}), 404
    
#     try:
#         # Fetch posts created by the specified user
#         user_posts = Post.objects(creator=user)
#         posts_data = []
        
#         for post in user_posts:
#             post_data = {
#                 'id': str(post.id),
#                 'title': post.title,
#                 'summary': post.summary,
#                 'post': post.post,
#                 'category': post.category,
#                 'subcategory': post.subcategory,
#                 'likes': post.likes,
#                 'dislikes': post.dislikes,
#                 'shares': post.shares,
#                 # 'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Uncomment if created_at is included
#             }
#             posts_data.append(post_data)
        
#         return jsonify({'body': posts_data, 'message': 'User posts fetched successfully', 'status': 'success', 'statuscode': 200}), 200
#     except Exception as e:
#         return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statuscode': 500}), 500

def paginate_query(query, page, page_size):
    # Calculate number of posts to skip
    skip = (page - 1) * page_size
    # Limit the results and skip the previous pages
    posts = query.skip(skip).limit(page_size)
    # Get total count of documents in the collection
    total_items = query.count()
    return posts, total_items

@postcreation.route('/v1/posts', methods=['GET'])
def get_user_posts():
    user_id = request.headers.get('userId')
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)

    if not user_id:
        return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {}, 'message': 'User not found', 'status': 'error', 'statusCode': 404}), 404

    try:
        query = Post.objects(creator=user)  # This is your query
        # Implement pagination
        paginated_posts, total_items = paginate_query(query, page, page_size)
        posts_data = [{
            'id': str(post.id),
            'title': post.title,
            'summary': post.summary,
            'post': post.post,
            'category': post.category,
            'subcategory': post.subcategory,
            'likes': post.likes,
            'dislikes': post.dislikes,
            'shares': post.shares,
        } for post in paginated_posts]

        total_pages = (total_items + page_size - 1) // page_size  # Calculate total pages

        return jsonify({
            'body': posts_data,
            'totalItems': total_items,
            'totalPages': total_pages,
            'currentPage': page,
            'pageSize': page_size,
            'message': 'User posts fetched successfully',
            'status': 'success',
            'statusCode': 200
        }), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statusCode': 500}), 500



















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
 








@postcreation.route('/v1/user/categories', methods=['GET'])
def get_user_categories():
    user_id = request.headers.get('userId')
    
    if not user_id:
        return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statuscode': 400}), 400
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {}, 'message': 'User not found', 'status': 'error', 'statuscode': 404}), 404
    
    try:
        # Fetch distinct categories for the user's posts
        categories = Post.objects(creator=user).distinct('category')
        return jsonify({'body': {'categories': categories}, 'message': 'Categories fetched successfully', 'status': 'success', 'statuscode': 200}), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statuscode': 500}), 500



@postcreation.route('/v1/user/subcategories', methods=['GET'])
def get_user_subcategories():
    user_id = request.headers.get('userId')
    category = request.args.get('category')  # Get category from query params
    
    if not user_id:
        return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statuscode': 400}), 400
    
    if not category:
        return jsonify({'body': {}, 'message': 'Category is missing', 'status': 'error', 'statuscode': 400}), 400
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {}, 'message': 'User not found', 'status': 'error', 'statuscode': 404}), 404
    
    try:
        # Fetch distinct subcategories for the user's posts in the specified category
        subcategories = Post.objects(creator=user, category=category).distinct('subcategory')
        return jsonify({'body': {'subcategories': subcategories}, 'message': 'Subcategories fetched successfully', 'status': 'success', 'statuscode': 200}), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statuscode': 500}), 500
