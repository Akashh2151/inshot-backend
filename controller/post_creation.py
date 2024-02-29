import re
from flask import Blueprint, jsonify,request
from model.signInsignup_model import User
from model.postCreation_model import   Comment, Dislike, Like, Post, Share 

postcreation=Blueprint('postcreation',__name__)


@postcreation.route('/v1/createpost', methods=['POST'])
def create_post():
    try:
        data = request.json
        user_id = request.headers.get('userId')     

        if not user_id:
            response = {'body': {},'message': 'UserID header is missing','status': 'error','statusCode': 400}
            return jsonify(response), 200   
        
        user = User.objects(id=user_id).first()     

        if not user:
            response = {'body': {},'message': 'The user ID entered does not correspond to an active user','status': 'error','statusCode': 404}
            return jsonify(response), 200    

        title = data.get('title')
        # Regex to match titles with characters and single spaces between words
        if not re.match("^[A-Za-z]+( [A-Za-z]+)*$", title):
            return jsonify({'body': {}, 'message': 'Title must only contain letters and single spaces between words', 'status': 'error', 'statusCode': 400}), 200
                      
        # Check if a post with the same title already exists
        existing_post = Post.objects(title=title).first()
        if existing_post:
            return jsonify({'body': {}, 'message': 'A post with this title already exists', 'status': 'error', 'statusCode': 400}), 200

        post = Post(
            title=data.get('title'),
            summary=data.get('summary'),
            post=data.get('post'),
            category=data.get('category'),
            subCategory=data.get('subCategory'),
            creator=user,
        )
        post.save()
        return jsonify({'body': data,'message': 'Post created successfully','postid': str(post.id),'status':'success',
                'statusCode': 201}), 200
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
            'subCategory': post.subCategory,
            'likes': post.likes,  
            'dislikes': post.dislikes,
            'shares': post.shares,
 
        }
        
        response = {'body': post_data,'message': 'Post retrieved successfully','status': 'success','statusCode': 200}
        return jsonify(response), 200
    
    except Post.DoesNotExist:
        response = {'body': {},'message': 'Post not found','status': 'error','statusCode': 404}
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
#                 'subCategory': post.subCategory,
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
            'subCategory': post.subCategory,
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



















# @postcreation.route('/v1/posts/<post_id>/like', methods=['POST'])
# def like_post(post_id):
#     try:
#         user_id = request.headers.get('userId')
#         if not user_id:
#             return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 200

#         user = User.objects.get(id=user_id)
#         post = Post.objects.get(id=post_id)

#         # Check if the user has already liked this post
#         existing_like = Like.objects(post=post, user=user).first()
#         if existing_like:
#             return jsonify({'body': {}, 'message': 'User already liked this post', 'status': 'error', 'statusCode': 400}), 200

#         like = Like(post=post, user=user)
#         like.save()
#         post.update(inc__likes=1)
#         post.reload()
#         return jsonify({'body': {}, 'message': 'Like added successfully', 'status': 'success', 'statusCode': 201}), 201
#     except (Post.DoesNotExist, User.DoesNotExist):
#         return jsonify({'body': {}, 'message': 'Post or User not found', 'status': 'error', 'statusCode': 404}), 404
#     except Exception as e:
#         return jsonify({'body': {}, 'message': str(e), 'status': 'error', 'statusCode': 500}), 500

    

# @postcreation.route('/v1/posts/<post_id>/dislike', methods=['POST'])
# def dislike_post(post_id):
#     try:
#         user_id = request.headers.get('userId')
#         if not user_id:
#             return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 200

#         user = User.objects.get(id=user_id)
#         post = Post.objects.get(id=post_id)

#         # Check if the user has already disliked this post
#         existing_dislike = Dislike.objects(post=post, user=user).first()
#         if existing_dislike:
#             return jsonify({'body': {}, 'message': 'User already disliked this post', 'status': 'error', 'statusCode': 400}), 200

