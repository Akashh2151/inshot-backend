from flask import Blueprint, jsonify, request
from model.postCreation_model import Post

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
        category = request.args.get('category', default=None)
        category = request.args.get('string', default='', type=str)
         # Check if the string is in uppercase
        is_upper = category.isupper()

        # Check if the string is in lowercase
        is_lower = category.islower()
       
       

        # Query posts by subcategory
        # posts = Post.objects.filter(category=category)
        posts = Post.objects.filter(category=category)
    
        # Serialize posts data
        posts_data = []

        for post in posts:
            post_dict = {
                'subCategories': post.subCategory,
            }
            posts_data.append(post_dict)
         

        response = {'body': posts_data,'categories':category, 'message': f'subCategories fetched successfully', 'status': 'success', 'statusCode': 200}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500
    



# Function for pagination
def paginate_query(query, page, page_size):
    skip = (page - 1) * page_size
    posts = query.skip(skip).limit(page_size)
    total_items = query.count()
    return posts, total_items

@member.route('/v1/Allposts', methods=['GET'])
def get_Allposts():
    try:
        categories = request.args.get('categories', default=None)
        subCategories = request.args.get('subCategory', default=None)
    
        page = int(request.args.get('page', default=1, type=int))  # Default page is 1
        pageSize = int(request.args.get('pageSize', default=10, type=int))  # Default page size is 10
        categories = request.args.get('string', default='', type=str)

        # Check if the string is in uppercase
        is_upper = categories.isupper()

        # Check if the string is in lowercase
        is_lower = categories.islower()
       

        # Query all posts if no category or subcategory is provided
        if not categories and not subCategories:
            posts = Post.objects.all()
        else:
            # Query posts based on category and subcategory
            if categories and subCategories:
                posts = Post.objects.filter(category=categories, subCategory=subCategories)
            elif categories:
                posts = Post.objects.filter(category=categories)
            elif subCategories:
                posts = Post.objects.filter(subCategory=subCategories)

        # Perform pagination
        paginated_posts, total_items = paginate_query(posts, page, pageSize)

        # Serialize posts data
        posts_data = []
        for post in paginated_posts:
            post_dict = {
                'title': post.title,
                'summary': post.summary,
                'post': post.post,
                'categories': post.category,
                'subCategories': post.subCategory,
                # 'creator': post.creator.name  # Assuming creator has a username field
            }
            posts_data.append(post_dict)

        # Calculate total pages
        total_pages = -(-total_items // pageSize)  # Ceiling division to get total pages

        response = {
            'body': posts_data,
            'page': page,
            'perPage': pageSize,
            'totalPages': total_pages,
            'totalPosts': total_items,
            'message': f'User Posts fetched successfully ',
            'status': 'success',
            'statusCode': 200,
            # 'input_string': input_string,
            # 'is_uppercase': is_upper,
            # 'is_lowercase': is_lower
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500

    



#likes,shares,comment,dislike
@member.route('/v1/manage-post-data/<post_id>', methods=['PUT'])
def like_post(post_id):
    try:
        data = request.json
        operation=data.get('operation')
        post = Post.objects(id=post_id).first()
        if operation=="like":
        
            if post:
                post.likes += 1
                post.save()
                return jsonify({'message': 'Post liked successfully.'})
            
        elif operation=="dislike":
        
            if post:
                post.dislikes += 1
                post.save()
                return jsonify({'message': 'Post disliked successfully.'})
            
        elif operation=="share":
        
            if post:
                post.shares += 1
                post.save()
                return jsonify({'message': 'Post shared successfully.'})
        else:
            return jsonify({'error': 'Post not found.'}), 404
    
    except Exception as e:
        return jsonify({'error':str(e)})