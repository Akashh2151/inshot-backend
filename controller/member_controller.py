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
        

        # Query all posts if no category or subcategory is provided
        if not categories and not subCategories:
            posts = Post.objects()
           
        else:
            # Query posts based on category and subcategory
            if categories and subCategories:
                posts = Post.objects.filter(category_iexact=categories, subCategory_iexact=subCategories)
            elif categories:
                posts = Post.objects.filter(category__iexact=categories)
            elif subCategories:
                posts = Post.objects.filter(subCategory__iexact=subCategories)

        # Perform pagination
        paginated_posts, total_items = paginate_query(posts, page, pageSize)

        # Serialize posts data
        posts_data = []
        for post in paginated_posts:
            post_dict = {
                '_id': str(post.id),
                'title': post.title,
                'summary': post.summary,
                'post': post.post,
                'categories': post.category,
                'subCategories': post.subCategory,
                'likes':post.likes,
                'dislikes':post.dislikes,
                'shares':post.shares,
                'viewcount':post.viewcount
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