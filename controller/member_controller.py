import uuid
from flask import Blueprint, jsonify, request, session
from model.member_model import Dislike, Like, Post, Share
from werkzeug.exceptions import NotFound, BadRequest
from model.signInsignup_model import User
member=Blueprint('member',__name__)




@member.route('/v1/categories', methods=['GET'])
def get_posts_by_user_categories():
    try:
        
        # Query all posts regardless of user
        posts = Post.objects.all()
       

        # Serialize posts data
        posts_data = [{
            'categories': post.category,
        } for post in posts]

        response = {'body': posts_data, 'message': f'All categories fetched successfully', 'status': 'success', 'statusCode': 200}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500


@member.route('/v1/subCategories', methods=['GET'])
def get_posts_by_subCategories():
    try:
        categories = request.args.get('categories', default=None)
        
        posts = Post.objects.filter(category__iexact=categories)
    
        # Serialize posts data
        posts_data = []

        for post in posts:
            post_dict = {
                'subCategories': post.subCategory,
            }
            posts_data.append(post_dict)
         

        response = {'body': posts_data,'categories':categories, 'message': f'subCategories fetched successfully', 'status': 'success', 'statusCode': 200}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500
    
# _________________________________________________________________________________________________
# # Function for pagination
# def paginate_query(query, page, page_size):
#     skip = (page - 1) * page_size
#     posts = query.skip(skip).limit(page_size)
#     total_items = query.count()
#     return posts, total_items

# @member.route('/v1/Allposts', methods=['GET'])
# def get_Allposts():
#     try:
#         categories = request.args.get('categories', default=None)
#         subCategories = request.args.get('subCategory', default=None)
    
#         page = int(request.args.get('page', default=1, type=int))  # Default page is 1
#         pageSize = int(request.args.get('pageSize', default=10, type=int))  # Default page size is 10
        

#         # Query all posts if no category or subcategory is provided
#         if not categories and not subCategories:
#             posts = Post.objects()
           
#         else:
#             # Query posts based on category and subcategory
#             if categories and subCategories:
#                 posts = Post.objects.filter(category_iexact=categories, subCategory_iexact=subCategories)
#             elif categories:
#                 posts = Post.objects.filter(category__iexact=categories)
#             elif subCategories:
#                 posts = Post.objects.filter(subCategory__iexact=subCategories)

#         # Perform pagination
#         paginated_posts, total_items = paginate_query(posts, page, pageSize)

#         # Serialize posts data
#         posts_data = []
#         for post in paginated_posts:
#             post_dict = {
#                 '_id': str(post.id),
#                 'title': post.title,
#                 'summary': post.summary,
#                 'post': post.post,
#                 'categories': post.category,
#                 'subCategories': post.subCategory,
#                 'likes':post.likes,
#                 'dislikes':post.dislikes,
#                 'shares':post.shares,
#                 'viewcount':post.viewcount
#                 # 'creator': post.creator.name  # Assuming creator has a username field
#             }
#             posts_data.append(post_dict)

#         # Calculate total pages
#         total_pages = -(-total_items // pageSize)  # Ceiling division to get total pages

#         response = {
#             'body': posts_data,
#             'page': page,
#             'perPage': pageSize,
#             'totalPages': total_pages,
#             'totalPosts': total_items,
#             'message': f'User Posts fetched successfully ',
#             'status': 'success',
#             'statusCode': 200,
#             # 'input_string': input_string,
#             # 'is_uppercase': is_upper,
#             # 'is_lowercase': is_lower
#         }
#         return jsonify(response), 200
#     except Exception as e:
#         return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500


# #likes,shares,comment,dislike
# @member.route('/v1/manage-post-data/<post_id>', methods=['PUT'])
# def like_post(post_id):
#     try:
#         data = request.json
#         operation=data.get('operation')
#         post = Post.objects(id=post_id).first()
#         if operation=="like":
        
#             if post:
#                 post.likes += 1
#                 post.save()
#                 return jsonify({'message': 'Post liked successfully.'})
            
#         elif operation=="dislike":
        
#             if post:
#                 post.dislikes += 1
#                 post.save()
#                 return jsonify({'message': 'Post disliked successfully.'})
            
#         elif operation=="share":
        
