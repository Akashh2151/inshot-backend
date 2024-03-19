from datetime import datetime
import re
import uuid
from flask import Blueprint, jsonify, request, session
from model.member_model import Dislike, Like, News, Post, Share, categories
from werkzeug.exceptions import NotFound, BadRequest
from model.signInsignup_model import User
member=Blueprint('member',__name__)


@member.route('/v2/news/<news_id>', methods=['GET'])
def get_single_news(news_id):
    try:
        # Retrieve the news item by its ID
        news_item = News.objects.get(id=news_id)
        print("news_item",news_item)
        
        if not news_item:
            return jsonify({'message': 'News not found', 'status': 'error', 'statusCode': 404}), 404

        # Serialize the news data
        news_dict = {
            '_id': str(news_item.id),
            'title': news_item.title,
            'summary': news_item.summary,
            'content': news_item.content,
            'createdAt': news_item.created_At.strftime('%Y-%m-%d %H:%M:%S'),
            'author': str(news_item.author),  # Assuming author is a string field
            'reference': news_item.reference,
            'likes': news_item.likes,
            'dislikes': news_item.dislikes,
            'comments': news_item.comments,
            'shares': news_item.shares,
            'viewCount': news_item.viewCount,
            'validTill': news_item.validTill.strftime('%Y-%m-%d %H:%M:%S'),
            'niche': news_item.niche,
            'category': news_item.category,
            'subCategory': news_item.subCategory
        }

        return jsonify({'body': news_dict, 'message': 'News fetched successfully', 'status': 'success', 'statusCode': 200}), 200

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500


# @member.route('/createcategorys',methods=['POST'])
# def create_categorys():
#     try:
#         data=request.json
#         cate=data.get('category')
#         subcate=data.get('subCategory')

#         all=categories(
#             category=cate,
#             subCategory=subcate
#         )
#         all.save()
#         return jsonify({'s':"succfully"})
    
#     except Exception as e:
#         return jsonify({'error':str(e)})    



# Assuming 'categories' is your model and it has fields 'category' and 'subCategory'
@member.route('/v1/member/categories', methods=['GET'])
def get_categories_and_subcategories():
    try:
        # Check if a specific category is ss
        categorie = request.args.get('categorie', default=None)
        
        if categorie:
            # Fetch subcategories for the specified category
            posts = categories.objects.filter(category__iexact=categorie)
            
            # Serialize posts data for the specific category
            posts_data = [{
                'subCategories': post.subCategory,
            } for post in posts]

            response = {
                'body': posts_data,
                'categories': categorie,
                'message': f'Subcategories for {categorie} fetched successfully',
                'status': 'success',
                'statusCode': 200
            }
        else:
            # Fetch all categories if no specific category is requested
            posts = categories.objects.all()
            
            # Serialize posts data for all categories
            posts_data = [{
                'categories': post.category,
            } for post in posts]

            response = {
                'body': posts_data,
                'message': 'All categories fetched successfully',
                'status': 'success',
                'statusCode': 200
            }

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
    # Order by 'created_at' in descending order, then skip and limit
    posts = query.order_by('-created_at').skip(skip).limit(page_size)
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
            "slug":post.slug,
            'shares': post.shares,
            'comment': post.comment,
            'viewCount': post.viewCount,
            "created_at": post.created_at.isoformat() if post.created_at else None
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




# # like dislike share
# @member.route('/v1/post/<post_id>/action', methods=['PUT'])
# def handle_member_post_action(post_id):
#     # user_id = request.headers.get('userId',None)
#     action = request.args.get('action')  # Expected to be one of 'like', 'dislike', 'share'
    
#     # if not user_id:
#     #     return jsonify({'body':{},'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}), 400

#     try:
#         post = Post.objects.get(id=post_id)
#     except (Post.DoesNotExist):
#         return jsonify({'body':{},'message': 'Post not found', 'status': 'error', 'statusCode': 404}), 404

#     if action not in ['like', 'dislike', 'share']:
#         return jsonify({'body':{},'message': 'Invalid action', 'status': 'error', 'statusCode': 400}), 400

#     try:
#         if action == 'like' or action == 'dislike':
#             # Process like or dislike
#             model = Like if action == 'like' else Dislike
#             opposite_model = Dislike if action == 'like' else Like
#             existing_reaction = model.objects(post=post).first()
#             if existing_reaction:
#                 return jsonify({'body':{},'message': f'User already {action}d this post', 'status': 'error', 'statusCode': 400}), 400

#             # Check if the opposite reaction exists and remove it
#             existing_opposite_reaction = opposite_model.objects(post=post).first()
#             if existing_opposite_reaction:
#                 existing_opposite_reaction.delete()
#                 post.update(**{'dec__likes' if action == 'dislike' else 'dec__dislikes': 1})

#             # Add the new like or dislike
#             reaction = model(post=post)
#             reaction.save()
#             post.update(**{'inc__likes' if action == 'like' else 'inc__dislikes': 1})

#         elif action == 'share':
#             # Process share
#             share = Share(post=post)
#             share.save()
#             post.update(inc__shares=1)

#         post.reload()
#         return jsonify({'message': f'Post {action}d successfully', 'status': 'success', 'statusCode': 201}), 201

#     except Exception as e:
#         return jsonify({'body':{},'message': str(e), 'status': 'error', 'statusCode': 500}), 500


