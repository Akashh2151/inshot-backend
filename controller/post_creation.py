import re
from flask import Blueprint, jsonify,request
from model.signInsignup_model import User
from mongoengine.queryset.visitor import Q
from model.postCreation_model import   Comment, Dislike, Like, Post, Share 
from mongoengine.errors import DoesNotExist
postcreation=Blueprint('postcreation',__name__)



# @postcreation.route('/v1/createpost', methods=['POST'])
# def create_post():
#     try:
#         data = request.json
#         user_id = request.headers.get('userId')     

#         if not user_id:
#             response = {'body': {},'message': 'UserID header is missing','status': 'error','statusCode': 400}
#             return jsonify(response), 200   
        
#         user = User.objects(id=user_id).first()     

#         if not user:
#             response = {'body': {},'message': 'The user ID entered does not correspond to an active user','status': 'error','statusCode': 404}
#             return jsonify(response), 200    

#         title = data.get('title')
#         # Regex to match titles with characters and single spaces between words
#         if not re.match("^[A-Za-z]+( [A-Za-z]+)*$", title):
#             return jsonify({'body': {}, 'message': 'Title must only contain letters and single spaces between words', 'status': 'error', 'statusCode': 400}), 200
                      
#         # Check if a post with the same title already exists
#         existing_post = Post.objects(title=title).first()
#         if existing_post:
#             return jsonify({'body': {}, 'message': 'A post with this title already exists', 'status': 'error', 'statusCode': 400}), 200

#         post = Post(
#             title=data.get('title'),
#             summary=data.get('summary'),
#             post=data.get('post'),
#             category=data.get('category'),
#             subCategory=data.get('subCategory'),
#             creator=user,
#         )
#         post.save()
#         return jsonify({'body': data,'message': 'Post created successfully','postId': str(post.id),'status':'success',
#                 'statusCode': 201}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400


# Example categories and subcategories structure
categories = {
    'Technology': ['Software', 'Hardware', 'AI & Machine Learning'],
    'Health': ['Fitness', 'Nutrition', 'Mental Health'],
    'Education': ['K-12', 'Higher Education', 'Online Learning'],
    'Finance': ['Investing', 'Saving', 'Banking'],
    'Entertainment': ['Movies', 'Music', 'Video Games'],
    'Lifestyle': ['Travel', 'Fashion', 'Home Decor'],
    'Science': ['Biology', 'Physics', 'Chemistry'],
    'Sports': ['Football', 'Basketball', 'Tennis'],
    'Art': ['Painting', 'Sculpture', 'Photography'],
    'Food': ['Cooking', 'Baking', 'Restaurants']
}

@postcreation.route('/v1/categories', methods=['GET'])
def get_defcategories():
    try:
        category_param = request.args.get('category')
        
        if category_param:
            # Return subcategories for the given category if it exists
            if category_param in categories:
                subcategories_response = [{category_param: subcategory} for subcategory in categories[category_param]]
                return jsonify({
                    'status': 'success',
                    'statusCode': 200,
                    'message': 'Subcategories fetched successfully',
                    'body': subcategories_response
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Category not found',
                    'body': []
                }), 200
        else:
            # Return all categories if no specific category is requested
            categories_response = [{'category': category} for category in categories.keys()]
            return jsonify({
                'status': 'success',
                'statusCode': 200,
                'message': 'Categories fetched successfully',
                'body': categories_response
            }), 200
    except Exception as e:
            return jsonify({
                'status': 'error',
                'statusCode': 500,
                'message': 'An error occurred: ' + str(e),
                'body': []
            }), 500