#             if post:
#                 post.shares += 1
#                 post.save()
#                 return jsonify({'message': 'Post shared successfully.'})
#         else:
#             return jsonify({'error': 'Post not found.'}), 404
    
#     except Exception as e:
#         return jsonify({'error':str(e)})
# ______________________________________________________________________________________________


# all post
def paginate_query(query, page, page_size):
    skip = (page - 1) * page_size
    posts = query.skip(skip).limit(page_size)
    total_items = query.count()
    return posts, total_items

@member.route('/v1/member/posts', methods=['GET'])  # Changed route to reflect broader functionality
def get_posts():
    # Define allowed query parameters
    allowed_keys = {'page', 'pageSize', 'categories', 'subCategories'}
    # Check for any unexpected query parameters
    if any(key not in allowed_keys for key in request.args.keys()):
        return jsonify({'body': {}, 'message': 'Invalid query detected. Only specific parameters are permitted', 'status': 'error', 'statusCode': 400}), 400

    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)
    category = request.args.get('categories', default=None)
    subCategory = request.args.get('subCategories', default=None)

    try:
        # Start with a base query for posts
        query = Post.objects()

        # Filter by category if specified
        if category:
            query = query.filter(category__iexact=category)

        # Filter by subCategory if specified
        if subCategory:
            query = query.filter(subCategory__iexact=subCategory)

        # Implement pagination
        paginated_posts, total_items = paginate_query(query, page, page_size)
        posts_data = [{
            'title': post.title,
            'summary': post.summary,
            'post': post.post,
            'category': post.category,
            'postId': str(post.id),
            'subCategory': post.subCategory,
            'likes': post.likes,
            'dislikes': post.dislikes,
            'shares': post.shares,
            'comment': post.comment,
            'viewCount': post.viewCount
        } for post in paginated_posts]

        total_pages = (total_items + page_size - 1) // page_size

        return jsonify({
            'body': posts_data,
            'totalItems': total_items,
            'totalPages': total_pages,
            'currentPage': page,
            'pageSize': page_size,
            'message': 'Posts fetched successfully',
            'status': 'success',
            'statusCode': 200
        }), 200
    except Exception as e:
        return jsonify({'body': {}, 'message': 'An error occurred: ' + str(e), 'status': 'error', 'statusCode': 500}), 500




# like dislike share
@member.route('/v1/post/<post_id>/action', methods=['PUT'])
def handle_member_post_action(post_id):
    # user_id = request.headers.get('userId',None)
    action = request.args.get('action')  # Expected to be one of 'like', 'dislike', 'share'
    
    # if not user_id:
    #     return jsonify({'body':{},'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400

    try:
        post = Post.objects.get(id=post_id)
    except (Post.DoesNotExist):
        return jsonify({'body':{},'message': 'Post not found', 'status': 'error', 'statusCode': 404}), 404

    if action not in ['like', 'dislike', 'share']:
        return jsonify({'body':{},'message': 'Invalid action', 'status': 'error', 'statusCode': 400}), 400

    try:
        if action == 'like' or action == 'dislike':
            # Process like or dislike
            model = Like if action == 'like' else Dislike
            opposite_model = Dislike if action == 'like' else Like
            existing_reaction = model.objects(post=post).first()
            if existing_reaction:
                return jsonify({'body':{},'message': f'User already {action}d this post', 'status': 'error', 'statusCode': 400}), 400

            # Check if the opposite reaction exists and remove it
            existing_opposite_reaction = opposite_model.objects(post=post).first()
            if existing_opposite_reaction:
                existing_opposite_reaction.delete()
                post.update(**{'dec__likes' if action == 'dislike' else 'dec__dislikes': 1})

            # Add the new like or dislike
            reaction = model(post=post)
            reaction.save()
            post.update(**{'inc__likes' if action == 'like' else 'inc__dislikes': 1})

        elif action == 'share':
            # Process share
            share = Share(post=post)
            share.save()
            post.update(inc__shares=1)

        post.reload()
        return jsonify({'message': f'Post {action}d successfully', 'status': 'success', 'statusCode': 201}), 201

    except Exception as e:
        return jsonify({'body':{},'message': str(e), 'status': 'error', 'statusCode': 500}), 500