#         dislike = Dislike(post=post, user=user)
#         dislike.save()
#         post.update(inc__dislikes=1)
#         post.reload()
#         return jsonify({'body': {}, 'message': 'Dislike added successfully', 'status': 'success', 'statusCode': 201}), 201
#     except (Post.DoesNotExist, User.DoesNotExist):
#         return jsonify({'body': {}, 'message': 'Post or User not found', 'status': 'error', 'statusCode': 404}), 404
#     except Exception as e:
#         return jsonify({'body': {}, 'message': str(e), 'status': 'error', 'statusCode': 500}), 500

# @postcreation.route('/v1/posts/<post_id>/share', methods=['POST'])
# def share_post(post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#         post.update(inc__shares=1)
#         post.reload()
#         return jsonify({'body': {'shares': post.shares}, 'message': 'Post shared successfully', 'status': 'success', 'statuscode': 200}), 200
#     except Post.DoesNotExist:
#         return jsonify({'body': {}, 'message': 'Post not found', 'status': 'error', 'statuscode': 404}), 404



@postcreation.route('/v1/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    try:
        user_id = request.headers.get('userId')
        if not user_id:
            return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 200

        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)

        # Check if the user has already liked this post
        existing_like = Like.objects(post=post, user=user).first()
        if existing_like:
            return jsonify({'body': {}, 'message': 'User already liked this post', 'status': 'error', 'statusCode': 400}), 200

        # Check if a dislike exists and remove it if so
        existing_dislike = Dislike.objects(post=post, user=user).first()
        if existing_dislike:
            existing_dislike.delete()
            post.update(dec__dislikes=1)

        like = Like(post=post, user=user)
        like.save()
        post.update(inc__likes=1)
        post.reload()
        return jsonify({'body': {}, 'message': 'Like added successfully', 'status': 'success', 'statusCode': 201}), 201
    except (Post.DoesNotExist, User.DoesNotExist):
        return jsonify({'body': {}, 'message': 'Post or User not found', 'status': 'error', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'body': {}, 'message': str(e), 'status': 'error', 'statusCode': 500}), 500


@postcreation.route('/v1/posts/<post_id>/dislike', methods=['POST'])
def dislike_post(post_id):
    try:
        user_id = request.headers.get('userId')
        if not user_id:
            return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 200

        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)

        # Check if the user has already disliked this post
        existing_dislike = Dislike.objects(post=post, user=user).first()
        if existing_dislike:
            return jsonify({'body': {}, 'message': 'User already disliked this post', 'status': 'error', 'statusCode': 400}), 200

        # Check if a like exists and remove it if so
        existing_like = Like.objects(post=post, user=user).first()
        if existing_like:
            existing_like.delete()
            post.update(dec__likes=1)

        dislike = Dislike(post=post, user=user)
        dislike.save()
        post.update(inc__dislikes=1)
        post.reload()
        return jsonify({'body': {}, 'message': 'Dislike added successfully', 'status': 'success', 'statusCode': 201}), 201
    except (Post.DoesNotExist, User.DoesNotExist):
        return jsonify({'body': {}, 'message': 'Post or User not found', 'status': 'error', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'body': {}, 'message': str(e), 'status': 'error', 'statusCode': 500}), 500





@postcreation.route('/v1/posts/<post_id>/share', methods=['POST'])
def share_post(post_id):
    try:
        # user_id = request.headers.get('userId')
        # if not user_id:
        #     return jsonify({'body': {}, 'message': 'userId header is missing', 'status': 'error', 'statusCode': 400}), 400

        # user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)

        # Optionally, you could check for excessive sharing in a short period and limit it here

        share = Share(post=post)
        share.save()
        post.update(inc__shares=1)
        post.reload()
        return jsonify({'body': {}, 'message': 'Post shared successfully', 'status': 'success', 'statusCode': 201}), 201
    except (Post.DoesNotExist, User.DoesNotExist):
        return jsonify({'body': {}, 'message': 'Post or User not found', 'status': 'error', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'body': {}, 'message': str(e), 'status': 'error', 'statusCode': 500}), 500