@member.route('/v1/post/<post_id>/action', methods=['PUT'])  # Consider using POST
def like_post(post_id):
    try:
        operation = request.args.get('action')
        
        # Ensure operation is provided
        if not operation:
            return jsonify({'body':{},'message': 'No operation provided','status': 'error', 'statusCode': 400}), 200

        post = Post.objects(id=post_id).first()

        # Ensure post exists
        if not post:
            return jsonify({'body':{},'message': 'Post not found','status': 'error', 'statusCode': 404}), 200

        # Perform the action
        if operation == "like":
            post.likes += 1
        elif operation == "dislike":
            post.dislikes += 1
        elif operation == "share":
            post.shares += 1
        else:
            # Operation not supported
            return jsonify({'body':{},'message': 'Operation not supported','status': 'error', 'statusCode': 400}), 200

        post.save()
        return jsonify({'body':{},'message': f'Post {operation} successfully','status': 'success','statusCode': 200}),200

    except Exception as e:
        # Logging the exception can be helpful for debugging
        # logger.error(f"Error in like_post: {str(e)}")
        return jsonify({'body':{},"message":str(e),'status':'error','statusCode': 500}), 500
    





@member.route('/v2/news/create-news', methods=['POST'])
def create_news():
    try:
        data = request.json
        user_id = request.headers.get('userId')
        print("user_id", user_id)
        if not user_id:
            response = {'body': {}, 'message': 'UserID header is missing', 'status': 'error', 'statusCode': 400}
            return jsonify(response), 200

        user = User.objects(id=user_id).first()
        
        if not user:
            response = {'body': {}, 'message': 'The user ID entered does not correspond to an active user',
                        'status': 'error', 'statusCode': 404}
            return jsonify(response), 200

        # Extract data from JSON
        title = data.get('title')
        summary = data.get('summary')
        content = data.get('content')
        created_at_str = data.get('createdAt')  # Retrieve date string from JSON
        author = data.get('author')
        reference = data.get('reference')
        likes = data.get('likes')
        dislikes = data.get('dislikes')
        comments = data.get('comments')
        shares = data.get('shares')
        viewCount = data.get('viewCount')
        validTill_str = data.get('validTill')  # Retrieve date string from JSON
        niche = data.get('niche')
        category = data.get('category')
        subCategory = data.get('subCategory')
        # Add more fields as needed

        # Validate title format
        if not re.match("^[A-Za-z]+( [A-Za-z]+)*$", title):
            return jsonify({'body': {}, 'message': 'Title must only contain letters and single spaces between words',
                            'status': 'error', 'statusCode': 400}), 200

        # Check if a post with the same title already exists
        existing_post = News.objects(title=title).first()
        if existing_post:
            return jsonify({'body': {}, 'message': 'A post with this title already exists', 'status': 'error',
                            'statusCode': 400}), 200

        # Parse datetime strings to datetime objects
        created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%S')
        validTill = datetime.strptime(validTill_str, '%Y-%m-%dT%H:%M:%S')

        # Create and save the post
        post = News(
            title=title,
            summary=summary,
            content=content,
            created_At=created_at,
            author=author,
            reference=reference,
            likes=likes,
            dislikes=dislikes,
            comments=comments,
            shares=shares,
            viewCount=viewCount,
            validTill=validTill,
            niche=niche,
            category=category,
            subCategory=subCategory,
        )
        post.save()

        # Prepare and return response
        response_data = {
            'body': data,
            'message': 'Post created successfully',
            'postId': str(post.id),
            'status': 'success',
            'statusCode': 201
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    


#news allpost
# Function for pagination
def paginate_query(query, page, page_size):
    skip = (page - 1) * page_size
    posts = query.skip(skip).limit(page_size)
    total_items = query.count()
    return posts, total_items

@member.route('/v2/news/all-news', methods=['GET'])
def get_allnews():
    try:
        page = int(request.args.get('page', default=1, type=int))
        pageSize = int(request.args.get('pageSize', default=10, type=int))
        sort_order = request.args.get('sort', default='asc')  # Default sorting order
        niche = request.args.get('niche')
        categories = request.args.get('category')
        subCategories = request.args.get('subCategory')
        
        # Construct query based on provided parameters
        query = News.objects()

        if niche:
            query = query.filter(niche__iexact=niche)
        if categories:
            query = query.filter(category__iexact=categories)
        if subCategories:
            query = query.filter(subCategory__iexact=subCategories)

        # Sort query results
        if sort_order.lower() == 'asc':
            query = query.order_by('created_At')
        elif sort_order.lower() == 'desc':
            query = query.order_by('-created_At')
        
        # Perform pagination
        paginated_news, total_items = paginate_query(query, page, pageSize)

        # Serialize news data
        news_data = []
        for news_item in paginated_news:
            news_dict = {
                '_id': str(news_item.id),
                'title': news_item.title,
                'summary': news_item.summary,
                'content': news_item.content,
                'createdAt': news_item.created_At.strftime('%Y-%m-%d %H:%M:%S'),
                'author': str(news_item.author),  # Assuming author is a string field
                'reference': news_item.reference,
                'likes': news_item.likes,
                'dislikes': news_item.dislikes,
                'comments': news_item.comments,
                'shares': news_item.shares,
                'viewCount': news_item.viewCount,
                'validTill': news_item.validTill.strftime('%Y-%m-%d %H:%M:%S'),
                'niche': news_item.niche,
                'category': news_item.category,
                'subCategory': news_item.subCategory
            }
            news_data.append(news_dict)

        # Calculate total pages
        total_pages = -(-total_items // pageSize)  # Ceiling division to get total pages

        response = {
            'body': news_data,
            'page': page,
            'perPage': pageSize,
            'totalPages': total_pages,
            'totalPosts': total_items,
            'message': 'News fetched successfully',
            'status': 'success',
            'statusCode': 200
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500