@postcreation.route('/v1/createpost', methods=['POST'])
def create_post():
    try:
        data = request.json
        user_id = request.headers.get('userId')

        if not user_id:
            response = {'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}
            return jsonify(response), 200

        user = User.objects(id=user_id).first()

        if not user:
            response = {'body': {}, 'message': 'The user ID entered does not correspond to an active user', 'status': 'error', 'statusCode': 404}
            return jsonify(response), 200

        title = data.get('title')
        # Regex to match titles with characters and single spaces between words
        if not re.match("^[A-Za-z0-9]+( [A-Za-z0-9]+)*$", title):
            return jsonify({'body': {}, 'message': 'Title must only contain letters,numbers and single spaces between words', 'status': 'error', 'statusCode': 400}), 200

        # Check if a post with the same title already exists
        existing_post = Post.objects(title=title).first()
        if existing_post:
            return jsonify({'body': {}, 'message': 'A post with this title already exists', 'status': 'error', 'statusCode': 400}), 200

        # Set default category and subCategory if they are None
        category = data.get('category') if data.get('category') is not None else 'Default Category'
        subCategory = data.get('subCategory') if data.get('subCategory') is not None else 'Default SubCategory'

        post = Post(
            title=title,
            summary=data.get('summary'),
            post=data.get('post'),
            category=category,
            subCategory=subCategory,
            creator=user,
        )
        post.save()
        return jsonify({'body': data, 'message': 'Post created successfully', 'postId': str(post.id), 'status': 'success', 'statusCode': 201}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400







     



@postcreation.route('/v1/posts/<post_id>', methods=['GET'])
def view_post(post_id):
        try:
            post = Post.objects.get(id=post_id)
            
            # Fetch comments for the post
            comments = Comment.objects(post=post).all()
            comments_data = [{
                'content': comment.content,
                'authorName': comment.author.name if comment.author else "Anonymous",
                # 'created_at': comment.created_at.isoformat() if comment.created_at else None
            } for comment in comments]

            post_data = {
                'title': post.title,
                'summary': post.summary,
                'post': post.post,
                'category': post.category,
                'subCategory': post.subCategory,
                'likes': post.likes,
                'dislikes': post.dislikes,
                'shares': post.shares,
                'comments': comments_data,  # Add comments data here
                # 'created_at': post.created_at.isoformat() if post.created_at else None
            }
            
            response = {'body': post_data, 'message': 'Post retrieved successfully', 'status': 'success', 'statusCode': 200}
            return jsonify(response), 200
        
        except DoesNotExist:
            response = {'body': {}, 'message': 'Post not found', 'status': 'error', 'statusCode': 404}
            return jsonify(response), 404
        except Exception as e:
            response = {'body': {}, 'message': str(e), 'status': 'error', 'statusCode': 500}
            return jsonify(response), 500

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
    skip = (page - 1) * page_size
    posts = query.skip(skip).limit(page_size)
    total_items = query.count()
    return posts, total_items

@postcreation.route('/v1/posts', methods=['GET'])
def get_user_posts():
    user_id = request.headers.get('userId')
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)
    category = request.args.get('category', default=None)
    subCategory = request.args.get('subCategory', default=None)

    if not user_id:
        return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {}, 'message': 'User not found', 'status': 'error', 'statusCode': 404}), 404

    try:
        # Start with a basic query filtering by the creator (user)
        query = Post.objects(creator=user)

        # If category is specified, filter by category
        if category:
            query = query.filter(Q(category__iexact=category))

        # If subCategory is specified, filter by subCategory
        if subCategory:
            query = query.filter(Q(subCategory__iexact=subCategory))

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

        total_pages = (total_items + page_size - 1) // page_size

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



@postcreation.route('/v1/user/subCategories', methods=['GET'])
def get_user_subcategories():
    user_id = request.headers.get('userId')
    category = request.args.get('Categories')  # Get category from query params
    
    if not user_id:
        return jsonify({'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400
    
    if not category:
        return jsonify({'body': {}, 'message': 'Category is missing', 'status': 'error', 'statusCode': 400}), 400
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({'body': {}, 'message': 'User not found', 'status': 'error', 'statusCode': 404}), 404
    
    try:
        # Use regex to make category search case-insensitive
        # regex_category = re.compile('^{}$'.format(category), re.IGNORECASE)
        # subcategories = Post.objects(creator=user, category=regex_category).distinct('subCategory')
        

        subcategories = Post.objects(creator=user, category__iexact=category).distinct('subCategory')
        # If __iexact does not work, try the regex approach below:
        # Create an array of objects with each subCategory as a separate object
        subcategories_response = [{'subCategory': subCategory} for subCategory in subcategories]
        return jsonify({'body': {'subCategories': subcategories_response}, 'message': 'Subcategories fetched successfully', 'status': 'success', 'statusCode': 200}), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statusCode': 500}), 500