@postcreation.route('/v1/posts/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    try:
        user_id = request.headers.get('userId')
        if not user_id:
            return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400
        user = User.objects.get(id=user_id)
        data = request.json
        comment_content = data.get('comment')
        if not comment_content:
            return jsonify({'body': {}, 'message': 'Comment content is missing', 'status': 'error', 'statusCode': 400}), 400

        post = Post.objects.get(id=post_id)
        comment = Comment(post=post, author=user, content=comment_content)
        comment.save()
        post.update(inc__comment=1)
        post.reload()
        return jsonify({'body': {}, 'message': 'Comment added successfully', 'status': 'success', 'statusCode': 201}), 201
    except (Post.DoesNotExist, User.DoesNotExist):
        return jsonify({'body': {}, 'message': 'Post or User not found', 'status': 'error', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'body': {}, 'message': str(e), 'status': 'error', 'statusCode': 500}), 500
 



@postcreation.route('/v1/posts/<post_id>/interactions', methods=['GET'])
def get_post_interactions(post_id):
    try:
        post = Post.objects.get(id=post_id)

        # Fetch likes for the post
        likes = Like.objects(post=post).all()
        like_users = [str(like.user.id) for like in likes]

        # Fetch dislikes for the post
        dislikes = Dislike.objects(post=post).all()
        dislike_users = [str(dislike.user.id) for dislike in dislikes]

        # Fetch comments for the post
        comments = Comment.objects(post=post).all()
        comment_users = [str(comment.author.id) for comment in comments]

        # Fetch shares for the post
        shares = Share.objects(post=post).all()
        share_users = [str(share.user.id) for share in shares]

        return jsonify({
            'message': 'Interactions fetched successfully',
            'status': 'success',
            'statusCode': 200,
            'data': {
                'likes': like_users,
                'dislikes': dislike_users,
                'comments': comment_users,
                'shares': share_users,
            }
        }), 200
    except Post.DoesNotExist:
        return jsonify({
            'body': {},
            'message': 'Post not found',
            'status': 'error',
            'statusCode': 404
        }), 404
    except Exception as e:
        return jsonify({
            'body': {},
            'message': str(e),
            'status': 'error',
            'statusCode': 500
        }), 500















@postcreation.route('/v1/user/categories', methods=['GET'])
def get_user_categories():
    user_id = request.headers.get('userId')
    
    if not user_id:
        return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {}, 'message': 'User not found', 'status': 'error', 'statusCode': 404}), 404
    
    try:
        categories = Post.objects(creator=user).distinct('category')
        # Create an array of objects with each category as a separate object
        categories_response = [{'category': category} for category in categories]
        return jsonify({'body': {'categories': categories_response}, 'message': 'Categories fetched successfully', 'status': 'success', 'statusCode': 200}), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred:' + str(e), 'status': 'error', 'statusCode': 500}), 500



@postcreation.route('/v1/user/subcategories', methods=['GET'])
def get_user_subcategories():
    user_id = request.headers.get('userId')
    category = request.args.get('category')  # Get category from query params
    
    if not user_id:
        return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400
    
    if not category:
        return jsonify({'body': {}, 'message': 'Category is missing', 'status': 'error', 'statusCode': 400}), 400
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {}, 'message': 'User not found', 'status': 'error', 'statusCode': 404}), 404
    
    try:
        subcategories = Post.objects(creator=user, category=category).distinct('subCategory')
        # Create an array of objects with each subCategory as a separate object
        subcategories_response = [{'subCategory': subCategory} for subCategory in subcategories]
        return jsonify({'body': {'subcategories': subcategories_response}, 'message': 'Subcategories fetched successfully', 'status': 'success', 'statusCode': 200}), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statusCode': 500}), 500
