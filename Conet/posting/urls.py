from django.urls import path
from . import post_api, views, Helper

urlpatterns = [
    ### HELPER START

    path('api/posts', post_api.PostReqHandler.as_view(), name='view_posts'),
    path('api/comments', post_api.CommentReqHandler.as_view(), name='view_comments'),
    path('create/', Helper.createPost, name='create_post'),
    path('<post_id>/', Helper.viewPost, name='post_details'),
    path('edit/<post_id>/', Helper.editPost, name='edit_post'),

    ### HELPER END


    ### API START

    path('', post_api.ReadAllPublicPosts.as_view(), name='view_public_posts'),
    path('<post_id>', post_api.ReadSinglePost.as_view(), name='view_post'),
    path('<post_id>/comments', post_api.ReadAndCreateAllCommentsOnSinglePost.as_view(), name='view_comments'),

    ### API END

    path('view/github', post_api.ReadGithubStream.as_view(), name='view_github'),

    #for remote
    path('<post_id>/', post_api.ReadSinglePost.as_view()),
    path('<post_id>/comments/', post_api.ReadAndCreateAllCommentsOnSinglePost.as_view()),
    path('/', post_api.ReadAllPublicPosts.as_view()),
]
