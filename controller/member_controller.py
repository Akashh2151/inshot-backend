from flask import Blueprint, jsonify, request
from model.postCreation_model import Post

from model.signInsignup_model import User
member=Blueprint('member',__name__)


@member.route('/v1/categories', methods=['GET'])
def get_posts_by_user_categories():
    try:
        # Assuming you don't need user authentication for this endpoint
        print("xyz")
        # Query all posts regardless of user
        posts = Post.objects.all()

        # Serialize posts data
        posts_data = [{
            'categories': post.categories,
        } for post in posts]
        
        response = {'body': posts_data, 'message': f'All categories retrieved successfully', 'status': 'success', 'statusCode': 200}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500



@member.route('/v1/subCategories', methods=['GET'])
def get_posts_by_subCategories():
    try:
        categories = request.args.get('categories') 
        
        # Query posts by subcategory
        posts = Post.objects.filter(categories=categories)
        
        # Serialize posts data
        posts_data = []
        for post in posts:
            post_dict = {
                'subCategories': post.subCategories,
            }
            posts_data.append(post_dict)

        response = {'body': posts_data,'categories':categories, 'message': f'Posts found for subCategories: {categories}', 'status': 'success', 'statusCode': 200}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500
 



 #function for pagination
def paginate_query(query, page, page_size):
    skip = (page - 1) * page_size
    posts = query.skip(skip).limit(page_size)
    total_items = query.count()
    return posts, total_items

@member.route('/v1/Allposts', methods=['GET'])
def get_Allposts():
    try:
        categories = request.args.get('categories', default=None)
        subCategories = request.args.get('subCategories', default=None)
        page = int(request.args.get('page', default=1, type=int))  # Default page is 1
        page_Size = int(request.args.get('page_Size', default=10, type=int))  # Default page size is 10

        # Query posts based on category and subcategory
        if categories and subCategories:
            posts = Post.objects.filter(categories=categories, subcategory=subCategories)
        elif categories:
            posts = Post.objects.filter(categories=categories)
        elif subCategories:
            posts = Post.objects.filter(subcategory=subCategories)
        else:
            return jsonify({'message': 'Please provide either category or subCategories parameter', 'status': 'error', 'statusCode': 400}), 400

        # Perform pagination
        paginated_posts, total_items = paginate_query(posts, page, page_Size)

        # Serialize posts data
        posts_data = []
        for post in paginated_posts:
            post_dict = {
                'title': post.title,
                'summary': post.summary,
                'post': post.post,
                'categories': post.categories,
                'subCategories': post.subCategories,
                # 'creator': post.creator.name  # Assuming creator has a username field
            }
            posts_data.append(post_dict)

        # Calculate total pages
        total_pages = -(-total_items // page_Size)  # Ceiling division to get total pages

        response = {
            'body': posts_data,
            'page': page,
            'per_page': page_Size,
            'total_pages': total_pages,
            'total_posts': total_items,
            'message': f'Posts found for category: {categories} and subcategory: {subCategories}',
            'status': 'success',
            'statusCode': 200
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500